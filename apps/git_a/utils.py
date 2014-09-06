from os import listdir, path
from git import *

from django.http import Http404
from django.conf import settings


def get_repos():
    repos = [list_repos(repo_dir) for repo_dir in listdir(settings.REPOS_ROOT)]
    return [r for r in repos if not (r is None)]


def list_repos(name):
    repo_path = path.join(settings.REPOS_ROOT, name)
    if path.isdir(repo_path):
        try:
            return Repo(repo_path)
        except InvalidGitRepositoryError:
            return None
    return None


def get_repo(name):
    repo_path = path.join(settings.REPOS_ROOT, name)
    try:
        return Repo(repo_path)
    except InvalidGitRepositoryError:
        raise Http404
    except NoSuchPathError:
        raise Http404


def get_repo_index(repo, tree_hash):
    """
    """
    root_tree = repo.head.commit.tree
    selected_tree = root_tree
    if tree_hash:
        for tree in root_tree.list_traverse():
            if tree.hexsha == tree_hash:
                selected_tree = tree
                break

    tree_index = [x for x in selected_tree]
    tree_index.sort()

    return tree_index


def get_commit(name, commit):
    repo = get_repo(name)
    commit = repo.commit(commit)
    return commit
