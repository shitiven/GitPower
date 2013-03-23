# -*- coding:utf-8 -*-

from django import template
from Common.templatetags.custom import timesince
from django.utils.encoding import force_unicode
from Issues.models import Issue, Comment, IssueLabel
from custom import timesince

register = template.Library()

@register.filter
def issues_closed_number(milestone):
    return  Issue.objects.filter(milestone=milestone, state="closed").count()


@register.filter
def issues_opened_number(milestone):
    return  Issue.objects.filter(milestone=milestone, state="opened").count()


@register.filter
def milestone_percent(milestone):
    opened    = issues_opened_number(milestone)
    allissues = Issue.objects.filter(milestone=milestone).count()

    if allissues == 0:
        return 0

    return (float(opened)/float(allissues))*100.0

@register.filter
def milestone_dueday(duedate):
    return timesince(duedate, future=True)


@register.filter
def comments_number(issue):
    return Comment.objects.filter(issue = issue).count()

@register.filter
def issues_numbers(repo, state=None):
    if state is None:return Issue.objects.filter(repo = repo).count()

    return Issue.objects.filter(repo=repo, state=state).count()


@register.filter
def issues_submitter_numbers(repo, submitter):
    return Issue.objects.filter(repo=repo, submitter=submitter).count()


@register.filter
def issues_assigend_to_me_numbers(repo, assigner):
    return Issue.objects.filter(repo=repo, assigner=assigner).count()


@register.filter
def issues_path_params(dic, rk=None):
    dic = dic.copy()
    try:
        if rk is not None:dic.pop(rk)
    except:
        pass

    params = []
    for k in dic:
        params.append("%s=%s"%(k,dic[k]))

    return "&".join(params)

@register.filter
def issue_labels(repo):
    return IssueLabel.objects.filter(repo=repo)

@register.filter
def issue_labels_number(label, repo):
    return Issue.objects.filter(repo=repo, labels__in=[label]).count()
