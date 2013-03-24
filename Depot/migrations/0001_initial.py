# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Repo'
        db.create_table('Depot_repo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('des', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 23, 0, 0))),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('issues_init', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Depot', ['Repo'])

        # Adding unique constraint on 'Repo', fields ['name', 'owner']
        db.create_unique('Depot_repo', ['name', 'owner_id'])

        # Adding M2M table for field services on 'Repo'
        db.create_table('Depot_repo_services', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repo', models.ForeignKey(orm['Depot.repo'], null=False)),
            ('deployservice', models.ForeignKey(orm['Service.deployservice'], null=False))
        ))
        db.create_unique('Depot_repo_services', ['repo_id', 'deployservice_id'])

        # Adding M2M table for field managers on 'Repo'
        db.create_table('Depot_repo_managers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repo', models.ForeignKey(orm['Depot.repo'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('Depot_repo_managers', ['repo_id', 'user_id'])

        # Adding M2M table for field developers on 'Repo'
        db.create_table('Depot_repo_developers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repo', models.ForeignKey(orm['Depot.repo'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('Depot_repo_developers', ['repo_id', 'user_id'])

        # Adding M2M table for field reporters on 'Repo'
        db.create_table('Depot_repo_reporters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repo', models.ForeignKey(orm['Depot.repo'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('Depot_repo_reporters', ['repo_id', 'user_id'])

        # Adding model 'BranchPermission'
        db.create_table('Depot_branchpermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Depot.Repo'], unique=True)),
            ('branch', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('Depot', ['BranchPermission'])

        # Adding unique constraint on 'BranchPermission', fields ['repo', 'branch']
        db.create_unique('Depot_branchpermission', ['repo_id', 'branch'])

        # Adding M2M table for field users on 'BranchPermission'
        db.create_table('Depot_branchpermission_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('branchpermission', models.ForeignKey(orm['Depot.branchpermission'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('Depot_branchpermission_users', ['branchpermission_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'BranchPermission', fields ['repo', 'branch']
        db.delete_unique('Depot_branchpermission', ['repo_id', 'branch'])

        # Removing unique constraint on 'Repo', fields ['name', 'owner']
        db.delete_unique('Depot_repo', ['name', 'owner_id'])

        # Deleting model 'Repo'
        db.delete_table('Depot_repo')

        # Removing M2M table for field services on 'Repo'
        db.delete_table('Depot_repo_services')

        # Removing M2M table for field managers on 'Repo'
        db.delete_table('Depot_repo_managers')

        # Removing M2M table for field developers on 'Repo'
        db.delete_table('Depot_repo_developers')

        # Removing M2M table for field reporters on 'Repo'
        db.delete_table('Depot_repo_reporters')

        # Deleting model 'BranchPermission'
        db.delete_table('Depot_branchpermission')

        # Removing M2M table for field users on 'BranchPermission'
        db.delete_table('Depot_branchpermission_users')


    models = {
        'Depot.branchpermission': {
            'Meta': {'unique_together': "(('repo', 'branch'),)", 'object_name': 'BranchPermission'},
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Depot.Repo']", 'unique': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
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

    complete_apps = ['Depot']