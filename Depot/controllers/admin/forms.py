# -*- coding:utf-8 -*-

from django import forms
from django.forms.widgets import RadioSelect

from Common import regular
from Depot.models  import Repo, DeployService, BranchPermission
from Common import get_mac_address

import re

class ServiceForm(forms.Form):
    '''service form'''
    METHODS = (
        ("POST", "POST"),
        ("GET" , "GET"),
        ("PUT" , "PUT"),
        ("DELETE", "DELETE"),
    )

    name       = forms.CharField(label="服务名称", max_length=30, min_length=5,required = True)
    call_url   = forms.URLField(label="服务请求地址", required = True)
    method     = forms.ChoiceField(label="请求方法", choices=METHODS, required = True)
    needwrite  = forms.BooleanField(label="需要写权限", required = False)
    service_to = forms.CharField(label="可使用该服务的项目", max_length=100, required = True)
    deploy_key = forms.CharField(label="deploy key", required = True)
    des        = forms.CharField(label="服务描述", min_length=10, required = True)
    creater    = None

    def clean(self):
        '''check the form data'''

        cleaned_data = super(ServiceForm, self).clean()

        name        = cleaned_data.get("name")
        service_to  = cleaned_data.get("service_to")
        deploy_key  = cleaned_data.get("deploy_key")

        #check name has register
        is_name_register = DeployService.objects.filter(name = name).count()

        if is_name_register: self._errors["name"] = self.error_class(["该服务名称已存在"])

        #check service_to regular
        if service_to is not None:
            try:
                username = service_to.split("/")[0]
                project  = service_to.split("/")[1]
                re.compile(str(username))
                re.compile(project)
            except Exception,e:
                self._errors["service_to"] = self.error_class(["正则表达式不正确"])

        #check sshkey mac address is correct 
        if get_mac_address(deploy_key) is None:
            self._errors["deploy_key"] = self.error_class(["ssh key不合法"])

        return cleaned_data

    def save(self):
        
        service = DeployService()
        for field in self.cleaned_data:
            if field is not None:
                setattr(service, field, self.cleaned_data[field])
                
        service.creater = self.creater
        service.save()


class RenameForm(forms.Form):
    '''rename repo form'''

    repo_name = forms.CharField(max_length = 100, label = u"项目名称")
    repo      = None

    def clean(self):
        '''check the form data'''

        cleaned_data = super(RenameForm, self).clean()

        cleaned_name = cleaned_data.get("repo_name")

        name_regular = regular["reponame"]

        #check the name rules
        if name_regular.match(cleaned_name) is None:
            self._errors["repo_name"] = self.error_class(["包含非法字符"])
        
        #check the name is exits
        is_name_register =  Repo.objects.filter(name = cleaned_name).exclude(id = self.repo.id)
        
        if is_name_register:
            self._errors["repo_name"] = self.error_class(["名称已存在"])

        return cleaned_data

    def save(self):
        '''do rename'''

        new_name = self.cleaned_data["repo_name"]

        self.repo.rename(new_name)

        return self.repo
