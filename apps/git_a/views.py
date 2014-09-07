from django.http import HttpResponse
from django.shortcuts import render_to_response

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter

from apps.git_a.utils import *
from conf.settings.base import MEDIA_ROOT


def repo_index(request):
    repos = get_repos()
    return render_to_response('git_a/index.html', {'repos': repos})


def repo_details(request, repo_name, tree_hash=None):
    repo = get_repo(repo_name)

    tree_index = get_repo_index(repo, tree_hash)

    return render_to_response('git_a/repo.html', {
        'repo': repo,
        'tree_index': tree_index})


def commit_details(request, repo_name, commit_hash):
    return render_to_response('git_a/commit.html',
                              {'repo': get_repo(repo_name),
                               'commit': get_commit(repo_name, commit_hash)})


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
    return render_to_response('git_a/object_details.html',
                              {'object_data': object_data,
                               'selected_object': selected_object,
                               'repo': repo, })


def archive_repo(request, repo_name):
    repo = get_repo(repo_name)
    filename = "%s/%s.zip" % (MEDIA_ROOT, repo_name)

    response = HttpResponse(repo.archive(open(filename, 'w+')),
                            content_type='application/zip')

    response['Content-Disposition'] = 'attachment; filename="%s.zip"' % repo_name
    return response
