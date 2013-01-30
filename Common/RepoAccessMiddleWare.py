# -*- coding:utf-8 -*-
from Depot.models import Repo
from django.core.exceptions import PermissionDenied
from Common import *
import GitPower.settings as settings
import re


class RepoAccessMiddleWare(object):
    '''access juage'''

    def get_repo(self,path):
        attributes = re.search('^/(\w+)/([-_\.a-zA-Z0-9]+)', path).groups()
        repo = get_object_or_404(Repo, owner__username=attributes[0], name=attributes[1])

        return repo

    def manange_repo(self, request):

        admin_parttern = '(^/(\w+)/([-_\.a-zA-Z0-9]+)/admin)|' \
            '(^/(\w+)/([-_\.a-zA-Z0-9]+)/issues/label/edit$)|' \
            '(^/(\w+)/([-_\.a-zA-Z0-9]+)/issues/label/create$)|' \
            '(^/(\w+)/([-_\.a-zA-Z0-9]+)/issues/milestones/(\d+)/edit$)|' \
            '(^/(\w+)/([-_\.a-zA-Z0-9]+)/issues/milestones/delete$)|' \
            '(^/(\w+)/([-_\.a-zA-Z0-9]+)/issues/milestones/new$)'

        repo = self.get_repo(request.path)

        #先判断项目根目录是否有访问权限
        if re.search('^/(\w+)/([-_\.a-zA-Z0-9]+)', request.path):
            if request.user not in repo.team_readers and not repo.is_public:
                if request.user.is_authenticated():raise PermissionDenied
                return HttpResponseRedirect(reverse("login_user"))


        #判断admin管理权限    
        if re.search(admin_parttern, request.path):
            if request.user not in repo.allowners:
                if request.user.is_authenticated():raise PermissionDenied
                return HttpResponseRedirect(reverse("login_user"))
        

        #插入Temlate变量
        request.repo = repo
        request.context = {
            "repo" : repo
        }
        if re.search('^/(\w+)/([-_\.a-zA-Z0-9]+)/issues', request.path):
            request.context.update({
                "current_block" : "issues"
            })

        if re.search('^/(\w+)/([-_\.a-zA-Z0-9]+)/admin', request.path):
            request.context.update({
                "current_block" : "admin"
            })

        return None


    def process_view(self, request, view_func, view_args, view_kwargs):

        #如果整站不处于对外开放，则除了特殊几个URL可以访问外，其余全都关闭
        if not settings.SITE_PUBLIC:

            #开启注册、登录、登出可访问
            if re.match("(^\/$)|(^/accounts/signup)|(^/accounts/login)|(^/accounts/logout)", request.path):
                return

            #非登录用户全都跳转到登录页面
            if not request.user.is_authenticated():
                return HttpResponseRedirect("/accounts/login")
            
            #如果email尚未激活则跳转到首页，可访问邀请码输入，以及激活页面
            elif not request.user.is_active and not re.match("(^/accounts/validate_code)|(^/accounts/user_active)",request.path):
                return HttpResponseRedirect("/")


        #过滤非项目URL
        if re.search("^/accounts/.*", request.path): return
        if re.search("^/repo/.*", request.path): return
        if re.search("^/pull/.*", request.path): return
        if re.search("^/service/.*", request.path): return


        #如果为项目URL则进行全局管理
        if re.search("^/(\w+)/([-_\.a-zA-Z0-9]+)", request.path):
            return self.manange_repo(request)
