# encoding: utf-8
from django.db import models
from Pull.models import PullRequest
from Depot.models import Repo
from django.contrib.auth.models import User
import datetime

# Create your models here.
class NewsFeed(models.Model):
    news_type   = models.CharField(max_length = 30)
    content     = models.TextField()
    create_date = models.DateTimeField(default = datetime.datetime.now())
    pull        = models.ForeignKey(PullRequest, null = True)
    repo        = models.ForeignKey(Repo, null = True)
    actioner    = models.ForeignKey(User, null = True)

    def pull_merged(self, *args, **kwargs):
        self.news_type = 'pull_merged'
        super(NewsFeed, self).save(*args, **kwargs)

    def pull_closed(self, *args, **kwargs):
        self.news_type = 'pull_closed'
        super(NewsFeed, self).save(*args, **kwargs)