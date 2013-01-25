# encoding: utf-8

from django.core.management import setup_environ
import sys, os, grequests

sys.path.insert(0,os.getcwd().replace("/Common/hook",""))
import GitPower.settings as settings
setup_environ(settings)

from Depot.models   import Repo
from Service.models import DeployService


repo_path  = sys.argv[1]
repo_head  = sys.argv[2]
repo_owner = repo_path.split("/")[0]
repo_name  = repo_path.split("/")[1]


data = {
"remote" : "%s:%s"%(settings.APP_URL, repo_path),
"head"   : repo_head,
"commit_msg" : sys.argv[3] 
}


repo = Repo.objects.get(owner__username = repo_owner, name = repo_name)
services = DeployService.objects.filter(repo = repo)
urls =  [service.call_url for service in services]
rs   = (grequests.post(u, data = data) for u in urls)
grequests.map(rs)

