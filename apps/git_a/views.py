# -*- coding: utf-8 -*-

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, DiffLexer, TextLexer
from pygments.formatters import HtmlFormatter

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import DetailView

from .utils import get_repo_index, get_commit, get_object
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
        repo = context['repo'].git_repo
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
    """
    Get commit object details.
    """
    repo = get_repo(repo_name)
    commit = get_commit(repo.git_repo, commit_hash)
    if not commit:
        raise Http404()
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

        file_raw = repo.git_repo.git.diff(b_file, a_file)
        file_diff = highlight(file_raw, DiffLexer(), HtmlFormatter())
        diff_data.append((mfile.a_blob.name, file_diff))

    return render_to_response('git_a/commit.html', {
        'repo': repo,
        'commit': commit,
        'diff_data': diff_data},
        context_instance=RequestContext(request))


def object_details(request, repo_name, object_hash):
    """
    Get an object details
    """
    repo = get_repo(repo_name)
    selected_object = get_object(repo, object_hash)

    if not selected_object:
        raise Http404()

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
    """
    Return result from git command archive.
    i.e.: `git archive master --format=zip > repo_name.zip`
    """
    repo = get_repo(repo_name)
    resp = HttpResponse(repo.git_repo.git.archive('master', '--format=zip'),
                        content_type='application/zip')
    resp['Content-Disposition'] = 'attachment; filename="%s.zip"' % repo_name
    return resp


def get_file(request, repo_name, file_hash):
    """
    Search a file from it hash and if exists return it attached
    """
    repo = get_repo(repo_name)
    sel_file = get_object(repo, file_hash)

    if not sel_file:
        raise Http404()

    resp = HttpResponse(sel_file.data_stream.read(), content_type='text/plain')
    resp['Content-Disposition'] = 'attachment; filename="%s"' % sel_file.name
    return resp


def get_repo(repo_name):
    """
    Lookup for a Repository object in DB
    """
    return get_object_or_404(Repository, name=repo_name)
