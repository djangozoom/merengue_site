# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        from django.conf import settings
        from johnny import cache
        from merengue.pluggable import register_plugin
        from merengue.pluggable.utils import install_plugin
        # Unpatch cache backend to disable johnny cache. Johny does weird things
        query_cache_backend = cache.get_backend()
        query_cache_backend.unpatch()
        from django.db import transaction
        for plug_dir in settings.DEMO_PLUGINS:
            plugin = register_plugin(plug_dir)
            plugin.installed = True
            plugin.active = True
            plugin.save()
            install_plugin(plugin)
            transaction.commit()

    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        
    }

    complete_apps = ['website']
