# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Portion.description'
        db.alter_column('progress_portion', 'description', self.gf('django.db.models.fields.CharField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Portion.description'
        db.alter_column('progress_portion', 'description', self.gf('django.db.models.fields.CharField')(max_length=40))

    models = {
        'progress.challenge': {
            'Meta': {'_ormbases': ['progress.Task'], 'object_name': 'Challenge'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['progress.Task']"})
        },
        'progress.effort': {
            'Meta': {'object_name': 'Effort', 'ordering': "('-date',)"},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'routine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'efforts'", 'to': "orm['progress.Routine']"})
        },
        'progress.portion': {
            'Meta': {'object_name': 'Portion', 'ordering': "('_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'portions'", 'to': "orm['progress.Challenge']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'done_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'OPEN'", 'max_length': '10'})
        },
        'progress.routine': {
            'Meta': {'_ormbases': ['progress.Task'], 'object_name': 'Routine'},
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['progress.Task']"})
        },
        'progress.task': {
            'Meta': {'object_name': 'Task'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['progress.Topic']"}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'progress.topic': {
            'Meta': {'object_name': 'Topic'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['progress']