# -*- coding:utf-8 -*-

from Common import *
from forms  import RenameForm
from Depot.decorators import repo_access_required


def repo_admin(request, username , repo_name):
    '''the admin default page'''

    repo    = request.repo
    context = request.context

    return render("repo/admin/option.html", request, context = context)


@csrf_protect
def repo_admin_competence(request, username, repo_name):
    public = request.POST.get("public", None)
    repo   = request.repo
    if public:
        repo.is_public = True
        repo.save()
    else:
        repo.is_public = False
        repo.save()

    messages.success(request, "项目权限更改成功")

    return HttpResponseRedirect(reverse("repo_admin", args=[username, repo_name])) 


@csrf_protect
def repo_rename(request, username, repo_name):
    '''rename project '''

    repo      = request.repo
    context   = request.context

    form      = RenameForm(request.POST)
    form.repo = repo

    if form.is_valid():

        repo  = form.save()
        messages.success(request, "项目名称修改成功！")

    else:

        form_message(request, form)

    return HttpResponseRedirect(reverse("repo_admin", args=[username, repo.name]))


@csrf_protect
def repo_delete(request, username, repo_name):
    '''delete the project'''

    confirm_name   = request.POST.get("repo_name")

    repo           = request.repo
    context        = request.context

    if confirm_name <> repo.name:
        messages.error(request, "输入的项目名称错误，删除失败！")
        return HttpResponseRedirect(reverse("repo_admin", args=[username, repo.name]))

    repo.delete()
    messages.success(request, u'<strong>%s</strong>项目删除成功！'%repo.name)

    return HttpResponseRedirect(reverse("index", args=[]))
