# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MileStone'
        db.create_table('Issues_milestone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('duedate', self.gf('django.db.models.fields.DateTimeField')()),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Depot.Repo'])),
            ('creater', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 23, 0, 0))),
        ))
        db.send_create_signal('Issues', ['MileStone'])

        # Adding unique constraint on 'MileStone', fields ['title', 'repo']
        db.create_unique('Issues_milestone', ['title', 'repo_id'])

        # Adding model 'IssueLabel'
        db.create_table('Issues_issuelabel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Depot.Repo'])),
        ))
        db.send_create_signal('Issues', ['IssueLabel'])

        # Adding unique constraint on 'IssueLabel', fields ['name', 'repo']
        db.create_unique('Issues_issuelabel', ['name', 'repo_id'])

        # Adding model 'Issue'
        db.create_table('Issues_issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 23, 0, 0))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 23, 0, 0))),
            ('commented', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 23, 0, 0))),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Issues.MileStone'], null=True, blank=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issuse_submitter', to=orm['auth.User'])),
            ('assigner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='issuse_assigner', null=True, to=orm['auth.User'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='opened', max_length=10)),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issuse_repo', to=orm['Depot.Repo'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal('Issues', ['Issue'])

        # Adding M2M table for field labels on 'Issue'
        db.create_table('Issues_issue_labels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issue', models.ForeignKey(orm['Issues.issue'], null=False)),
            ('issuelabel', models.ForeignKey(orm['Issues.issuelabel'], null=False))
        ))
        db.create_unique('Issues_issue_labels', ['issue_id', 'issuelabel_id'])

        # Adding model 'Comment'
        db.create_table('Issues_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 23, 0, 0))),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issue_comment', to=orm['Issues.Issue'])),
        ))
        db.send_create_signal('Issues', ['Comment'])


    def backwards(self, orm):
        # Removing unique constraint on 'IssueLabel', fields ['name', 'repo']
        db.delete_unique('Issues_issuelabel', ['name', 'repo_id'])

        # Removing unique constraint on 'MileStone', fields ['title', 'repo']
        db.delete_unique('Issues_milestone', ['title', 'repo_id'])

        # Deleting model 'MileStone'
        db.delete_table('Issues_milestone')

        # Deleting model 'IssueLabel'
        db.delete_table('Issues_issuelabel')

        # Deleting model 'Issue'
        db.delete_table('Issues_issue')

        # Removing M2M table for field labels on 'Issue'
        db.delete_table('Issues_issue_labels')

        # Deleting model 'Comment'
        db.delete_table('Issues_comment')


    models = {
        'Depot.repo': {
            'Meta': {'unique_together': "(('name', 'owner'),)", 'object_name': 'Repo'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 23, 0, 0)'}),
            'des': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'developers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'repo_developers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'issues_init': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'repo_managers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'reporters': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'repo_reporters'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Service.DeployService']", 'symmetrical': 'False'})
        },
        'Issues.comment': {
            'Meta': {'object_name': 'Comment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 23, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issue_comment'", 'to': "orm['Issues.Issue']"}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'Issues.issue': {
            'Meta': {'object_name': 'Issue'},
            'assigner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'issuse_assigner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'commented': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 23, 0, 0)'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 23, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['Issues.IssueLabel']", 'null': 'True', 'blank': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Issues.MileStone']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issuse_repo'", 'to': "orm['Depot.Repo']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'opened'", 'max_length': '10'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issuse_submitter'", 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 23, 0, 0)'})
        },
        'Issues.issuelabel': {
            'Meta': {'unique_together': "(('name', 'repo'),)", 'object_name': 'IssueLabel'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Depot.Repo']"})
        },
        'Issues.milestone': {
            'Meta': {'unique_together': "(('title', 'repo'),)", 'object_name': 'MileStone'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 23, 0, 0)'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'creater': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'duedate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Depot.Repo']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'Service.deployservice': {
            'Meta': {'object_name': 'DeployService'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 23, 0, 0)'}),
            'call_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'creater': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'deploy_key': ('django.db.models.fields.TextField', [], {}),
            'des': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'needwrite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_to': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Issues']