import os

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, DiffLexer, TextLexer
from pygments.formatters import HtmlFormatter

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import DetailView

from .utils import get_repo_index, get_commit
from .models import Repository


class RepositoryView(DetailView):
    """
    Repository view
    """
    model = Repository
    template_name = 'git_a/repo.html'
    context_object_name = 'repo'
    slug_field = 'name'
    slug_url_kwarg = 'repo_name'

    def get_context_data(self, **kwargs):
        context = super(RepositoryView, self).get_context_data(**kwargs)
        repo = context['repo'].repo
        tree_hash = self.kwargs.get('tree_hash', None)
        tree_index = get_repo_index(repo, tree_hash)

        diff_data = []
        if repo.is_dirty():
            mod_files = repo.git.diff_files('--name-only').split('\n')
            for mfile in mod_files:
                file_raw = repo.git.diff(mfile)
                file_diff = highlight(file_raw, DiffLexer(), HtmlFormatter())
                diff_data.append((mfile, file_diff))
        context['diff_data'] = diff_data
        context['tree_index'] = tree_index
        context['commits'] = repo.iter_commits('master')
        return context


def commit_details(request, repo_name, commit_hash):
    repo = get_repo(repo_name)
    commit = get_commit(repo, commit_hash)
    diff_data = []
    parents = commit.parents

    # Compare diff against first parent
    commit_files = commit.diff(parents[0]) if len(parents) else []
    for mfile in commit_files:
        a_file = mfile.a_blob
        b_file = mfile.b_blob

        # TODO: Compare new files and deleted
        if not mfile.a_mode or not mfile.b_mode:
            continue

        file_raw = repo.git.diff(a_file, b_file)
        file_diff = highlight(file_raw, DiffLexer(), HtmlFormatter())
        diff_data.append((mfile.a_blob.name, file_diff))

    return render_to_response('git_a/commit.html', {
        'repo': repo,
        'commit': commit,
        'diff_data': diff_data},
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
    try:
        lexer = guess_lexer_for_filename(selected_object.name, raw_data)
    except Exception:
        lexer = TextLexer()
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


def get_repo(repo_name):
    return get_object_or_404(Repository, name=repo_name).repo
