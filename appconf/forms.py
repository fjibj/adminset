#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from django.forms.widgets import *
from .models import Product, Project, AppOwner


class AppOwnerForm(forms.ModelForm):

    class Meta:
        model = AppOwner
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'phone': TextInput(attrs={'class': 'form-control','style': 'width:450px'}),
            'qq': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'weChat': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'owner': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_url': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_user': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_password': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'language_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'server_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'jmx_port': TextInput(attrs={'class': 'form-control','style': 'width:450px;','placeholder': u'必填项'}),
            'app_arch': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'appPath': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'source_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'source_address': TextInput(attrs={'class': 'form-control','style': 'width:450px;','placeholder': u'必填项'}),
            'configPath': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'product': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'owner': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'serverList': forms.SelectMultiple(attrs={'class': 'form-control', 'size':'10', 'multiple': 'multiple'}),
            'console_url': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_console_user': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_console_password': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'db_user': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'db_password': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'os_user': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'os_password': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'db_info': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'province': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'operator': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'location': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'project_type': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'develop_type': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
        }
