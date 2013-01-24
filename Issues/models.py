# -*- coding:utf-8 -*-

from django.db import models
from Depot.models import Repo
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

import datetime

class MileStone(models.Model):
    '''milestone model'''

    title    = models.CharField(u'名称', max_length = 50)
    content  = models.TextField(u'描述')
    duedate  = models.DateTimeField(u'截止时间')
    repo     = models.ForeignKey(Repo, verbose_name="项目")
    creater  = models.ForeignKey(User)
    add_time = models.DateTimeField(default = datetime.datetime.now()) 

    class Meta:
        unique_together = ("title", "repo",)

    def __str__(self):
        return self.title


class IssueLabel(models.Model):
    '''issue's label'''

    name  = models.CharField(u'名称', max_length = 30)
    color = models.CharField(u'颜色', max_length = 7)
    repo  = models.ForeignKey(Repo)

    class Meta:
        unique_together = ("name", "repo", )


    def save(self, *args, **kwargs):
        try:
            IssueLabel.objects.get(name=self.name, repo=self.repo)
        except:
            super(IssueLabel, self).save(*args, **kwargs)


@receiver(post_save, sender=Repo)
def RepoSaved(sender, **kwargs):
    '''create default labels when repo object is saved '''

    labels = [
        {
            "name" : "缺陷",
            "color" : "#fc2929"
        },
        {
            "name" : "功能",
            "color" : "#cc317c"
        },
        {
            "name" : "支持",
            "color" : "#cccccc"
        },
        {
            "name" : "建议",
            "color" : "#84b6eb"
        }
    ]
    saved_repo  = kwargs["instance"]
    
    for label in labels:
        label_model = IssueLabel()
        label_model.name  = label["name"]
        label_model.color = label["color"]
        label_model.repo  = saved_repo
        label_model.save()


class Issue(models.Model):
    '''issue model'''

    title   = models.CharField(u'标题', max_length = 50)
    content = models.TextField(u'内容')
    created = models.DateTimeField(default   = datetime.datetime.now())
    updated = models.DateTimeField(default   = datetime.datetime.now())
    commented = models.DateTimeField(default = datetime.datetime.now())
    milestone = models.ForeignKey(MileStone, null = True, blank = True)
    submitter = models.ForeignKey(User, related_name="issuse_submitter")
    assigner  = models.ForeignKey(User, related_name="issuse_assigner", null = True, blank = True)
    labels    = models.ManyToManyField(IssueLabel, null = True, blank= True)
    state     = models.CharField(max_length = 10, default = "opened")
    repo      = models.ForeignKey(Repo, related_name="issuse_repo")
    order     = models.IntegerField(max_length = 10)

    def save(self, *args, **kwargs):

        if self.order is None:
            self.order = Issue.objects.filter(repo = self.repo).count() + 1

        super(Issue, self).save(*args, **kwargs)

    def close(self, *args, **kwargs):

        self.state = "closed"
        super(Issue, self).save(*args, **kwargs)

    def open(self, *args, **kwargs):

        self.state = "opened"
        super(Issue, self).save(*args, **kwargs)

    def state_toggle(self, *args, **kwargs):

        if self.is_open:
            self.close()
        else:
            self.open()

    @property
    def is_open(self):
        return self.state == "opened"


class Comment(models.Model):
    '''issue's comments'''
    
    content   = models.TextField(u'内容')
    submitter = models.ForeignKey(User)
    created   = models.DateTimeField(default = datetime.datetime.now())
    issue     = models.ForeignKey(Issue, related_name="issue_comment")
    
    