from django.conf.urls import patterns, url

urlpatterns = patterns('progress.views',

    # published
    url(r'^$', 'index', name='index'),
    url(r'^topics/new$', 'create_topic', name='create_topic'),
    url(r'^topics/(?P<topic_id>\d+)/tasks/new$', 'create_task', name='create_task'),
    url(r'^tasks/(?P<task_id>\d+)$', 'task', name='task'),
    url(r'^tasks/(?P<task_id>\d+)/edit$', 'edit_task', name='edit_task'),
    url(r'^tags$', 'tags_index', name='tags_index'),

    # internal
    url(r'^tasks/(?P<task_id>\d+)/portions/(?P<portion_id>\d+)/close$',
            'close_portion', name='close_portion'),

)
