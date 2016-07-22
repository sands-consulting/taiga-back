# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-29 10:36
from __future__ import unicode_literals

from django.db import migrations
from taiga.projects.history.services import get_instance_from_key


def forward_func(apps, schema_editor):
    HistoryEntry = apps.get_model("history", "HistoryEntry")
    db_alias = schema_editor.connection.alias
    for entry in HistoryEntry.objects.using(db_alias).all().iterator():
        instance = get_instance_from_key(entry.key)
        if type(instance) == apps.get_model("projects", "Project"):
            entry.project_id = instance.id
        else:
            entry.project_id = getattr(instance, 'project_id', None)
            entry.save()

    HistoryEntry.objects.using(db_alias).filter(project_id__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0010_historyentry_project'),
    ]

    operations = [
        migrations.RunPython(forward_func, atomic=False),
    ]