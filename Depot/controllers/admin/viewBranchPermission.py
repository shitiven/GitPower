# encoding: utf-8

from Common import *
from Depot.decorators import repo_access_required
from Depot.models import BranchPermission


@csrf_protect
def branch_permission(request, username, repo_name):

    if request.method == "POST":
        branch = request.POST.get("branch", None)
        member = request.POST.get("member", None)
        try:
            member = User.objects.get(username=member)
        except User.DoesNotExsit:
            messages.error(request, "成员不存在")

        if not member in request.repo.team_writers:
            messages.error(request, "该成员不在可写权限组内")

        obj, created = BranchPermission.objects.get_or_create(branch=branch, repo=request.repo)
        obj.users.add(member)

        messages.success(request, "权限指定成功")

        return HttpResponseRedirect(reverse("repo_branch_permission", args=[username, repo_name]))

    request.context.update({
        "git_repo" : request.repo.repo()
    })

    return render("repo/admin/branch_permission.html", request, context=request.context)


@csrf_protect
def branch_permission_remove(request, username, repo_name):

    if request.method == "POST":
        branch   = request.POST.get("branch")
	member   = request.POST.get("username")
        member   = User.objects.get(username=member)
        obj = BranchPermission.objects.get(repo=request.repo, branch=branch)
        obj.users.remove(member)

        messages.success(request, "移除成功")

        return HttpResponseRedirect(reverse("repo_branch_permission", args=[username, repo_name]))
