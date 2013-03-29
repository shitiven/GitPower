# -*- coding:utf-8 -*-

from Common import *
from Depot.models import Repo
from Issues.models import Issue
from Account.models import SSHKey


@csrf_protect
def index(request):

    current_profile = None
    if request.user.is_authenticated():
        template = "index_login.html"
        current_profile  = request.user.get_profile()
    else:
        template = "index_nologin.html"

    if request.user.is_authenticated():
        sshkeys_len = SSHKey.objects.filter(user = request.user).count()
    else:
        sshkeys_len = 1

    return render_to_response(template,context_instance  = RequestContext(request,{
           "current_profile" : current_profile,
           "sshkeys_len" : sshkeys_len
    }))


@login_required
def notify(request, username, repo_name):
    issue    = request.GET.get("issue", None)
    next_url = request.GET.get("next_url", None)
    ignore   = request.GET.get("ignore", None)
    repo  = request.repo

    if issue:
        issue = get_object_or_404(Issue, id=issue)

        try:

            if ignore: issue.ignores.add(request.user)

            issue.subscribers.get(username=request.user.username)
            issue.subscribers.remove(request.user)

            messages.success(request, '订阅已成功取消')

        except User.DoesNotExist:

            if not ignore:
                issue.subscribers.add(request.user)
                issue.ignores.remove(request.user)
                messages.success(request, '订阅成功，该Issue的任何变动都将通过邮件通知')
            else:
                messages.success(request, '订阅已成功取消')
                

        return HttpResponseRedirect(next_url)
    

    #默认为repo项目订阅相关操作
    try:
        repo.subscribers.get(username=request.user.username)
        repo.subscribers.remove(request.user)
        messages.success(request, '订阅已成功取消')

    except:
        repo.subscribers.add(request.user)
        messages.success(request, '订阅成功，该项目的任何变动都将通过邮件通知')

    return HttpResponseRedirect(next_url)


def view404(request):
    return render("404.html", request, context={})


def view500(request):
    return render("500.html", request, context={})


def view403(request):
    return render("403.html", request, context={})