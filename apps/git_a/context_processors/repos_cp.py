from apps.git_a.models import Repository


def get_repositories(request):
    repos = [x for x in Repository.objects.all()]
    return {'repos': repos}
