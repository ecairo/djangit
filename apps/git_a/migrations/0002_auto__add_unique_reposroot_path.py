# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'ReposRoot', fields ['path']
        db.create_unique(u'git_a_reposroot', ['path'])


    def backwards(self, orm):
        # Removing unique constraint on 'ReposRoot', fields ['path']
        db.delete_unique(u'git_a_reposroot', ['path'])


    models = {
        u'git_a.reposroot': {
            'Meta': {'object_name': 'ReposRoot'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['git_a']