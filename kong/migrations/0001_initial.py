
from south.db import db
from django.db import models
from kong.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'TestResult'
        db.create_table('kong_testresult', (
            ('id', models.AutoField(primary_key=True)),
            ('test', models.ForeignKey(orm.Test, related_name='test_results')),
            ('site', models.ForeignKey(orm.Site, related_name='test_results')),
            ('run_date', models.DateTimeField(default=datetime.datetime.now)),
            ('duration', models.IntegerField(null=True)),
            ('succeeded', models.BooleanField()),
            ('content', models.TextField()),
        ))
        db.send_create_signal('kong', ['TestResult'])
        
        # Adding model 'Server'
        db.create_table('kong_server', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=80, blank=True)),
            ('slug', models.SlugField()),
            ('hostname', models.CharField(max_length=100)),
            ('internalip', models.IPAddressField(null=True, blank=True)),
            ('externalip', models.IPAddressField(null=True, blank=True)),
        ))
        db.send_create_signal('kong', ['Server'])
        
        # Adding model 'HostedSite'
        db.create_table('kong_hostedsite', (
            ('site_ptr', models.OneToOneField(orm['kong.Site'])),
            ('servername', models.CharField(default='example.com', max_length=100)),
            ('maxclients', models.IntegerField(default=30, null=True, blank=True)),
            ('wsgi_processes', models.IntegerField(default=5, null=True, blank=True)),
            ('wsgi_max_requests', models.IntegerField(default=500, null=True, blank=True)),
            ('serveradmin', models.CharField(max_length=100, null=True, blank=True)),
            ('mediaserver', models.CharField(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('kong', ['HostedSite'])
        
        # Adding model 'Client'
        db.create_table('kong_client', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=100, blank=True)),
            ('slug', models.SlugField(blank=True)),
            ('phone', USmodels.PhoneNumberField(blank=True)),
            ('email', models.EmailField(blank=True)),
            ('contact', models.CharField(max_length=100, blank=True)),
        ))
        db.send_create_signal('kong', ['Client'])
        
        # Adding model 'Site'
        db.create_table('kong_site', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=80, blank=True)),
            ('slug', models.SlugField()),
            ('type', models.ForeignKey(orm.Type, related_name='sites')),
            ('client', models.ForeignKey(orm.Client, related_name='sites', null=True, blank=True)),
            ('settings', models.CharField(max_length=80)),
            ('pythonpath', models.CharField(default='/home/code.django-1.0', max_length=255)),
            ('is_live', models.BooleanField(default=False)),
        ))
        db.send_create_signal('kong', ['Site'])
        
        # Adding model 'Alias'
        db.create_table('kong_alias', (
            ('id', models.AutoField(primary_key=True)),
            ('site', models.ForeignKey(orm.HostedSite, related_name="aliases")),
            ('url', models.CharField(max_length=100)),
        ))
        db.send_create_signal('kong', ['Alias'])
        
        # Adding model 'Test'
        db.create_table('kong_test', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=250)),
            ('slug', models.SlugField(blank=True)),
            ('body', models.TextField()),
        ))
        db.send_create_signal('kong', ['Test'])
        
        # Adding model 'DeployTarget'
        db.create_table('kong_deploytarget', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=250)),
            ('slug', models.SlugField(blank=True)),
            ('is_active', models.BooleanField()),
            ('last_deployed', models.DateTimeField()),
        ))
        db.send_create_signal('kong', ['DeployTarget'])
        
        # Adding model 'Type'
        db.create_table('kong_type', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=40)),
            ('slug', models.SlugField(blank=True)),
        ))
        db.send_create_signal('kong', ['Type'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'TestResult'
        db.delete_table('kong_testresult')
        
        # Deleting model 'Server'
        db.delete_table('kong_server')
        
        # Deleting model 'HostedSite'
        db.delete_table('kong_hostedsite')
        
        # Deleting model 'Client'
        db.delete_table('kong_client')
        
        # Deleting model 'Site'
        db.delete_table('kong_site')
        
        # Deleting model 'Alias'
        db.delete_table('kong_alias')
        
        # Deleting model 'Test'
        db.delete_table('kong_test')
        
        # Deleting model 'DeployTarget'
        db.delete_table('kong_deploytarget')
        
        # Deleting model 'Type'
        db.delete_table('kong_type')
        
    
    
    models = {
        'kong.testresult': {
            'Meta': {'ordering': "('-run_date',)"},
            'content': ('models.TextField', [], {}),
            'duration': ('models.IntegerField', [], {'null': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'run_date': ('models.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'site': ('models.ForeignKey', ["orm['kong.Site']"], {'related_name': "'test_results'"}),
            'succeeded': ('models.BooleanField', [], {}),
            'test': ('models.ForeignKey', ["orm['kong.Test']"], {'related_name': "'test_results'"})
        },
        'kong.server': {
            'clients': ('ManyToManyField_NoSyncdb', ["orm['kong.HostedSite']"], {'db_table': "'kong_hostedsite_on_servers'"}),
            'externalip': ('models.IPAddressField', [], {'null': 'True', 'blank': 'True'}),
            'hostname': ('models.CharField', [], {'max_length': '100'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'internalip': ('models.IPAddressField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {})
        },
        'kong.hostedsite': {
            'Meta': {'_bases': ['kong.models.Site']},
            'maxclients': ('models.IntegerField', [], {'default': '30', 'null': 'True', 'blank': 'True'}),
            'mediaserver': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'on_servers': ('models.ManyToManyField', ["orm['kong.Server']"], {'related_name': '"sites"', 'null': 'True', 'blank': 'True'}),
            'serveradmin': ('models.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'servername': ('models.CharField', [], {'default': "'example.com'", 'max_length': '100'}),
            'site_ptr': ('models.OneToOneField', ["orm['kong.Site']"], {}),
            'wsgi_max_requests': ('models.IntegerField', [], {'default': '500', 'null': 'True', 'blank': 'True'}),
            'wsgi_processes': ('models.IntegerField', [], {'default': '5', 'null': 'True', 'blank': 'True'})
        },
        'kong.client': {
            'contact': ('models.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email': ('models.EmailField', [], {'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone': ('USmodels.PhoneNumberField', [], {'blank': 'True'}),
            'slug': ('models.SlugField', [], {'blank': 'True'})
        },
        'kong.site': {
            'client': ('models.ForeignKey', ["orm['kong.Client']"], {'related_name': "'sites'", 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_live': ('models.BooleanField', [], {'default': 'False'}),
            'name': ('models.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'pythonpath': ('models.CharField', [], {'default': "'/home/code.django-1.0'", 'max_length': '255'}),
            'settings': ('models.CharField', [], {'max_length': '80'}),
            'slug': ('models.SlugField', [], {}),
            'type': ('models.ForeignKey', ["orm['kong.Type']"], {'related_name': "'sites'"})
        },
        'kong.alias': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'site': ('models.ForeignKey', ["orm['kong.HostedSite']"], {'related_name': '"aliases"'}),
            'url': ('models.CharField', [], {'max_length': '100'})
        },
        'kong.test': {
            'body': ('models.TextField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '250'}),
            'sites': ('models.ManyToManyField', ["orm['kong.Site']"], {'related_name': "'tests'", 'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'blank': 'True'}),
            'types': ('models.ManyToManyField', ["orm['kong.Type']"], {'related_name': "'tests'", 'null': 'True', 'blank': 'True'})
        },
        'kong.deploytarget': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('models.BooleanField', [], {}),
            'last_deployed': ('models.DateTimeField', [], {}),
            'name': ('models.CharField', [], {'max_length': '250'}),
            'servers': ('models.ManyToManyField', ["orm['kong.Server']"], {}),
            'slug': ('models.SlugField', [], {'blank': 'True'})
        },
        'kong.type': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '40'}),
            'slug': ('models.SlugField', [], {'blank': 'True'})
        }
    }
    
    complete_apps = ['kong']
