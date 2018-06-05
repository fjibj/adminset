# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-11-24 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='\u8d1f\u8d23\u4eba\u59d3\u540d')),
                ('phone', models.CharField(max_length=50, verbose_name='\u8d1f\u8d23\u4eba\u624b\u673a')),
                ('qq', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u8d1f\u8d23\u4ebaQQ')),
                ('weChat', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u8d1f\u8d23\u4eba\u5fae\u4fe1')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='\u4ea7\u54c1\u7ebf\u540d\u79f0')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appconf.AppOwner', verbose_name='\u4ea7\u54c1\u7ebf\u8d1f\u8d23\u4eba')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('language_type', models.CharField(blank=True, choices=[('Java', 'Java'), ('PHP', 'PHP'), ('Python', 'Python'), ('C#', 'C#'), ('Html', 'Html'), ('Javascript', 'Javascript'), ('C/C++', 'C/C++'), ('Ruby', 'Ruby'), ('Other', 'Other')], max_length=30, null=True, verbose_name='\u8bed\u8a00\u7c7b\u578b')),
                ('app_type', models.CharField(blank=True, choices=[('Frontend', 'Frontend'), ('Middleware', 'Middleware'), ('Backend', 'Backend')], max_length=30, null=True, verbose_name='\u7a0b\u5e8f\u7c7b\u578b')),
                ('server_type', models.CharField(blank=True, choices=[('Tomcat', 'Tomcat'), ('Weblogic', 'Weblogic'), ('JETTY', 'JETTY'), ('Nginx', 'Nginx'), ('Gunicorn', 'Gunicorn'), ('Uwsgi', 'Uwsgi'), ('Apache', 'Apache'), ('IIS', 'IIS')], max_length=30, null=True, verbose_name='\u670d\u52a1\u5668\u7c7b\u578b')),
                ('app_arch', models.CharField(blank=True, choices=[('Django', 'Django'), ('Flask', 'Flask'), ('Tornado', 'Tornado'), ('Dubbo', 'Dubbo'), ('SSH', 'SSH'), ('Spring boot', 'Spring boot'), ('Spring cloud', 'Spring cloud'), ('Laravel', 'Laravel'), ('ThinkPHP', 'ThinkPHP'), ('Phalcon', 'Phalcon'), ('other', 'other')], max_length=30, null=True, verbose_name='\u7a0b\u5e8f\u6846\u67b6')),
                ('source_type', models.CharField(blank=True, choices=[('svn', 'svn'), ('git', 'git'), ('file', 'file')], max_length=255, verbose_name='\u6e90\u7c7b\u578b')),
                ('source_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u6e90\u5730\u5740')),
                ('appPath', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7a0b\u5e8f\u90e8\u7f72\u8def\u5f84')),
                ('configPath', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u914d\u7f6e\u6587\u4ef6\u8def\u5f84')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appconf.AppOwner', verbose_name='\u9879\u76ee\u8d1f\u8d23\u4eba')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appconf.Product', verbose_name='\u6240\u5c5e\u4ea7\u54c1\u7ebf')),
                ('serverList', models.ManyToManyField(blank=True, to='cmdb.Host', verbose_name='\u6240\u5728\u670d\u52a1\u5668')),
            ],
        ),
    ]
