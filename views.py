import logging
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.db.models import Count, Max
from django.views.decorators.csrf import ensure_csrf_cookie
from progress.models import Topic, Task, Challenge, Routine, Portion, Effort, Tag
from progress.forms import TaskForm, ChallengeForm


logger = logging.getLogger(__name__)


def task_stats_for_topic(topic=None):
    """Return the number of "open" and "done" tasks as well as the sum total.

    Queries the database to determine these numbers for a given Topic. If no
    Topic is given the numbers are cumulative for all Tasks in the database.
    """
    if topic:
        manager = topic.tasks
        lookup = {'topic': topic}
    else:
        manager = Task.objects
        lookup = {}
    return {
        'total': manager.count(),
        'open': len([challenge for challenge in Challenge.objects.filter(**lookup) if not challenge.done()]) + \
                Routine.objects.filter(**lookup).count(),
        'done': len(([challenge for challenge in Challenge.objects.filter(**lookup) if challenge.done()])),
    }


@ensure_csrf_cookie
def index(request):
    active_topic_ids = Task.objects.all().values('topic')
    idle_topics = Topic.objects.exclude(id__in=active_topic_ids).order_by('-created_date')
    active_topics = Topic.objects.filter(id__in=active_topic_ids) \
            .annotate(most_recent_update=Max('tasks__updated_date')) \
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
                elif not challenge.done():
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


def create_topic(request):
    return HttpResponse("Not yet implemented: Create topic")


def task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'progress/task.html', {'task': task})


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


# TODO This annotation deprecated in Django 1.6
@transaction.commit_on_success
def create_task(request, topic_id):

    # TODO Implement create_task, especially Routine

    topic = get_object_or_404(Topic, pk=topic_id)

    # TODO cleanup: this means create challenge not task!
    task_type = Challenge
    if request.method == 'POST' and task_type == Challenge:
        taskform = ChallengeForm(request.POST)
        bulk_portions = request.POST['bulk_portions']
        portions = bulk_lines_to_portions(bulk_portions.splitlines())
        if taskform.is_valid() and portions:
            challenge = taskform.save(commit=False)
            challenge.topic = topic
            challenge.save()
            for order, portion in enumerate(portions):
                portion.challenge = challenge
                portion._order = order
            Portion.objects.bulk_create(portions)
    else:
        taskform = ChallengeForm()
    return render(request, 'progress/create_task.html', {
        'topic': topic,
        'topic_stats': task_stats_for_topic(topic),
        'taskform': taskform,
    })


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return HttpResponse("Not yet implemented: Edit task")


def tags_index(request):
    tags = get_list_or_404(Tag.objects.all())
    orphaned_tags = []
    used_tags = [tag for tag in tags if tag.tasks.exists() or orphaned_tags.append(tag)]
    return render(request, 'progress/tags_index.html', {
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
            pass # invalid request
    else:
        pass
    return HttpResponse()
