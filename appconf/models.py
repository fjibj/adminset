#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from cmdb.models import Host


class AppOwner(models.Model):
    name = models.CharField(u"负责人姓名", max_length=50, unique=True, null=False, blank=False)
    phone = models.CharField(u"负责人手机", max_length=50, null=False, blank=False)
    qq = models.CharField(u"负责人QQ", max_length=100, null=True, blank=True)
    weChat = models.CharField(u"负责人微信", max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(u"产品线名称", max_length=50, unique=True, null=False, blank=False)
    owner = models.ForeignKey(
        AppOwner, verbose_name=u"产品线负责人",
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.name


class Project(models.Model):

    LANGUAGE_TYPES = (
        ("Java", "Java"),
        ("PHP", "PHP"),
        ("Python", "Python"),
        ("C#", "C#"),
        ("Html", "Html"),
        ("Javascript", "Javascript"),
        ("C/C++", "C/C++"),
        ("Ruby", "Ruby"),
        ("Other", "Other"),
    )

    APP_TYPE = (
        ("Frontend", "Frontend"),
        ("Middleware", "Middleware"),
        ("Backend", "Backend"),
    )

    SERVER_TYPE = (
        ("Tomcat", "Tomcat"),
        ("Weblogic9i", "Weblogic9i"),
        ("Weblogic11g", "Weblogic11g"),
        ("JETTY", "JETTY"),
        ("Nginx", "Nginx"),
        ("Gunicorn", "Gunicorn"),
        ("Uwsgi", "Uwsgi"),
        ("Apache", "Apache"),
        ("IIS", "IIS"),
        ("Was6", "Was6"),
        ("Was7", "Was7"),
    )

    APP_ARCH = (
        ("Django", "Django"),
        ("Flask", "Flask"),
        ("Tornado", "Tornado"),
        ("Dubbo", "Dubbo"),
        ("SSH", "SSH"),
        ("Spring boot", "Spring boot"),
        ("Spring cloud", "Spring cloud"),
        ("Laravel", "Laravel"),
        ("ThinkPHP", "ThinkPHP"),
        ("Phalcon", "Phalcon"),
        ("other", "other"),
    )

    SOURCE_TYPE = (
        ("svn", "svn"),
        ("git", "git"),
        ("file", "file"),
    )

    name = models.CharField(u"项目名称", max_length=50, null=False, blank=False)
    app_url = models.CharField(u"应用URL", max_length=255, null=True, blank=True)
    app_user = models.CharField(u"登录用户名", max_length=255, null=True, blank=True)
    app_password = models.CharField(u"登录密码", max_length=255, null=True, blank=True)
    os_user = models.CharField(u"操作系统用户名", max_length=255, null=True, blank=True)
    os_password = models.CharField(u"操作系统密码", max_length=255, null=True, blank=True)
    console_url = models.CharField(u"控制台URL", max_length=255, null=True, blank=True)
    app_console_user = models.CharField(u"控制台用户名", max_length=255, null=True, blank=True)
    app_console_password = models.CharField(u"控制台密码", max_length=255, null=True, blank=True)
    db_user = models.CharField(u"数据库用户名", max_length=255, null=True, blank=True)
    db_password = models.CharField(u"数据库密码", max_length=255, null=True, blank=True)
    db_info = models.CharField(u"数据库信息", max_length=255, null=True, blank=True)
    province = models.CharField(u"省份信息", max_length=255, null=True, blank=True)
    operator = models.CharField(u"运营商信息", max_length=255, null=True, blank=True)
    location = models.CharField(u"位置信息", max_length=255, null=True, blank=True)
    project_type = models.CharField(u"项目类型", max_length=255, null=True, blank=True)
    develop_type = models.CharField(u"环境类型", max_length=255, null=True, blank=True)
    language_type = models.CharField(u"语言类型", choices=LANGUAGE_TYPES, max_length=30, null=True, blank=True)
    app_type = models.CharField(u"程序类型", choices=APP_TYPE, max_length=30, null=True, blank=True)
    server_type = models.CharField(u"服务器类型", choices=SERVER_TYPE, max_length=30, null=True, blank=True)
    jmx_port = models.CharField(u"JMX服务端口", max_length=255, null=True, blank=False,default='1')
    app_arch = models.CharField(u"程序框架", choices=APP_ARCH, max_length=30, null=True, blank=True)
    source_type = models.CharField(max_length=255, choices=SOURCE_TYPE, verbose_name=u"源类型", null=True,blank=True)
    source_address = models.CharField(max_length=255, verbose_name=u"机器地址", null=False, blank=False)
    appPath = models.CharField(u"程序部署路径", max_length=255, null=True, blank=True)
    configPath = models.CharField(u"日志文件路径", max_length=255, null=True, blank=True)
    product = models.ForeignKey(
            Product,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"所属中心"
    )
    owner = models.ForeignKey(
            AppOwner,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"项目负责人"
    )
    serverList = models.ManyToManyField(
            Host,
            blank=True,
            verbose_name=u"所在服务器"
    )
