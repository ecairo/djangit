# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from apps.git_a.views import RepositoryView, commit_details,\
    object_details, archive_repo, get_file

urlpatterns = patterns(
    '',
    url(r'^(?P<repo_name>[\w_-]+)/tree/(?P<object_hash>[\w\d]+)/$',
        object_details, name='object_details'),

    url(r'^(?P<repo_name>[\w_-]+)/commit/(?P<commit_hash>[\w\d]+)/$',
        commit_details, name='commit_details'),

    url(r'^(?P<repo_name>[\w_-]+)/archive/$',
        archive_repo, name='repository_archive'),

    url(r'^(?P<repo_name>[\w_-]+)/file/(?P<file_hash>[\w\d]+)/$',
        get_file, name='file_download'),

    url(r'^(?P<repo_name>[\w_-]+)/(?P<tree_hash>[\w\d]+)/$',
        RepositoryView.as_view(),
        name='repository_navigate'),

    url(r'^(?P<repo_name>[\w_-]+)$',
        RepositoryView.as_view(),
        name='repository_index'),

    url(r'^$',
        TemplateView.as_view(template_name='git_a/index.html'),
        name='repositories'),
)
