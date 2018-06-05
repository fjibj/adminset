# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-10 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appconf', '0004_auto_20180104_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='app_password',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u767b\u5f55\u5bc6\u7801'),
        ),
        migrations.AlterField(
            model_name='project',
            name='app_user',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u767b\u5f55\u7528\u6237\u540d'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u6240\u5c5e\u4ea7\u54c1'),
        ),
        migrations.AlterField(
            model_name='project',
            name='source_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u673a\u5668\u5730\u5740'),
        ),
    ]
