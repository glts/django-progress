from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('progress.views',

    # published
    url(r'^$', 'index', name='index'),

    url(r'^topics/new$', views.TopicCreateView.as_view(), name='topic_new'),
    url(r'^topics/(?P<pk>\d+)$', views.TopicDetailView.as_view(), name='topic_detail'),
    url(r'^topics/(?P<pk>\d+)/edit$', views.TopicUpdateView.as_view(), name='topic_edit'),

    url(r'^topics/(?P<topic_id>\d+)/tasks/new$', 'task_new', name='task_new'),
    url(r'^tasks/(?P<task_id>\d+)$', 'task_detail', name='task_detail'),
    url(r'^tasks/(?P<task_id>\d+)/edit$', 'task_edit', name='task_edit'),

    url(r'^tags$', 'tag_list', name='tag_list'),

    # internal
    url(r'^tasks/(?P<task_id>\d+)/portions/(?P<portion_id>\d+)/close$',
            'close_portion', name='close_portion'),

)
