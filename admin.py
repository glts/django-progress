from django.contrib import admin

from .models import Topic, Challenge, Routine, Portion, Effort, Tag


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'updated_date')


class PortionInline(admin.TabularInline):
    model = Portion


class EffortInline(admin.TabularInline):
    model = Effort
    extra = 1


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'topic', 'updated_date', 'done')
    inlines = [PortionInline]


class RoutineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'topic', 'updated_date')
    inlines = [EffortInline]


class TagAdmin(admin.ModelAdmin):
    model = Tag


admin.site.register(Topic, TopicAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Routine, RoutineAdmin)
admin.site.register(Tag, TagAdmin)
