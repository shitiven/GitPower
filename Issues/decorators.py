from django.contrib.auth.models import User
from Issues.models import Issue
from Depot.models import Repo
from Depot.decorators import repo_access 
from functools import wraps
from Common import *


def issue_decorator(func):

    def decorator(request, *args, **kwargs):

        issue = get_object_or_404(Issue, id=args[2])
        user  = request.user

        username  = args[0]
        repo_name = args[1]
        repo = get_object_or_404(Repo, owner__username = username , name = repo_name)

        request.issue_role = "viewer"
        if issue.submitter == user:
        	request.issue_role = "submitter"

        request.issue = issue
        request.repo  = repo
        request.context.update({
            "issue" : issue,
            "issue_role" : request.issue_role,
            "repo" : repo,
            "repo_roles" : repo_access(repo, user),
            "is_team" : repo.owner.get_profile().is_team,
            "current_block" : "issues"
        })

        return func(request, *args, **kwargs)

    return decorator
