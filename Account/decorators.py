# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from Account.models import User
from functools import wraps
from Common import *


def team_mamanger_decorator(func):

    def decorator(request, team_name, *args, **kwargs):

        team = get_object_or_404(User, username=team_name)
        team = team.get_profile()

        if team.owners.filter(id=request.user.id).count() < 1:
            return HttpResponseForbidden()

        request.team = team

        return func(request, team_name, *args, **kwargs)

    return decorator
