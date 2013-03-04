# encoding: utf-8

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from Account.models import *
from Account.profile.forms import UserForm
from Depot.models import *
from Common import *

import json, urllib
from ldap_auth import ldap_user


def index(request, username):
    current_user    = get_object_or_404(User, username = username)
    current_profile = current_user.get_profile()

    profile_index = request.GET.get("tab", "manage_projects")
    if profile_index == "joined_projects":
        repos = current_profile.joined_repos
    else:
        repos  = current_profile.repos

    return render_to_response("user/index.html", context_instance  = RequestContext(request,{
                "current_user"    : current_user,
                "current_profile" : current_profile,
                "repos" : repos,
                "is_team" : current_profile.is_team,
                "profile_index" : profile_index
            }))


@login_required
def filter_user(request):
    keywords = request.POST.get("keywords").lower()
    users = UserProfile.objects.filter(Q(user__username__startswith = keywords) | Q(nickname__startswith = keywords))
    result = {}
    result["users"] = []

    for user in users:
        if user.is_team is False:
            result["users"].append({
                "username" : user.user.username,
                "email"    : user.user.email,
                "display_name" : user.display_name
            })

    return HttpResponse(json.dumps(result))


@csrf_protect
def signup(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email    = form.cleaned_data["email"]

            user = User.objects.create_user(username, email=email, password=password)
            
            if not settings.SITE_PUBLIC:
                user.is_active = False
            else:
                user.is_active = True

            user.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            return HttpResponseRedirect("/accounts/settings")

        else:

            form_message(request, form)

    else:
        form = UserForm()

    return render("index_nologin.html", request, context={
        "form" : form
    })


@login_required
@csrf_protect
def user_to_active(request):
    '''user to active'''

    if request.method == "POST":
        invite_code  = request.POST.get("invite_code", None)
        user_profile = request.user.get_profile()
        try:
            invite_code = InviteCode.objects.get(code=invite_code, used=False)
            
            active_params = {
                "active_code":user_profile.active_code,
                "invite_code":invite_code.code,
                "user_email":request.user.email
            }
            active_url  = settings.APP_URL+"/accounts/user_active?"+urllib.urlencode(active_params)
            mail_server = MailServer()
            mail_server.active_mail(request.user.email, active_url)

            invite_code.used = True
            invite_code.user = request.user
            invite_code.save()

            messages.success(request, u'已将激活连接发送至<strong>"%s"</strong>，请进入你的邮箱进行激活'%request.user.email)

        except InviteCode.DoesNotExist:
            messages.error(request, "邀请码已过期")

    return HttpResponseRedirect("/")


def user_active(request):
    '''active from mail'''

    invite_code = request.GET.get("invite_code", None)
    active_code = request.GET.get("active_code", None)
    user_email  = request.GET.get("user_email", None)

    try:
        invite_code = InviteCode.objects.get(code=invite_code, user__email=user_email)
        try:
            user_profile = UserProfile.objects.get(active_code=active_code, user__email=user_email)
            user = user_profile.user
            user.is_active = True
            user.save()

            messages.success(request, "激活成功, 欢迎加入GitPower")

        except UserProfile.DoesNotExist:
            messages.error(request, "激活码已过期")

    except InviteCode.DoesNotExist:
        messages.error(request, "激活码已过期")

    return HttpResponseRedirect("/")


def login_out(request):
    logout(request)
    return HttpResponseRedirect("/")


@csrf_protect
def login_user(request):

    def login_with_db(username, password):

        if re.match("^(.*)@(.*)$", username):
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                return None

        return authenticate(username=username, password=password)


    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        if settings.LDAP_SERVER:
            user = ldap_user(username, password)
        else:
            user = login_with_db(username, password)

        if user is not None:
            login(request, user)
            messages.success(request, "登录成功")
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "用户名或密码错误")

    return  render("login.html", request, context = {

    })
