# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PullRequest'
        db.create_table('Pull_pullrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Depot.Repo'])),
            ('requester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('from_head', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('to_head', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('commit_msg', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 23, 0, 0))),
            ('create_commit_hexsha', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('merged_commit_hexsha', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('stat', self.gf('django.db.models.fields.CharField')(default='open', max_length=10)),
            ('assigner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assigner', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('Pull', ['PullRequest'])


    def backwards(self, orm):
        # Deleting model 'PullRequest'
        db.delete_table('Pull_pullrequest')


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
        'Pull.pullrequest': {
            'Meta': {'object_name': 'PullRequest'},
            'assigner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assigner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'commit_msg': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'create_commit_hexsha': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 23, 0, 0)'}),
            'from_head': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merged_commit_hexsha': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Depot.Repo']"}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'stat': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '10'}),
            'to_head': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['Pull']