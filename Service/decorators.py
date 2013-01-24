# -*- coding:utf-8 -*-

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from Service.models import DeployService

def service_creater_required(func):
    '''service access decorator'''

    def decorator(request, service_id, *args, **kwargs):

        user    = request.user
        service = get_object_or_404(DeployService, id = service_id)
        request.service = service

        if service.creater <> user:
        	return HttpResponseForbidden()

        return func(request, service_id, *args, **kwargs)


    return decorator