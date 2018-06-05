#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from django.shortcuts import render, HttpResponse
from pyzabbix import ZabbixAPI
from datetime import datetime
from config.views import get_dir
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
TIME_SECTOR = (
            3600,
            3600*3,
            3600*5,
            86400,
            86400*3,
            86400*7,
)

@login_required()
@permission_verify()
def get_app(request, hostid, appid, app_name, timing):
	#连接zabbix
	zapi = ZabbixAPI("http://10.45.59.240/zabbix")
	zapi.login("admin", "zabbix")
	
	app_data = []

	#根据hostid和applicationid查找item集合
	items = zapi.item.get(hostids=hostid,applicationids=appid)
	
	#时间范围
	range_time = TIME_SECTOR[int(timing)]
	time_till = int(time.time())  #当前时间
	time_from = time_till - range_time 
	#遍历itemid集合
	for item in items:
		item_name = item['name']
		item_id = item['itemid']

		#对每一个itemid获取history
		history = zapi.history.get(itemids=[item_id],
								   time_from=time_from,
								   time_till=time_till,
								   output='extend',
								   #limit='5000',
								   )

		# If nothing was found, try getting it from history (float) data
		if not len(history):
			history = zapi.history.get(itemids=[item_id],
									   time_from=time_from,
									   time_till=time_till,
									   output='extend',
									   #limit='5000',
									   history=0,  #长整型
									   )		
		#定义
		data_time = []
		data_value = []

		#遍历history
		for h in history:		

			#获取值和时间戳
			unix_time = int(h['clock'])
			times = time.localtime(unix_time)
			dt = time.strftime("%m%d-%H:%M", times)
			data_time.append(dt)
			data_value.append(h['value'])

		idata = {"item_name": item_name, "data_time": data_time, "data_value": data_value}
		app_data.append(idata)
	
	data = {"app_name": app_name, "app_value": app_data}
	return HttpResponse(json.dumps(data))


@login_required()
@permission_verify()
def jmx_info(request, ip, port,server_type, timing):
	temp_name = "monitor/monitor-header.html"
	#连接zabbix
	zapi = ZabbixAPI("http://10.45.59.240/zabbix")
	zapi.login("admin", "zabbix")

	#从request中获取ip地址
	hosts = zapi.hostinterface.get(filter={"ip":ip,"type":4,"port":port})
	
	if len(hosts):
		hostid = hosts[0]['hostid']
				
		#根据hostid找到application集合
		apps = zapi.application.get(hostids=hostid)

	return render(request, "monitor/jmx_info_{}.html".format(timing), locals())
