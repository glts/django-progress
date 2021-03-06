# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Portion.done'
        db.delete_column('progress_portion', 'done')


    def backwards(self, orm):
        # Adding field 'Portion.done'
        db.add_column('progress_portion', 'done',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        'progress.challenge': {
            'Meta': {'_ormbases': ['progress.Task'], 'object_name': 'Challenge'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['progress.Task']", 'primary_key': 'True', 'unique': 'True'})
        },
        'progress.effort': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Effort'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 15, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'routine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress.Routine']", 'related_name': "'efforts'"})
        },
        'progress.portion': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Portion'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress.Challenge']", 'related_name': "'portions'"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'done_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'OPEN'", 'max_length': '10'})
        },
        'progress.routine': {
            'Meta': {'_ormbases': ['progress.Task'], 'object_name': 'Routine'},
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['progress.Task']", 'primary_key': 'True', 'unique': 'True'})
        },
        'progress.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'progress.task': {
            'Meta': {'object_name': 'Task'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['progress.Tag']", 'symmetrical': 'False', 'related_name': "'tasks'"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress.Topic']", 'related_name': "'tasks'"}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        },
        'progress.topic': {
            'Meta': {'object_name': 'Topic'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['progress']