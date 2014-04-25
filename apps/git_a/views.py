from django.shortcuts import render_to_response

from apps.git_a.utils import *


def repo_index(request, template_name='git_a/index.html'):
    return render_to_response(template_name, {'repos': get_repos()})


def repo_details(request, repo_name, template_name='git_a/repo.html'):
    return render_to_response(template_name, {'repo': get_repo(repo_name)})


def commit_details(request, repo_name, commit_hash, template_name='git_a/commit.html'):
    return render_to_response(template_name, {'repo': get_repo(repo_name),
                                              'commit': get_commit(repo_name, commit_hash)})
