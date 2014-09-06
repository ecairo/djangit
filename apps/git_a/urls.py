from django.conf.urls import patterns, url

from apps.git_a.views import repo_index, repo_details, commit_details, object_details

urlpatterns = patterns(
    '',
    url(r'^(?P<repo_name>[\w_-]+)/tree/(?P<object_hash>[\w\d]+)/$',
        object_details, name='object_details'),

    url(r'^(?P<repo_name>[\w_-]+)/commit/(?P<commit_hash>[\w\d]+)/$',
        commit_details, name='commit_details'),

    url(r'^(?P<repo_name>[\w_-]+)$',
        repo_details, name='repository_index'),

    url(r'^(?P<repo_name>[\w_-]+)/(?P<tree_hash>[\w\d]+)/$',
        repo_details, name='repository_navigate'),

    url(r'^$',
        repo_index, name='repositories'),
)
