# -*- coding:utf-8 -*-

from Common import *
from Depot.models import Repo
from Account.models import UserProfile


@login_required
def my_projects(request):
    '''filter project related with me'''
    keyword = request.POST.get("keyword")
    repos   = []

    teams   = UserProfile.objects.filter(owners__in=[request.user])
    for team in teams:
        repos.extend(Repo.objects.filter(owner=team.user, name__icontains=keyword))
    repos.extend(Repo.objects.filter(owner=request.user, name__icontains=keyword))
    repos.extend(Repo.objects.filter(managers__in=[request.user], name__icontains=keyword))

    result = []
    for repo in repos:
        result.append({
            "owner" : repo.owner.username,
            "name"  : repo.name
        })
    
    if keyword.strip().__len__():
        result = result[:10]

    return render_json({
            "status" : "ok",
            "repos"  : result
        })