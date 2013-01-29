#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.core.management import setup_environ
import sys
sys.path.insert(0,"/home/git/gitpower")
import GitPower.settings as settings
setup_environ(settings)


from Common import User
from Depot.models import BranchPermission, Repo
import os, git

head = sys.argv[1]
new_commit = sys.argv[3]

repo   = git.Repo(os.getcwd())
commit = repo.commit(new_commit)

user_email = commit.author.email

try:
	user = User.objects.get(email=user_email)
except User.DoesNotExist:
	sys.exit("[Error] %s not gitpower's member, please visit http://www.gitpower.com")

try:
	repo = re.search('([a-zA-Z]+[-_\.a-zA-Z0-9]+)\/([a-zA-Z]+[-_\.a-zA-Z0-9]+)\.git$',a).groups()
	repo_owner = repo[0]
	repo_name  = repo[1]
	
	try:
		repo = Repo.objects.get(name=repo_name, owner__username=repo_owner)
	except Repo.DoesNotExist:
		sys.exit('[Error] the git project not exits, please visit http://www.gitpower.com')


	head = re.search('heads/(.*)',a).groups()[0]
	try:
		permission = BranchPermission.objects.get(repo=repo, branch=head)
		if permission.users.all.count():
			if not user in permission.users.all():
				sys.exit('[Access Error] You have not access to push this branch')

	except BranchPermission.DoesNotExist:
		pass

except:
	pass

sys.exit(0)
