# -*- coding:utf-8 -*-
from Depot.models import Repo
from django.core.exceptions import PermissionDenied
from Common import *
import re


class RequestMiddelWare(object):

    def get_repo(self,path):
        attributes = re.search('^/(\w+)/([-_\.a-zA-Z0-9]+)', path).groups()
        repo = get_object_or_404(Repo, owner__username=attributes[0], name=attributes[1])

        return repo

    def manange_repo(self, request):
        repo = self.get_repo(request.path)
        issue_path  = re.compile(r'^/(\w+)/([-_\.a-zA-Z0-9]+)/issues')
        admin_path = re.compile(r'^/(\w+)/([-_\.a-zA-Z0-9]+)/admin')

        #如果为私有项目则判断用户权限
        if request.user.is_authenticated():
            if request.user not in repo.team_readers and repo.is_public is False:
                raise PermissionDenied()
        else:
            raise PermissionDenied()

        request.repo = repo
        request.context = {
            "repo" : repo
        }
        if issue_path.search(request.path) is not None:
            return self.manange_issue(request)

        if admin_path.search(request.path) is not None:
            return self.manange_admin(request)

        return None

    def manange_admin(self, request):

        request.context.update({
            "current_block" : "admin"
        })

        return None
        

    def manange_issue(self, request):

        request.context.update({
            "current_block" : "issues"
        })

        return None


    def process_view(self, request, view_func, view_args, view_kwargs):

        if re.match("(^\/$)|(^/accounts/signup)|(^/accounts/login)|(^/accounts/logout)", request.path):
            return

        if not request.user.is_authenticated():
            return HttpResponseRedirect("/accounts/login")
 
        elif not request.user.is_active and not re.match("(^/accounts/validate_code)|(^/accounts/user_active)",request.path):
            return HttpResponseRedirect("/")

        #过滤非项目URL
        if re.search("^/accounts/.*", request.path) is not None: return
        if re.search("^/repo/.*", request.path) is not None: return
        if re.search("^/pull/.*", request.path) is not None: return
        if re.search("^/service/.*", request.path) is not None: return

        #如果为项目URL则进行全局管理
        if re.search("^/(\w+)/([-_\.a-zA-Z0-9]+)", request.path) is not None:
            return self.manange_repo(request)
