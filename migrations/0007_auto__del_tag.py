# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('progress_tag')

        # Removing M2M table for field tags on 'Task'
        db.delete_table(db.shorten_name('progress_task_tags'))


    def backwards(self, orm):
        # Adding model 'Tag'
        db.create_table('progress_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('progress', ['Tag'])

        # Adding M2M table for field tags on 'Task'
        m2m_table_name = db.shorten_name('progress_task_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['progress.task'], null=False)),
            ('tag', models.ForeignKey(orm['progress.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'tag_id'])


    models = {
        'progress.challenge': {
            'Meta': {'_ormbases': ['progress.Task'], 'object_name': 'Challenge'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['progress.Task']", 'unique': 'True', 'primary_key': 'True'})
        },
        'progress.effort': {
            'Meta': {'object_name': 'Effort', 'ordering': "('-date',)"},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'routine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress.Routine']", 'related_name': "'efforts'"})
        },
        'progress.portion': {
            'Meta': {'object_name': 'Portion', 'ordering': "('_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress.Challenge']", 'related_name': "'portions'"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'done_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'OPEN'"})
        },
        'progress.routine': {
            'Meta': {'_ormbases': ['progress.Task'], 'object_name': 'Routine'},
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['progress.Task']", 'unique': 'True', 'primary_key': 'True'})
        },
        'progress.task': {
            'Meta': {'object_name': 'Task'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress.Topic']", 'related_name': "'tasks'"}),
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