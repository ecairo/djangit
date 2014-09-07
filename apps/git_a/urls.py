from django.conf.urls import patterns, url

from apps.git_a.views import repo_index, repo_details, commit_details, object_details, archive_repo

urlpatterns = patterns(
    '',
    url(r'^(?P<repo_name>[\w_-]+)/tree/(?P<object_hash>[\w\d]+)/$',
        object_details, name='object_details'),

    url(r'^(?P<repo_name>[\w_-]+)/commit/(?P<commit_hash>[\w\d]+)/$',
        commit_details, name='commit_details'),

    url(r'^(?P<repo_name>[\w_-]+)/archive/$',
        archive_repo, name='repository_archive'),

    url(r'^(?P<repo_name>[\w_-]+)/(?P<tree_hash>[\w\d]+)/$',
        repo_details, name='repository_navigate'),

    url(r'^(?P<repo_name>[\w_-]+)$',
        repo_details, name='repository_index'),

    url(r'^$',
        repo_index, name='repositories'),
)
