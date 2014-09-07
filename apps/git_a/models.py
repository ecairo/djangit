import os

from django.db import models
from django.utils.translation import ugettext as _

from .utils import get_repo


class ReposRoot(models.Model):
    """
    Root directory to each repositories folder.
    """
    path = models.CharField(max_length=255, unique=True)

    def save(self):
        if not os.path.exists(self.path):
            raise Exception('Path do not exists')
        super(ReposRoot, self).save()

    def __unicode__(self):
        return u'%s' % self.path


class Repo(models.Model):
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

    def repo(self):
        return get_repo(self.path)
