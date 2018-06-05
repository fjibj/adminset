#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from cmdb.models import Host
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
import json
from pyzabbix import ZabbixAPI
from datetime import datetime
import time
from api import GetSysData
from cmdb.forms import AssetForm
from cmdb.models import Host, Idc, HostGroup, ASSET_STATUS, ASSET_TYPE
from django.shortcuts import render, HttpResponse
from django.db.models import Q
from cmdb.api import get_object
from cmdb.api import pages, str2gb
import csv
import datetime
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from config.views import get_dir
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
def asset(request):
    asset_find = []
    idc_info = Idc.objects.all()
    host_list = Host.objects.all()
    group_info = HostGroup.objects.all()
    asset_types = ASSET_TYPE
    asset_status = ASSET_STATUS
    idc_name = request.GET.get('idc', '')
    group_name = request.GET.get('group', '')
    asset_type = request.GET.get('asset_type', '')
    status = request.GET.get('status', '')
    keyword = request.GET.get('keyword', '')
    export = request.GET.get("export", '')
    group_id = request.GET.get("group_id", '')
    idc_id = request.GET.get("idc_id", '')
    asset_id_all = request.GET.getlist("id", '')

    if group_id:
        group = get_object(HostGroup, id=group_id)
        if group:
            asset_find = Host.objects.filter(group=group)
    elif idc_id:
        idc = get_object(Idc, id=idc_id)
        if idc:
            asset_find = Host.objects.filter(idc=idc)
    else:
        asset_find = Host.objects.all()
    if idc_name:
        asset_find = asset_find.filter(idc__name__contains=idc_name)
    if group_name:
        asset_find = asset_find.filter(group__name__contains=group_name)
    if asset_type:
        asset_find = asset_find.filter(asset_type__contains=asset_type)
    if status:
        asset_find = asset_find.filter(status__contains=status)
    if keyword:
        asset_find = asset_find.filter(
            Q(hostname__contains=keyword) |
            Q(ip__contains=keyword) |
            Q(other_ip__contains=keyword) |
            Q(os__contains=keyword) |
            Q(vendor__contains=keyword) |
            Q(cpu_model__contains=keyword) |
            Q(cpu_num__contains=keyword) |
            Q(memory__contains=keyword) |
            Q(disk__contains=keyword) |
            Q(sn__contains=keyword) |
            Q(position__contains=keyword) |
            Q(memo__contains=keyword))
    if export:
        response = create_asset_excel(export, asset_id_all)
        return response
    assets_list, p, assets, page_range, current_page, show_first, show_end = pages(asset_find, request)
    return render(request, 'cmdb/index.html', locals())

@login_required()
@permission_verify()
def get_cpu(request, hostname, timing):
    data_time = []
    cpu_percent = []
    range_time = TIME_SECTOR[int(timing)]
    cpu_data = GetSysData(hostname, "cpu", range_time)
    for doc in cpu_data.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        c_percent = doc['cpu']['percent']
        cpu_percent.append(c_percent)
    data = {"data_time": data_time, "cpu_percent": cpu_percent}
    return HttpResponse(json.dumps(data))


@login_required()
@permission_verify()
def get_mem(request, hostname, timing):
    data_time = []
    mem_percent = []
    range_time = TIME_SECTOR[int(timing)]
    mem_data = GetSysData(hostname, "mem", range_time)
    for doc in mem_data.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        m_percent = doc['mem']['percent']
        mem_percent.append(m_percent)
    data = {"data_time": data_time, "mem_percent": mem_percent}
    return HttpResponse(json.dumps(data))

def get_value(request, hostname):
    starttime = int(request.GET["start"])
    endtime = int(request.GET["end"])
    mem_percent = []
    mem_data = GetSysData(hostname, "mem", int(time.time()))
    for doc in mem_data.get_data():
        m_value = []
        unix_time = (int(doc['timestamp']/60)*60  +10108800 -10108800)*1000
        if (unix_time>=starttime) and (unix_time<=endtime):
            m_percent = doc['mem']['percent']
            m_value.append(m_percent)
            m_tv = {"time":unix_time,"value":m_value}
            mem_percent.append(m_tv)
    data = { "result":[{"data": mem_percent}],"success":True }
    return HttpResponse(json.dumps(data))


@login_required()
@permission_verify()
def get_disk(request, hostname, timing, partition):
    data_time = []
    disk_percent = []
    disk_name = ""
    range_time = TIME_SECTOR[int(timing)]
    disk = GetSysData(hostname, "disk", range_time)
    for doc in disk.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        d_percent = doc['disk'][int(partition)]['percent']
        disk_percent.append(d_percent)
        if not disk_name:
            disk_name = doc['disk'][int(partition)]['mountpoint']
    data = {"data_time": data_time, "disk_name": disk_name, "disk_percent": disk_percent}
    return HttpResponse(json.dumps(data))


@login_required()
@permission_verify()
def get_net(request, hostname, timing, net_id):
    data_time = []
    nic_in = []
    nic_out = []
    nic_name = ""
    range_time = TIME_SECTOR[int(timing)]
    net = GetSysData(hostname, "net", range_time)
    for doc in net.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        in_ = doc['net'][int(net_id)]['traffic_in']
        out_ = doc['net'][int(net_id)]['traffic_out']
        nic_in.append(in_)
        nic_out.append(out_)
        if not nic_name:
            nic_name = doc['net'][int(net_id)]['nic_name']
    data = {"data_time": data_time, "nic_name": nic_name, "traffic_in": nic_in, "traffic_out": nic_out}
    return HttpResponse(json.dumps(data))


@login_required()
@permission_verify()
def index(request):
    temp_name = "monitor/monitor-header.html"
    all_host = Host.objects.all()
    return render(request, "monitor/index.html", locals())


@login_required()
@permission_verify()
def host_info(request, hostname, timing):
    temp_name = "monitor/monitor-header.html"
    # 传递磁盘号给前端JS,用以迭代分区图表
    disk = GetSysData(hostname, "disk", 3600, 1)
    disk_data = disk.get_data()
    partitions_len = []
    for d in disk_data:
        p = len(d["disk"])
        for x in range(p):
            partitions_len.append(x)
    # 传递网卡号给前端,用以迭代分区图表
    net = GetSysData(hostname, "net", 3600, 1)
    nic_data = net.get_data()
    nic_len = []
    for n in nic_data:
        p = len(n["net"])
        for x in range(p):
            nic_len.append(x)
    return render(request, "monitor/host_info_{}.html".format(timing), locals())


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
			unix_time = h['clock']
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
def jmx_info(request, ip, timing):
	temp_name = "monitor/monitor-header.html"
	#连接zabbix
	zapi = ZabbixAPI("http://10.45.59.240/zabbix")
	zapi.login("admin", "zabbix")

	#从request中获取ip地址
	hosts = zapi.hostinterface.get(filter={"ip":ip,"type":4})
	
	if len(hosts):
		hostid = hosts[0]['hostid']
				
		#根据hostid找到application集合
		apps = zapi.application.get(hostids=hostid)

	return render(request, "monitor/jmx_info_{}.html".format(timing), locals())
