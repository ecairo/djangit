from apps.git_a.utils import get_repos


def get_repositories(request):
    return {'repos': get_repos()}
