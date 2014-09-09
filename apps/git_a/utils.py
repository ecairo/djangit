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
    tree_index.sort()

    return tree_index


def get_commit(repo, commit_name):
    commit = repo.commit(commit_name)
    return commit
