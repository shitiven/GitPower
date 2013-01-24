# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from Service import (
    service_create,
    service_delete,
    service_edit,
    service_admin
)

urlpatterns = patterns('',

    url(r'create$', service_create, name = "service_create"),
    url(r'(\d+)/edit$', service_edit, name = "service_edit"),
    url(r'(\d+)/delete$', service_delete, name = "service_delete"),
    url(r'my$', service_admin, name = "service_admin"),
    
)