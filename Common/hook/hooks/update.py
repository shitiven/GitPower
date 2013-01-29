#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.core.management import setup_environ
import sys
sys.path.insert(0,"/home/git/gitpower")
import GitPower.settings as settings
setup_environ(settings)


from Common import User
from Depot.models import BranchPermission, Repo
import os, git, re

head = sys.argv[1]
project_path = os.getcwd()
new_commit   = sys.argv[3]

repo   = git.Repo(os.getcwd())
commit = repo.commit(new_commit)

user_email = commit.author.email
user_name  = commit.author.name

try:
    repo = re.search('([a-zA-Z]+[-_\.a-zA-Z0-9]+)\/([a-zA-Z]+[-_\.a-zA-Z0-9]+)\.git$',project_path).groups()
    repo_owner = repo[0]
    repo_name  = repo[1]
    
    try:
        repo = Repo.objects.get(name=repo_name, owner__username=repo_owner)
    except Repo.DoesNotExist:
        sys.exit('[Error] the git project not exits, please visit http://www.gitpower.com')

    head = re.search('heads/(.*)',head).groups()[0]
    try:
        permission = BranchPermission.objects.get(repo=repo, branch=head)
        if permission.users.all().count():

            try:
                user = User.objects.get(email=user_email, username=user_name)
            except User.DoesNotExist:
                
                sys.exit("[Error] %(username)s(%(email)s) not gitpower's member, please visit http://help.gitpower.com")%dict(
                    username=user_name,
                    email=user_email
                )

            if not user in permission.users.all():
                sys.exit('[Access Error] %(username)s(%(email)s) have not access to push this branch, please visit http://help.gitpower.com')%dict(
		    username=user_name,
                    email=user_email
		)

    except BranchPermission.DoesNotExist:
        pass

except Exception, e:
    sys.exit(str(e))

sys.exit(0)

