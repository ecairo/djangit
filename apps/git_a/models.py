import os

from django.db import models


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
