# -*- coding: utf-8 -*-

from os import listdir, path
from git import Repo, InvalidGitRepositoryError


def get_repos(repos_root):
    """
    Return a list with all valid git repositories
    within `repos_root` path.
    """
    repos = []
    for repo_dir in listdir(repos_root):
        repo_path = path.join(repos_root, repo_dir)
        if not path.isdir(repo_path):
            continue

        repo = get_repo_or_none(repo_path)
        if repo:
            repos.append(repo)
    return repos


def get_repo_or_none(repo_path):
    try:
        return Repo(repo_path)
    except InvalidGitRepositoryError:
        return None


def get_repo_index(repo, tree_hash=None):
    """
    Get all object in repository, or from specific tree
    """
    root_tree = repo.head.commit.tree
    selected_tree = root_tree
    if tree_hash:
        for tree in root_tree.list_traverse():
            if tree.hexsha == tree_hash:
                selected_tree = tree
                break

    tree_index = [x for x in selected_tree]
    tree_index.sort(cmp=compare_objects)

    return tree_index


def compare_objects(x, y):
    """
    Comparer to sort the folders first than files.
    """
    if x.type == y.type == 'blob' or x.type == y.type == 'tree':
        return cmp(x.name, y.name)

    if x.type == 'blob':
        return 1
    return -1


def get_commit(repo, commit_hash):
    """
    Get commit object from a repository and a commit hash
    """
    try:
        commit = repo.commit(commit_hash)
    except Exception:
        return None
    return commit


def get_object(repo, object_hash):
    """
    Get an git object
    """
    root_tree = repo.git_repo.head.commit.tree
    selected_object = None

    for blob_object in root_tree.list_traverse():
        if blob_object.hexsha == object_hash:
            selected_object = blob_object
            break

    return selected_object
