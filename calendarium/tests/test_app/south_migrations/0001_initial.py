# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DummyModel'
        db.create_table('test_app_dummymodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('test_app', ['DummyModel'])


    def backwards(self, orm):
        # Deleting model 'DummyModel'
        db.delete_table('test_app_dummymodel')


    models = {
        'test_app.dummymodel': {
            'Meta': {'object_name': 'DummyModel'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['test_app']