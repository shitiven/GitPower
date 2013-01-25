# -*- coding:utf-8 -*-

from Common import *
from django.contrib.auth.decorators import login_required
from Depot.decorators import repo_required, repo_access_required
from Issues.forms import IssueForm, CommentForm, LabelForm
from Issues.models import Issue, Comment, IssueLabel, MileStone
from Issues.decorators import issue_decorator
import datetime


@issue_decorator
def issue(request, username, repo_name, issue_id):
    '''issue details'''
    context  = request.context

    comments = Comment.objects.filter(issue = request.issue).order_by("created")

    context.update({
        "comments" : comments,
        "members"  : request.repo.owner.get_profile().members.all(),
        "milestones" : MileStone.objects.filter(repo = request.repo),
        "labels" : [label.name for label in context["issue"].labels.all()]
    })

    return render("issues/issue.html", request, context = context)


@repo_access_required("owner")
@csrf_protect
def issue_labels_update(request, username, repo_name, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    issue.labels.clear()
    for label in request.POST.getlist("label"):
        label = IssueLabel.objects.get(id=label)
        issue.labels.add(label)

    messages.success(request, "更新成功")
    repo = request.repo
    return HttpResponseRedirect(reverse("issue", args=[repo.owner.username, repo.name, issue.id]))


@repo_access_required("member")
def issue_assign_milestone(request, username, repo_name, issue_id, milestone_id):
    milestone = get_object_or_404(MileStone, id = milestone_id)
    issue     = get_object_or_404(Issue, id = issue_id)
    issue.milestone = milestone
    issue.save()

    messages.success(request, "指派已成功")

    return HttpResponseRedirect(reverse("issue", args=[request.repo.owner.username, request.repo.name, issue_id]))


@repo_access_required("member")
def issue_assign_assigner(request, username, repo_name, issue_id, assigner_id):
    issue    = get_object_or_404(Issue, id = issue_id)
    assigner = get_object_or_404(User, id = assigner_id)
    issue.assigner = assigner
    issue.save()

    messages.success(request, "指派成功")

    return HttpResponseRedirect(reverse("issue", args=[request.repo.owner.username, request.repo.name, issue_id]))


@login_required
@issue_decorator
@csrf_protect
def issue_comment(request, username, repo_name, issue_id):
    '''issue comment'''
    context = request.context

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST.update({
            "submitter"  : request.user.id,
            "issue"      : request.issue.id
        })

        form = CommentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "评论成功")

        else:
            form_message(request, form) 

    return HttpResponseRedirect(reverse("issue", args = [request.repo.owner.username, request.repo.name, request.issue.id]))
 

def issues_filter(request, submitter=None):

    state     = request.GET.get("state", "opened")
    milestone = request.GET.get("milestone", None)
    assigner  = request.GET.get("assigner", None)
    label     = request.GET.get("label",None)

    issues = Issue.objects.filter(repo=request.repo).order_by("-created")

    context = {"issues_page":"all"}
    query   = {"state":state}

    if milestone is not None:
        milestone = MileStone.objects.get(id=milestone)
        issues    = issues.filter(milestone=milestone)
        query["milestone"] = str(milestone.id)

    if submitter is not None:
        context["issues_page"] = "submitter"
        issues = issues.filter(submitter=submitter)

    if assigner is not None:
        assigner = User.objects.get(username = assigner)
        issues = issues.filter(assigner=assigner)
        query["assigner"] = assigner.username

    if label is not None:
        label = IssueLabel.objects.get(id=label)
        issues = issues.filter(labels__in=[label])
        query["label"] = label.id


    context.update({
        "issues" : issues.filter(state=state),
        "opened_number" : issues.filter(state="opened").count(),
        "closed_number" : issues.filter(state="closed").count(),
        "state" : state,
        "members" : request.repo.owner.get_profile().members.all(),
        "milestones" : MileStone.objects.filter(repo=request.repo),
        "milestone" : milestone,
        "assigner" : assigner,
        "query" : query,
        "filter_label" : label,
        "labels" : [label.name for label in IssueLabel.objects.filter(repo=request.repo)]
    })

    return context


@repo_required
def issues(request, username, repo_name):
    '''issues view'''

    issues  = issues_filter(request)

    context = request.context
    context.update(issues)
    context.update({
        "issues_path" : reverse("issues", args=[request.repo.owner.username, request.repo.name])
    })
    return render("issues/issues.html", request, context = context)


@repo_required
def issues_created_by(request, username, repo_name, submitter):
    '''filter submitter by some boday'''

    submitter = get_object_or_404(User, username=submitter)

    context = request.context
    issues = issues_filter(request, submitter=submitter)
    context.update(issues)
    context.update({
        "issues_path" : reverse("issues_created_by", args=[request.repo.owner.username, request.repo.name, request.user.username])
    })

    return render("issues/issues.html", request, context = context)


def issue_model_edit(request, instance=False):
    request.POST = request.POST.copy()
    request.POST.update({
        "submitter" : request.user.id,
        "repo"    : request.repo.id
    })

    if instance:
        form = IssueForm(request.POST, instance=instance, initial={"submitter":request.user, "repo" : request.repo})
        instance.labels.clear()
    else:
        form = IssueForm(request.POST)

    if form.is_valid():
        issue = form.save()

        for label in request.POST.getlist("label"):
            label = IssueLabel.objects.get(id=label)
            issue.labels.add(label)

        if instance:
            messages.success(request, "Issue更新成功")

        else:
            messages.success(request, "Issue创建成功")

        return issue

    else:
        form_message(request, form)

    return form


@repo_access_required("owner")
@csrf_protect
def issue_state_toggle(request, username, repo_name):

    if request.method == "POST":
        issues = request.POST.getlist("issue")
        for issue in issues:
            issue = Issue.objects.get(id=issue)
            issue.state_toggle()

        messages.success(request, "操作成功")
        if issues.__len__() == 1:
            return HttpResponseRedirect(reverse("issue", args=[request.repo.owner.username, request.repo.name, issue.id]))

    return HttpResponseRedirect(reverse("issues",args=[request.repo.owner.username, request.repo.name]))



@issue_decorator
def issue_edit(request, username, repo_name, issue_id):
    if request.issue_role != "submitter":
        return HttpResponseForbidden()

    context = request.context

    if request.method == "POST":
        form = issue_model_edit(request, instance=request.issue)
        if form.__class__.__name__ == "Issue":
            return HttpResponseRedirect(reverse("issue", args = [request.repo.owner.username, request.repo.name, request.issue.id]))
    else:
        form = IssueForm(instance=request.issue)

    context.update({
        "form" : form,
        "members" : request.repo.owner.get_profile().members.all(),
        "milestones" : MileStone.objects.filter(repo = request.repo),
        "labels" : [label.name for label in context["issue"].labels.all()],
        "issue_edit" : True
    })

    return render("issues/issue_form.html", request, context = context)


@login_required
@repo_required
@csrf_protect
def issue_create(request, username, repo_name):
    '''create view'''

    context = request.context

    if request.method == "POST":
        form = issue_model_edit(request)
        if form.__class__.__name__ == "Issue":
            return HttpResponseRedirect(reverse("issue", args = [request.repo.owner.username, request.repo.name, form.id]))

    else:
        form = IssueForm()

    context.update({
        "form" : form,
        "members" : request.repo.owner.get_profile().members.all(),
        "milestones" : MileStone.objects.filter(repo = request.repo)
    })

    return render("issues/issue_form.html", request, context = context)