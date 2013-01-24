# -*- coding:utf-8 -*-

from Common import *
from Depot.decorators import repo_access_required

@repo_access_required("owner")
@csrf_protect
def repo_admin_members_remove(request, ownername, repo_name):

    context = request.context
    repo = request.repo

    if request.method == "POST":
        username = request.POST.get("username")
        member   = get_object_or_404(User, username=username)
        repo.managers.remove(member)
        repo.developers.remove(member)
        repo.reporters.remove(member)

        messages.success(request, u"移除成功")
        return HttpResponseRedirect(reverse("repo_admin_members", args=[ownername, repo_name]))


@repo_access_required("owner")
def repo_admin_members(request, ownername, repo_name):
    context = request.context
    repo = request.repo

    if request.method == "POST":
        jurisdiction = request.POST.get("jurisdiction", None)
        username     = request.POST.get("username")
        member       = get_object_or_404(User, username=username)

        owner_profile = repo.owner.get_profile()
        if owner_profile.is_team:
            if owner_profile.owners.filter(id=member.id).count() or \
                owner_profile.members.filter(id=member.id).count() or \
                owner_profile.reporters.filter(id=member.id).count(): \

                messages.error(request, u'该成员已属于Team "%s"的一员'%owner_profile.user)
                return HttpResponseRedirect(reverse("repo_admin_members", args=[ownername, repo_name]))
        
        elif owner_profile.id == member.id:
            messages.error(request, u'该成员是创建者') 
            return HttpResponseRedirect(reverse("repo_admin_members", args=[ownername, repo_name]))
      

        if jurisdiction == "owner":
            repo.managers.add(member)
            repo.developers.remove(member)
            repo.reporters.remove(member)

        elif jurisdiction == "developer":
            repo.managers.remove(member)
            repo.developers.add(member)
            repo.reporters.remove(member)

        else:
            repo.managers.remove(member)
            repo.reporters.add(member)
            repo.developers.remove(member)

        messages.success(request, "添加成功")
        return HttpResponseRedirect(reverse("repo_admin_members", args=[ownername, repo_name]))
    
    return render("repo/admin/members.html", request, context=context)


