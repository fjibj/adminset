# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-02-28 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appconf', '0015_auto_20180228_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='app_console_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u63a7\u5236\u53f0URL'),
        ),
    ]
