# -*- coding:utf-8 -*-

from Common import *
from django.contrib.auth.decorators import login_required
from Depot.decorators import repo_required, repo_access_required
from Issues.forms import MileStoneForm
from Issues.models import MileStone
import datetime


def milestones(request, username, repo_name):
    '''milstones view'''

    context = request.context

    milestones = MileStone.objects.filter(repo=request.repo)

    context.update({
        "milestones" : milestones
    })

    return render("issues/milestones.html", request, context = context)


def delete_milestone(request, username, repo_name):
    '''delete milestone'''

    if request.method == "POST":

        milestone_id = request.POST.get("milestone_id", None)
        milestone = get_object_or_404(MileStone, id = milestone_id)
        milestone.delete()

        messages.success(request, u'里程碑 "%s" 删除成功'%milestone.title)

    return HttpResponseRedirect(reverse("milestones", args = [request.repo.owner.username, request.repo.name]))


def edit_milestone(request, username, repo_name, milestone_id):
    '''edit milestone'''

    context = request.context
    milestone = get_object_or_404(MileStone, id=milestone_id)

    if request.method == "POST":

        duedate = request.POST.get("duedate", None)
        duedate_parttern = re.compile("(\d+)/(\d+)/(\d+)")
        if duedate_parttern.search(duedate) is not None:
            duedate = datetime.datetime.strptime(duedate, "%m/%d/%Y")

        request.POST = request.POST.copy()
        request.POST.update({
            "creater" : request.user.id,
            "repo"    : request.repo.id,
            "duedate" : duedate
        })

        form = MileStoneForm(request.POST, instance=milestone, initial={"creater":request.user, "repo" : request.repo})
        
        if form.is_valid():
            form.save()

            messages.success(request, u'里程碑 "%s" 编辑成功'%milestone.title)
            return HttpResponseRedirect(reverse("milestones", args = [request.repo.owner.username, request.repo.name]))
        else:
            form_message(request, form)

    else:
        form = MileStoneForm(instance=milestone)

    context.update({
        "form" : form,
        "is_edit" : True,
        "milestone" : milestone
    })

    return render("issues/milestone_form.html", request, context = context) 


@csrf_protect
def create_milestone(request, username, repo_name):
    '''create milestone for some project'''

    context  = request.context
    if request.method == "POST":

        duedate = request.POST.get("duedate", None)
        duedate_parttern = re.compile("(\d+)/(\d+)/(\d+)")
        if duedate_parttern.search(duedate) is not None:
            duedate = datetime.datetime.strptime(duedate, "%m/%d/%Y")

        request.POST = request.POST.copy()
        request.POST.update({
            "creater" : request.user.id,
            "repo"    : request.repo.id,
            "duedate" : duedate
        })

        form = MileStoneForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "里程碑创建成功")
            return HttpResponseRedirect(reverse("milestones", args = [request.repo.owner.username, request.repo.name]))

        else:

            form_message(request, form)

    else:

        form = MileStoneForm()

    context.update({
        "form" : form
    })

    return render("issues/milestone_form.html", request, context = context)