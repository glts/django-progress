from django.db import models
from django.db.models import F, Sum
from django.core.urlresolvers import reverse
from django.utils import timezone


class Topic(models.Model):
    """An area of interest.

    A Topic represents some field of interest and serves as the header
    to which tasks are assigned. A Topic could be a foreign language or
    a programming project or a musical instrument.

    >>> topic = Topic(title="Lisp")
    >>> topic.save()
    """
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_topic', args=[self.pk])

    def updated_date(self):
        if self.tasks.exists():
            return self.tasks.latest('updated_date').updated_date
        else:
            return self.created_date


class Tag(models.Model):
    """A label for tasks."""
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def related(self):
        if self.pk is None or not Task.objects.filter(tags__in=[self.pk]).exists():
            return Tag.objects.none()
        else:
            return Tag.objects.filter(tasks__in=self.tasks.all()).exclude(pk=self.pk).distinct()


class Task(models.Model):
    """An item of work, can be either a Challenge or a Routine.

    Do not instantiate Tasks directly, a Task must always be created via
    the Challenge or Routine subclass.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='tasks')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='tasks')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_task', args=[self.pk])


class Challenge(Task):
    done = models.BooleanField(editable=False, default=False)


class Routine(Task):
    pass


class Portion(models.Model):
    description = models.CharField(max_length=40)
    challenge = models.ForeignKey(Challenge, related_name='portions')
    done = models.BooleanField(default=False)
    done_date = models.DateTimeField(null=True, editable=False)
    size = models.IntegerField(default=1)

    class Meta:
        order_with_respect_to = 'challenge'

    def __str__(self):
        return '{} [{}]'.format(self.challenge.name, self._order)

    def save(self, *args, **kwargs):
        was_done = False
        if self.pk is not None:
            was_done = Portion.objects.get(pk=self.pk).done
        if self.done and not was_done:
            self.done_date = timezone.now()
        elif not self.done and was_done:
            self.done_date = None

        super().save(*args, **kwargs)

        all_done = all(portion.done for portion in self.challenge.portions.all())
        Challenge.objects.filter(pk=self.challenge.pk).update(done=all_done,
                                                              updated_date=timezone.now())

    def delete(self, *args, **kwargs):
        was_done = self.done
        siblings = self.challenge.portions.exclude(pk=self.pk)

        super().delete(*args, **kwargs)

        # Update order of following Portions, bypassing Portion.save()
        siblings.filter(_order__gt=self._order).update(_order=F('_order')-1)

        if not was_done and all(portion.done for portion in siblings):
            Challenge.objects.filter(pk=self.challenge.pk).update(done=True)

    def relative_size(self):
        total_size = self.challenge.portions.aggregate(Sum('size'))['size__sum']
        return self.size / total_size * 100


class Effort(models.Model):
    """A work session, a contribution to a Routine.

    An Effort records the date on which work on a routine task was put
    in. The accompanying note is optional.
    """
    note = models.CharField(max_length=200, blank=True)
    routine = models.ForeignKey(Routine, related_name='efforts')
    date = models.DateTimeField(default=lambda:timezone.now())

    class Meta:
        ordering = ('-date',)
        get_latest_by = 'date'

    def __str__(self):
        return '{} {}'.format(self.routine, self.date)
