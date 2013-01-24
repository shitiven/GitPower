# -*- coding:utf-8 -*-

from Common import *
from Depot.models import Repo
from Account.models import SSHKey


@csrf_protect
def index(request):
    repos = []
    repos_len = 0
    if request.user.is_authenticated():
        template = "index_login.html"
        profile  = request.user.get_profile()
        repos = profile.repos
        repos_len = repos.__len__()
        repos = repos[:10]
    else:
        template = "index_nologin.html"

    if request.user.is_authenticated():
        sshkeys_len = SSHKey.objects.filter(user = request.user).count()
    else:
        sshkeys_len = 1

    return render_to_response(template,context_instance  = RequestContext(request,{
           "repos" : repos,
           "rlen"  : repos_len,
           "sshkeys_len" : sshkeys_len
    }))


def view404(request):
    return render("404.html", request, context={})


def view500(request):
    return render("500.html", request, context={})


def view403(request):
    return render("403.html", request, context={})