#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import system, manage, jmx
from cmdb  import api, idc, asset, group
import api


urlpatterns = [
    url(r'^asset/get/cpu/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_cpu, name='get_cpu'),
    url(r'^asset/get/mem/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_mem, name='get_mem'),
    url(r'^asset/get/disk/(?P<hostname>.+)/(?P<timing>\d+)/(?P<partition>\d+)/$', system.get_disk, name='get_disk'),
    url(r'^asset/get/net/(?P<hostname>.+)/(?P<timing>\d+)/(?P<net_id>\d+)/$', system.get_net, name='get_net'),
    url(r'^asset/get/value/(?P<hostname>.+)/$', system.get_value, name='get_value'),
    url(r'^asset/(?P<hostname>.+)/(?P<timing>\d+)/$', system.host_info, name='host_info'),
    url(r'^system/$', system.index, name='monitor'),    
    url(r'^manage/del/all/$', manage.drop_sys_info, name='drop_all'),
    url(r'^manage/del/range/(?P<timing>[0-9])/$', manage.del_monitor_data, name='del_monitor_data'),
    url(r'^manage/$', manage.index, name='monitor_manage'),   
    url(r'^received/sys/info/$', api.received_sys_info, name='received_sys_info'),
    url(r'^jmx/get/(?P<hostid>\d+)/(?P<appid>\d+)/(?P<app_name>.+)/(?P<timing>\d+)/$', jmx.get_app, name='get_app'),
    url(r'^jmx/(?P<ip>.+)/(?P<port>\d+)/(?P<server_type>.+)/(?P<timing>\d+)/$', jmx.jmx_info, name='jmx_info'),
    
]
