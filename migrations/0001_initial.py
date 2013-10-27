# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topic'
        db.create_table('progress_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('progress', ['Topic'])

        # Adding model 'Tag'
        db.create_table('progress_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('progress', ['Tag'])

        # Adding model 'Task'
        db.create_table('progress_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress.Topic'], related_name='tasks')),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('progress', ['Task'])

        # Adding M2M table for field tags on 'Task'
        m2m_table_name = db.shorten_name('progress_task_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['progress.task'], null=False)),
            ('tag', models.ForeignKey(orm['progress.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'tag_id'])

        # Adding model 'Challenge'
        db.create_table('progress_challenge', (
            ('task_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, to=orm['progress.Task'], unique=True)),
        ))
        db.send_create_signal('progress', ['Challenge'])

        # Adding model 'Routine'
        db.create_table('progress_routine', (
            ('task_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, to=orm['progress.Task'], unique=True)),
        ))
        db.send_create_signal('progress', ['Routine'])

        # Adding model 'Portion'
        db.create_table('progress_portion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress.Challenge'], related_name='portions')),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('done_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('progress', ['Portion'])

        # Adding model 'Effort'
        db.create_table('progress_effort', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('routine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress.Routine'], related_name='efforts')),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 27, 0, 0))),
        ))
        db.send_create_signal('progress', ['Effort'])


    def backwards(self, orm):
        # Deleting model 'Topic'
        db.delete_table('progress_topic')

        # Deleting model 'Tag'
        db.delete_table('progress_tag')

        # Deleting model 'Task'
        db.delete_table('progress_task')

        # Removing M2M table for field tags on 'Task'
        db.delete_table(db.shorten_name('progress_task_tags'))

        # Deleting model 'Challenge'
        db.delete_table('progress_challenge')

        # Deleting model 'Routine'
        db.delete_table('progress_routine')

        # Deleting model 'Portion'
        db.delete_table('progress_portion')

        # Deleting model 'Effort'
        db.delete_table('progress_effort')


    models = {
        'progress.challenge': {
            'Meta': {'_ormbases': ['progress.Task'], 'object_name': 'Challenge'},
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['progress.Task']", 'unique': 'True'})
        },
        'progress.effort': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Effort'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 27, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'routine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress.Routine']", 'related_name': "'efforts'"})
        },
        'progress.portion': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Portion'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress.Challenge']", 'related_name': "'portions'"}),
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
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['progress.Tag']", 'related_name': "'tasks'"}),
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