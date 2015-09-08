# -*- coding: utf-8 -*-

import os

from django.db import models
from django.utils.translation import ugettext as _

from .utils import get_repo_or_none, get_repos


class ReposRoot(models.Model):
    """
    Root directory to each repositories folder.
    """
    path = models.CharField(max_length=255, unique=True)

    def save(self):
        if not os.path.exists(self.path):
            raise Exception('Path do not exists')
        super(ReposRoot, self).save()

        # Add all repositories within new path
        repos = get_repos(self.path)
        for repo in repos:
            new_repo = Repository()
            new_repo.path = repo.working_dir
            # TODO: fix this patch to skip names with "."
            new_repo.name = repo.working_dir.split(os.sep)[-1].split('.')[0]
            new_repo.save()

    def __unicode__(self):
        return u'%s' % self.path


class Repository(models.Model):
    path = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100, verbose_name=_(u'Repo Name'))
    description = models.TextField(verbose_name=_('Description'),
                                   blank=True, null=True)
    public = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Repo')
        verbose_name_plural = _('Repos')

    def __unicode__(self):
        return u'%s' % self.name

    @property
    def git_repo(self):
        return get_repo_or_none(self.path)
