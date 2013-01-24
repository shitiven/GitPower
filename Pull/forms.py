# encoding: utf-8

from django import forms
from models import PullRequest
from django.contrib.auth.models import User
import re

class PullForm(forms.Form):
    commit_msg = forms.CharField(label = '标题',max_length = 200)
    from_head  = forms.CharField(max_length = 30)
    to_head    = forms.CharField(max_length = 30)
    commit     = forms.CharField(max_length = 100)
    comment    = forms.CharField(max_length = 200, required = False)

    def save(self, requester, repo, assigner = None):
        commit_msg = self.cleaned_data["commit_msg"]
        from_head  = self.cleaned_data["from_head"]
        to_head  = self.cleaned_data["to_head"]
        commit_hexsha  = self.cleaned_data["commit"]
        comment  = self.cleaned_data["comment"]

        pull = PullRequest()
        pull.commit_msg = commit_msg
        pull.from_head  = from_head
        pull.to_head    = to_head
        pull.create_commit_hexsha = commit_hexsha
        pull.requester = requester
        pull.repo = repo
        if assigner:
            pull.assigner = assigner

        if comment:
            pull.comment = comment

        pull.save()

        return pull

