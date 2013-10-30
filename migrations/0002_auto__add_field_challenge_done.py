# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Challenge.done'
        db.add_column('progress_challenge', 'done',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Challenge.done'
        db.delete_column('progress_challenge', 'done')


    models = {
        'progress.challenge': {
            'Meta': {'_ormbases': ['progress.Task'], 'object_name': 'Challenge'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['progress.Task']", 'unique': 'True'})
        },
        'progress.effort': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Effort'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 30, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'routine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'efforts'", 'to': "orm['progress.Routine']"})
        },
        'progress.portion': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Portion'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'portions'", 'to': "orm['progress.Challenge']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'done_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'progress.routine': {
            'Meta': {'_ormbases': ['progress.Task'], 'object_name': 'Routine'},
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['progress.Task']", 'unique': 'True'})
        },
        'progress.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'progress.task': {
            'Meta': {'object_name': 'Task'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tasks'", 'to': "orm['progress.Tag']", 'symmetrical': 'False'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['progress.Topic']"}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        },
        'progress.topic': {
            'Meta': {'object_name': 'Topic'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['progress']