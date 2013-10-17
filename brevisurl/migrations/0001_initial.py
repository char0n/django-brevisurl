# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings


MAX_LEN_ORI_URL = getattr(settings, 'BREVISURL_LOCAL_BACKEND_TOKEN_LENGTH', 200)


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShortUrl'
        db.create_table('brevisurl_shorturl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_url', self.gf('django.db.models.fields.URLField')(max_length=MAX_LEN_ORI_URL)),
            ('original_url_hash', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('shortened_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('backend', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('brevisurl', ['ShortUrl'])

        # Adding unique constraint on 'ShortUrl', fields ['original_url_hash', 'backend']
        db.create_unique('brevisurl_shorturl', ['original_url_hash', 'backend'])


    def backwards(self, orm):
        # Removing unique constraint on 'ShortUrl', fields ['original_url_hash', 'backend']
        db.delete_unique('brevisurl_shorturl', ['original_url_hash', 'backend'])

        # Deleting model 'ShortUrl'
        db.delete_table('brevisurl_shorturl')


    models = {
        'brevisurl.shorturl': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('original_url_hash', 'backend'),)", 'object_name': 'ShortUrl'},
            'backend': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_url': ('django.db.models.fields.URLField', [], {'max_length': str(MAX_LEN_ORI_URL)}),
            'original_url_hash': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'shortened_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['brevisurl']
