import os
from git import *

from django.conf import settings


def get_repos():
    repos = [get_repo(dir) for dir in os.listdir(settings.REPOS_ROOT)]
    return [r for r in repos if not (r is None)]


def get_repo(name):
    repo_path = os.path.join(settings.REPOS_ROOT, name)
    if os.path.isdir(repo_path):
        try:
            return Repo(repo_path)
        except Exception:
            pass
    return None


def get_commit(name, commit):
    repo = get_repo(name)
    commit = repo.commit(commit)
    return commit
