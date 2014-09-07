from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, DiffLexer
from pygments.formatters import HtmlFormatter

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.git_a.utils import *


def repo_index(request):
    return render_to_response('git_a/index.html',
                              context_instance=RequestContext(request))


def repo_details(request, repo_name, tree_hash=None):
    repo = get_repo(repo_name)

    tree_index = get_repo_index(repo, tree_hash)

    diff_data = []
    if repo.is_dirty():
        modified_files = repo.git.diff_files('--name-only').split('\n')
        for mfile in modified_files:
            file_raw = repo.git.diff(mfile)
            file_diff = highlight(file_raw, DiffLexer(), HtmlFormatter())
            diff_data.append((mfile, file_diff))

    return render_to_response('git_a/repo.html', {
        'repo': repo,
        'diff_data': diff_data,
        'tree_index': tree_index,
        'commits': repo.iter_commits('master')},
        context_instance=RequestContext(request))


def commit_details(request, repo_name, commit_hash):
    return render_to_response('git_a/commit.html', {
        'repo': get_repo(repo_name),
        'commit': get_commit(repo_name, commit_hash)},
        context_instance=RequestContext(request))


def object_details(request, repo_name, object_hash):
    """
    """
    repo = get_repo(repo_name)
    root_tree = repo.head.commit.tree
    selected_object = None
    for blob_object in root_tree.list_traverse():
        if blob_object.hexsha == object_hash:
            selected_object = blob_object
            break

    raw_data = selected_object.data_stream.read()
    lexer = guess_lexer_for_filename(selected_object.name, raw_data)
    object_data = highlight(raw_data, lexer, HtmlFormatter())

    return render_to_response('git_a/object_details.html', {
        'object_data': object_data,
        'selected_object': selected_object,
        'repo': repo},
        context_instance=RequestContext(request))


def archive_repo(request, repo_name):
    repo = get_repo(repo_name)
    resp = HttpResponse(repo.git.archive('master', '--format=zip'),
                        content_type='application/zip')
    resp['Content-Disposition'] = 'attachment; filename="%s.zip"' % repo_name
    return resp
