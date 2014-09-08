from django.contrib import admin

from apps.git_a.models import ReposRoot, Repository


admin.site.register(ReposRoot)
admin.site.register(Repository)
