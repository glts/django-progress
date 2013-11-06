from django.forms.models import modelform_factory

from .models import Task, Challenge, Routine


TaskForm = modelform_factory(Task, exclude=('topic',))
ChallengeForm = modelform_factory(Challenge, exclude=('topic',))
RoutineForm = modelform_factory(Routine, exclude=('topic',))
