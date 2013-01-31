# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
import views as repo

urlpatterns = patterns('',

    url(r'add$', repo.add_repo, name="repo_add"),
    url(r'filter$', repo.fliter_project),
    url(r'tree_ajax$', repo.repo_tree_ajax),
    
)