# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-30 06:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appconf', '0011_auto_20180130_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AlterField(
            model_name='project',
            name='server_type',
            field=models.CharField(blank=True, choices=[('Tomcat', 'Tomcat'), ('Weblogic9i', 'Weblogic9i'), ('Weblogic11g', 'Weblogic11g'), ('JETTY', 'JETTY'), ('Nginx', 'Nginx'), ('Gunicorn', 'Gunicorn'), ('Uwsgi', 'Uwsgi'), ('Apache', 'Apache'), ('IIS', 'IIS'), ('Was6', 'Was6'), ('Was7', 'Was7')], max_length=30, null=True, verbose_name='\u670d\u52a1\u5668\u7c7b\u578b'),
        ),
    ]