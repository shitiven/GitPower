# -*- coding:utf-8 -*-

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from Depot.models import Repo
from functools import wraps

def repo_access(repo, user):

    access = []

    if repo.is_public is True and user.is_authenticated() is False:
        return ['reporter']

    user_profile = repo.owner.get_profile()
    if user_profile.is_team:
        
        check_owner  = user_profile.owners.filter(username = user.username).count()
        if check_owner > 0:access.append("owner")

        check_member = user_profile.members.filter(username = user.username).count()
        if check_member > 0:access.append("member") 

    else:
        
        if repo.owner == user:
            access.append("owner")
            access.append("member")

    if repo.is_public is False and access.__len__() < 1:return []

    return access 


def repo_required(func):
    '''require repo decorator'''

    def decorator(request, *args, **kwargs):

        username  = args[0]
        repo_name = args[1]
        
        repo = get_object_or_404(Repo, owner__username = username , name = repo_name)

        request.repo = repo
        request.context.update({
            "repo" : repo,
            "repo_roles" : repo_access(repo, request.user),
            "is_team" :  repo.owner.get_profile().is_team
        })

        return func(request, *args, **kwargs)


    return decorator

def repo_access_required(permission):
    '''project access decorator'''

    def decorator(func, *args, **kwargs):
        
        def inner_decorator(request, *args, **kwargs):
            username  = args[0]
            repo_name = args[1]

            repo   = get_object_or_404(Repo, owner__username = username , name = repo_name)
            access = repo_access(repo, request.user)

            if permission not in access:
                return HttpResponseForbidden()

            request.repo    = repo
            request.context.update({
                "repo" : repo,
                "access" : access
            })

            return func(request, *args, **kwargs)

        return wraps(func)(inner_decorator)

    return decorator