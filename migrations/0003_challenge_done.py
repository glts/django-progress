# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for challenge in orm.Challenge.objects.all():
            if all([portion.done for portion in challenge.portions.all()]):
                challenge.done = True
                challenge.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        'progress.challenge': {
            'Meta': {'object_name': 'Challenge', '_ormbases': ['progress.Task']},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['progress.Task']", 'unique': 'True', 'primary_key': 'True'})
        },
        'progress.effort': {
            'Meta': {'object_name': 'Effort', 'ordering': "('-date',)"},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 30, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'routine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'efforts'", 'to': "orm['progress.Routine']"})
        },
        'progress.portion': {
            'Meta': {'object_name': 'Portion', 'ordering': "('_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'portions'", 'to': "orm['progress.Challenge']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'done_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'progress.routine': {
            'Meta': {'object_name': 'Routine', '_ormbases': ['progress.Task']},
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['progress.Task']", 'unique': 'True', 'primary_key': 'True'})
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
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['progress.Tag']", 'symmetrical': 'False', 'related_name': "'tasks'"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['progress.Topic']"}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'progress.topic': {
            'Meta': {'object_name': 'Topic'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['progress']
    symmetrical = True
