import json
import logging

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.db import transaction
from django.db.models import Count, Max
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from django.utils.translation import ugettext as _

from .models import Topic, Task, Challenge, Routine, Portion, Effort, Tag
from .forms import TaskForm, ChallengeForm, RoutineForm


logger = logging.getLogger(__name__)


def task_stats_for_topic(topic=None):
    """Return basic task stats for a Topic.

    For a given Topic, this returns the number of "open" and "done"
    tasks, as well as the sum total of tasks. When no Topic is given the
    numbers are for all Tasks in the database.
    """
    if topic is None:
        manager = Task.objects
        lookup = {}
    else:
        manager = topic.tasks
        lookup = {'topic': topic}
    return {
        'total': manager.count(),
        'open': Challenge.objects.filter(**lookup).filter(done=False).count() + Routine.objects.filter(**lookup).count(),
        'done': Challenge.objects.filter(**lookup).filter(done=True).count(),
    }


@ensure_csrf_cookie
def index(request):
    active_topic_ids = Task.objects.all().values('topic')
    idle_topics = Topic.objects.exclude(id__in=active_topic_ids).order_by('-created_date')
    active_topics = Topic.objects.filter(id__in=active_topic_ids) \
            .annotate(most_recent_update=Max('task__updated_date')) \
            .order_by('-most_recent_update')

    topics = []
    for topic in idle_topics:
        topics.append({
            'topic': topic,
            'tasks': [],
            'stats': {'total': 0, 'open': 0, 'done': 0},
        })
    for topic in active_topics:
        tasks = topic.tasks.order_by('-updated_date')
        invalid, open, done = [], [], []
        for task in tasks:
            ischallenge = False
            try:
                ischallenge = task.challenge is not None
            except Challenge.DoesNotExist:
                pass
            if ischallenge:
                challenge = task.challenge
                if not challenge.portions.exists():
                    invalid.append((True, challenge))
                elif not challenge.done:
                    open.append((True, challenge))
                else:
                    done.append((True, challenge))
            else:
                open.append((False, task.routine))
        ordered_tasks = invalid + open + done
        topics.append({
            'topic': topic,
            'tasks': ordered_tasks,
            'stats': task_stats_for_topic(topic),
        })

    topic_stats = task_stats_for_topic()

    recent_portions = Portion.objects.filter(done=True).order_by('-done_date')[:5]
    zipped_portions = map(lambda p: (p.done_date, p), recent_portions)
    recent_efforts = Effort.objects.all()[:5]
    zipped_efforts = map(lambda e: (e.date, e), recent_efforts)
    sorted_activities = sorted(list(zipped_portions) + list(zipped_efforts), key=lambda x: x[0], reverse=True)[:5]

    activities = []
    for activity in sorted_activities:
        if isinstance(activity[1], Portion):
            portion = activity[1]
            activities.append({
                'portion': True,
                'challenge': portion.challenge,
                'description': portion.description,
                'date': portion.done_date,
            })
        else:
            effort = activity[1]
            activities.append({
                'portion': False,
                'routine': effort.routine,
                'date': effort.date
            })

    return render(request, 'progress/index.html', {
        'topics': topics,
        'topic_stats': topic_stats,
        'recent_activities': activities,
    })


class TopicDetailView(DetailView):
    model = Topic


class TopicCreateView(CreateView):
    model = Topic


class TopicUpdateView(UpdateView):
    model = Topic


def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'progress/task_detail.html', {'task': task})


def bulk_lines_to_portions(lines):
    portions = []
    for line in filter(lambda l: l and not l.isspace(), lines):
        fields = line.split('\t', 1)
        description = fields[0].strip()[0:40] # FIXME ugliness
        if not description:
            continue
        size = 1
        if len(fields) > 1:
            try:
                size = max(int(fields[1].strip()), 1)
            except ValueError:
                pass
        portions.append(Portion(description=fields[0], size=size))
    return portions


@transaction.atomic
def task_new(request, topic_id):

    topic = get_object_or_404(Topic, pk=topic_id)

    # tricky: the only reason we differentiate between ChallengeForm and
    # RoutineForm is that we can obtain a Challenge/Routine instance through
    # the save() method. There's no difference in the template.
    if request.method == 'POST':
        task_type = request.POST['task_type']
        if task_type == 'C':
            form = ChallengeForm(request.POST)
        elif task_type == 'R':
            form = RoutineForm(request.POST)
        else:
            return HttpResponseBadRequest()
        if form.is_valid():
            if task_type == 'C':
                bulk_portions = request.POST['bulk_portions']
                portions = bulk_lines_to_portions(bulk_portions.splitlines())
                task = form.save(commit=False)
                task.topic = topic
                task.save()
                form.save_m2m()
                for order, portion in enumerate(portions):
                    portion.challenge = task
                    portion._order = order
                Portion.objects.bulk_create(portions)
            else:
                task = form.save(commit=False)
                task.topic = topic
                task.save()
                form.save_m2m()
            return HttpResponseRedirect(task.get_absolute_url())
    else:
        form = TaskForm()
    return render(request, 'progress/task_new.html', {
        'topic': topic,
        'topic_stats': task_stats_for_topic(topic),
        'taskform': form,
    })


def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return HttpResponse(_("Not yet implemented: Edit task"))


def tag_list(request):
    tags = get_list_or_404(Tag.objects.all())
    orphaned_tags = []
    used_tags = [tag for tag in tags if tag.tasks.exists() or orphaned_tags.append(tag)]
    return render(request, 'progress/tag_list.html', {
        'tags': tags,
        'used_tags': used_tags,
        'orphaned_tags': orphaned_tags,
    })


def close_portion(request, task_id, portion_id):
    if request.method == 'POST' and request.is_ajax():
        portion = get_object_or_404(Portion, pk=portion_id)
        if portion.challenge.pk == int(task_id) and not portion.done:
            portion.done = True
            portion.save()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['POST'])
    done = Challenge.objects.get(pk=portion.challenge.pk).done
    return HttpResponse(json.dumps({'challenge': {'done': done}}), content_type='application/json')


def routine_touch(request, task_id):
    if request.method == 'POST' and request.is_ajax():
        routine = get_object_or_404(Routine, pk=task_id)
        effort = Effort.objects.create(routine=routine)
    else:
        return HttpResponseNotAllowed(['POST'])
    return HttpResponse(json.dumps({
        'routine': {
            'most_recent_effort': {
                'id': effort.pk,
                'date': str(timezone.localtime(effort.date)),
            },
        },
    }), content_type='application/json')
