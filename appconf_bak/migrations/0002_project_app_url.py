# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-04 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appconf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='app_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5e94\u7528URL'),
        ),
    ]