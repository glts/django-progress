from django.forms.models import modelform_factory

from .models import Task, Challenge, Routine


TaskForm = modelform_factory(Task, fields=('name', 'description'))
ChallengeForm = modelform_factory(Challenge, fields=('name', 'description'))
RoutineForm = modelform_factory(Routine, fields=('name', 'description'))
