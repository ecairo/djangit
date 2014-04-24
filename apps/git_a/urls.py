from django.conf.urls import patterns, url

from apps.git_a.views import repo_index, repo_details, commit_details

urlpatterns = patterns(
    '',
    url(r'^(?P<repo_name>[\w_-]+)/commit/(?P<commit_hash>[\w\d]+)/$', commit_details, name='git_admin_commit_details'),
    url(r'^(?P<repo_name>[\w_-]+)/$', repo_details, name='git_admin_repository'),
    url(r'^$', repo_index, name='git_admin_repositories'),
)
