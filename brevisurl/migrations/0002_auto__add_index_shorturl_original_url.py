# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'ShortUrl', fields ['original_url']
        db.create_index('brevisurl_shorturl', ['original_url'])


    def backwards(self, orm):
        # Removing index on 'ShortUrl', fields ['original_url']
        db.delete_index('brevisurl_shorturl', ['original_url'])


    models = {
        'brevisurl.shorturl': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('original_url_hash', 'backend'),)", 'object_name': 'ShortUrl'},
            'backend': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'db_index': 'True'}),
            'original_url_hash': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'shortened_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['brevisurl']