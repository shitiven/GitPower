# encoding: utf-8

from django import template
from Depot.models import BranchPermission
import GitPower.settings as settings
import os

register = template.Library()


@register.filter
def branch_permission_users(repo, branch):
	try:
		permission = BranchPermission.objects.get(repo=repo, branch=branch)
		if not permission.users.all().count():
			return None

	except BranchPermission.DoesNotExist:
		return None

	return permission.users.all()