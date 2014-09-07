# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReposRoot'
        db.create_table(u'git_a_reposroot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'git_a', ['ReposRoot'])


    def backwards(self, orm):
        # Deleting model 'ReposRoot'
        db.delete_table(u'git_a_reposroot')


    models = {
        u'git_a.reposroot': {
            'Meta': {'object_name': 'ReposRoot'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['git_a']