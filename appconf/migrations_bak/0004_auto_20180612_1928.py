# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-12 11:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appconf', '0003_auto_20180612_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='develop_type',
        ),
        migrations.RemoveField(
            model_name='project',
            name='location',
        ),
        migrations.RemoveField(
            model_name='project',
            name='operator',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_type',
        ),
    ]
