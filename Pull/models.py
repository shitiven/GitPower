# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User
from Depot.models import Repo
import datetime

class PullRequest(models.Model):
    repo      = models.ForeignKey(Repo)
    requester = models.ForeignKey(User)
    from_head = models.CharField(max_length = 100)
    to_head   = models.CharField(max_length = 100)
    commit_msg    = models.CharField(max_length = 100)
    create_date   = models.DateTimeField(default = datetime.datetime.now())
    create_commit_hexsha = models.CharField(max_length = 100)
    merged_commit_hexsha = models.CharField(max_length = 100)
    comment   = models.TextField()
    stat      = models.CharField(max_length = 10, default = "open")
    assigner  = models.ForeignKey(User, related_name = "assigner", null = True, blank = True)