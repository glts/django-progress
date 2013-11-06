from django.forms.models import modelform_factory

from .models import Task, Challenge, Routine


TaskForm = modelform_factory(Task, fields=('name', 'description', 'tags'))
ChallengeForm = modelform_factory(Challenge, fields=('name', 'description', 'tags'))
RoutineForm = modelform_factory(Routine, fields=('name', 'description', 'tags'))
