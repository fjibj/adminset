#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import modelform_factory
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from appconf.models import Project
from forms import ProjectForm
from accounts.permission import permission_verify
import csv
import datetime
from cmdb.api import str2gb
from models import Product, Project
from accounts.models import UserInfo, RoleList, PermissionList

@login_required()
@permission_verify()
def project_list(request):
    temp_name = "appconf/appconf-header.html"
    all_project = Project.objects.all()
    all_product = Product.objects.all()
    is_superuser = "Y"
    product_name = request.GET.get('product', '')
    if not product_name:
        product_name = get_user_productname(request)
        if product_name:
            is_superuser = "N"
            all_product = Product.objects.filter(name=product_name)
    server_types = Project.SERVER_TYPE
    server_type = request.GET.get('server_type', '')
    if product_name:
        all_project = Project.objects.filter(product__name=product_name)
    if server_type:
        all_project = Project.objects.filter(server_type=server_type)
    results = {
        'all_product':  all_product,
        'temp_name': temp_name,
        'all_project':  all_project,
        'product_name': product_name,
        'server_types': server_types,
        'server_type' : server_type,
        'is_superuser': is_superuser,
    }

    return render(request, 'appconf/project_list.html', results)

#获得用户管理的产品中心
def get_user_productname(request):
    product_name = None
    iUser = UserInfo.objects.get(username=request.user)
    # 判断用户如果是超级管理员则跳过
    if not iUser.is_superuser:
        role_permission = RoleList.objects.get(name=iUser.role)
        role_permission_list = role_permission.permission.all()

	for x in role_permission_list:
	    # 找到"资产管理"权限对应的URL,从中分解出对应的主机组名称
	    if x.url.startswith("/appconf/"):
		str = x.url
		product_name = str[str.find("?product=")+9:]
		break
	    else:
		pass
	else:
	    pass

    return product_name

@login_required
@permission_verify()
def project_del(request):
    project_id = request.GET.get('project_id', '')
    if project_id:
        Project.objects.filter(id=project_id).delete()

    project_id_all = str(request.POST.get('project_id_all', ''))
    if project_id_all:
        for project_id in project_id_all.split(','):
            Project.objects.filter(id=project_id).delete()

    return HttpResponseRedirect(reverse('project_list'))


@login_required
@permission_verify()
def project_add(request):
    temp_name = "appconf/appconf-header.html"
    product_name = get_user_productname(request)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            if product_name:
                products = Product.objects.filter(name=product_name)
                new_project = form.save(commit=False)
                new_project.product = products[0]
                new_project.save()
            else:
                form.save()
            return HttpResponseRedirect(reverse('project_list'))
    else:
        if product_name:
            products = Product.objects.filter(name=product_name)
            if len(products):
                form = ProjectForm(initial={'product': products[0].id})
        else:
            product_name = ""
            form = ProjectForm()

    results = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
        'product_name': product_name,
    }
    return render(request, 'appconf/project_base.html', results)


@login_required
@permission_verify()
def project_edit(request, project_id):
    project = Project.objects.get(id=project_id)
    temp_name = "appconf/appconf-header.html"
    product_name = get_user_productname(request)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            if product_name:
                products = Product.objects.filter(name=product_name)
                new_project = form.save(commit=False)
                new_project.product = products[0]
                new_project.save()
            else:
                form.save()      
            return HttpResponseRedirect(reverse('project_list'))
    else:
        if not product_name:
            product_name = ""
        form = ProjectForm(instance=project)

    results = {
        'form': form,
        'project_id': project_id,
        'request': request,
        'temp_name': temp_name,
        'product_name': product_name,
    }
    return render(request, 'appconf/project_base.html', results)


@login_required
@permission_verify()
def project_export(request):
    export = request.GET.get("export", '')
    project_id_list = request.GET.getlist("id", '')
    if export == "part":
        if project_id_list:
            project_find = []
            for project_id in project_id_list:
                project_item = Project.objects.get(id=project_id)
                if project_item:
                    project_find.append(project_item)

    if export == "all":
        project_find = Project.objects.all()

    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    file_name = 'adminset_project_' + now + '.csv'
    response['Content-Disposition'] = "attachment; filename="+file_name
    writer = csv.writer(response)
    writer.writerow([str2gb(u'项目名称'), str2gb(u'项目描述'), str2gb(u'语言类型'), str2gb(u'程序类型'),
                     str2gb(u'服务器类型'), str2gb(u'程序框架'), str2gb(u'源类型'), str2gb(u'源地址'),
                     str2gb(u'程序部署路径'), str2gb(u'日志文件路径'),
                     str2gb(u'所属产品线'), str2gb(u'项目负责人'), str2gb(u'服务器')])
    for p in project_find:
        server_array = p.serverList
        server_result = ""
        for server in p.serverList.all():
            server_result += server.hostname+"\n"
        writer.writerow([str2gb(p.name), p.language_type, p.app_type, p.server_type,
                        p.app_arch, p.source_type, p.source_address, p.appPath, p.configPath, str2gb(p.product),
                         str2gb(p.owner), str2gb(server_result)])
    return response
