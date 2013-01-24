# -*- coding:utf-8 -*-

from Common import *
from django.contrib.auth.decorators import login_required
from Depot.decorators import repo_required, repo_access_required
from Issues.forms import LabelForm
from Issues.models import IssueLabel
from Issues.decorators import issue_decorator
import datetime


@repo_access_required("owner")
def create_label(request, username, repo_name):

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST.update({
            "repo" : request.repo.id
        })

        form = LabelForm(request.POST)

        if form.is_valid():
            label = form.save()

        else:
            return render_json({"status":"fail","messages":{"type":"error", "msg":form.errors.items()}})

    messages.success(request, "添加成功")
    return render_json({"status":"ok", "label" : {"name":label.name, "color":label.color, "id":label.id}})


@repo_access_required("owner")
def edit_labels(request, username, repo_name):

    if request.method == "POST":

        labels_data  = json.loads(request.POST.get("data","[]"))
        remove_data  = json.loads(request.POST.get("removes" , "[]"))
        request.POST = request.POST.copy()
        forms = []
        for label in labels_data:
            request.POST.update({
                "repo"  : request.repo.id,
                "name"  : label["name"],
                "color" : label["color"]
            })

            label_model = IssueLabel.objects.get(id=label["id"])
            form = LabelForm(request.POST, instance=label_model, initial={"repo" : request.repo})
            
            if form.is_valid():
                forms.append(form)
            else:
                return render_json({"status":"fail", "messages":{"type":"error", "msg":form.errors.items()}})


        for form in forms:
            form.save()


        for lid in remove_data:
            label = IssueLabel.objects.get(id = lid)
            label.delete()

    return render_json({"status":"ok"})