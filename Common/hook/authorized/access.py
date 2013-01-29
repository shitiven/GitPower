#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.core.management import setup_environ
import sys
sys.path.insert(0,"/home/git/gitpower")
import GitPower.settings as settings
setup_environ(settings)

from django.contrib.auth.models import User
from Depot.models import Repo
import Account
import logging

DEBUG = True
logging.basicConfig(filename="/tmp/autkeys.log", level=logging.DEBUG)

def log(msg):

    if DEBUG: logging.debug(msg)


def filter_users_bykey(pubkey):
    '''filter users by sshkey'''
    return list(Account.models.SSHKey.objects.filter(content=pubkey))


def repo_access(username, repo_path):
    '''get user readonly or writeable in repo_path'''

    repo_owner = repo_path.split("/")[0]
    repo_name  = repo_path.split("/")[1]
   
    try: 
        user = User.objects.get(username=username)    
    except User.DoesNotExist:
        sys.exit("[ERROR] You are not gitpower member, please got to http://www.gitpower.com")
    
    try:
        repo = Repo.objects.get(owner__username=user, name=repo_name)
    except Repo.DoesNotExist:
       sys.exit("[ERROR] This project is not exist")

    access = []
    if repo.is_public:access.append("r")
    if user in repo.team_writers:access.append("w")

    return access

