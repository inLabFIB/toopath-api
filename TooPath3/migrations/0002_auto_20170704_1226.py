# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 10:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TooPath3', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actuallocation',
            old_name='locations',
            new_name='point',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='locations',
            new_name='actual_location',
        ),
        migrations.RenameField(
            model_name='routelocation',
            old_name='locations',
            new_name='point',
        ),
    ]
