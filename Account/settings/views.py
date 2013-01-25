# -*- coding:utf-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from Account.models import SSHKey
from Depot.models import Repo
from forms  import *
from Account.models import UserProfile
from Account.decorators import team_mamanger_decorator
from Common import *
import GitPower.settings as settings

import json


@login_required
def profile(request):

    if request.method == "POST":
        user_profile = request.user.get_profile()
        form = UserProfileForm(request.POST,instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, u"资料更新成功")
            return HttpResponseRedirect(reverse("settings_profile"))

        else:
            form_message(request, form)

    return render("user/settings/profile.html", request, context={
                "page" : "profile",
                "user" : request.user
            })


@login_required
@csrf_protect
def sshkey_delete(request, id):

    sshkey = get_object_or_404(SSHKey, id = id, user = request.user)
    sshkey.delete()
    messages.success(request, "删除成功")

    return HttpResponseRedirect(reverse("settings_sshkey"))


@login_required
@csrf_protect
def sshkey(request):

    if request.method == "POST":
        request.POST = request.POST.copy()
        request.POST.update({
            "user" : request.user.id
        })

        form = SSHkeyForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "SSHKey添加成功")
            return HttpResponseRedirect(reverse("settings_sshkey"))

        else:
            form_message(request, form) 

    else:
        form = SSHkeyForm()
    
    sshkeys = SSHKey.objects.filter(user = request.user).order_by("-add_time")
    
    context = {
        "sshkeys" : sshkeys,
        "form" : form
    }

    return render("user/settings/sshkey.html", request, context=context)


@login_required
@csrf_protect
def team(request):

    if request.method == "POST":
        form = TeamForm(request.POST)

        if form.is_valid():
            team = form.save(request.user)
            messages.success(request, "Team创建成功")
            return HttpResponseRedirect(reverse("team_members",args = [team.username]))

        else:
            form_message(request, form)

    else:

        form = TeamForm()

    return render_to_response("user/settings/team.html",context_instance  = RequestContext(request,{
                "page" : "team",
                "form" : form
            }))



@login_required
@team_mamanger_decorator
@csrf_protect
def team_members(request, team_name):

    team = request.team

    if request.method == "POST":
        jurisdiction = request.POST.get("jurisdiction", None)
        username  = request.POST.get("username")
        member    = get_object_or_404(User, username=username)

        if jurisdiction == "owner":
            team.owners.add(member)
            team.members.remove(member)
            team.reporters.remove(member)

        elif jurisdiction == "developer":

            if  team.owners.filter(id=member.id).count() and team.owners.all().count() < 2:
                messages.error(request, "至少保留一名管理人员")
                return HttpResponseRedirect(reverse("team_members", args=[team_name]))

            else:
                team.owners.remove(member)

            team.members.add(member)
            team.reporters.remove(member)

        else:
            if team.owners.filter(id=member.id).count() and team.owners.all().count() < 2:
                messages.error(request, "至少保留一名管理人员")
                return HttpResponseRedirect(reverse("team_members", args=[team_name]))
                
            else:
                team.owners.remove(member)

            team.reporters.add(member)
            team.members.remove(member)

        messages.success(request, "添加成功")

        return HttpResponseRedirect(reverse("team_members", args=[team_name]))
         

    return render("user/settings/team_members.html",request, context={
                "team" : team,
                "owners"    : team.owners.all(),
                "members"   : team.members.all(),
                "reporters" : team.reporters.all()
            })


@login_required
def team_delete(request, team_name):
    team = get_object_or_404(UserProfile, owners__in = [request.user], user__username = team_name)
    confirm_username = request.POST.get("confirm_username")

    if confirm_username <> team_name:
        messages.error(request, "Team名称输入错误")
        return HttpResponseRedirect(reverse("team_members", args = [team.user.username]))

    team.user.delete()

    return HttpResponseRedirect(reverse("settings_index"))


@login_required
@team_mamanger_decorator
@csrf_protect
def team_remove_member(request, team_name):
    
    if request.method == 'POST':
        user = request.POST.get("username")
        user = get_object_or_404(User, username=user)

        request.team.owners.remove(user)
        request.team.members.remove(user)
        request.team.reporters.remove(user)

        messages.success(request, "移除成功")

    return HttpResponseRedirect(reverse("team_members", args=[team_name]))


@login_required
def team_members_delete_owner(request, team_name):
    team = get_object_or_404(UserProfile, owners__in = [request.user], user__username = team_name)

    owner = User.objects.get(username = request.GET.get('username'))

    username  = request.GET.get('username')

    if username == request.user.username:
        return HttpResponseRedirect(reverse("team_members", args = [team.user.username]))

    team.owners.remove(owner)

    return HttpResponseRedirect(reverse("team_members", args = [team.user.username]))

@login_required
def team_members_delete_member(request, team_name):
    team = get_object_or_404(UserProfile, owners__in = [request.user], user__username = team_name)

    username  = request.GET.get('username')

    if username == request.user.username:
        return HttpResponseRedirect(reverse("team_members", args = [team.user.username]))

    member = User.objects.get(username = username)

    team.members.remove(member)
    member_profile = member.get_profile()
    member_profile.teams.remove(team.user)
    member_profile.save()

    return HttpResponseRedirect(reverse("team_members", args = [team.user.username]))
