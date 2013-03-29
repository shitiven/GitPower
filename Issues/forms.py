# -*- coding:utf-8 -*-

from django import forms
from models import MileStone, Issue, Comment, IssueLabel, IssueLabel
from django.contrib.auth.models import User
from django.forms.widgets import RadioSelect
from Depot.models import Repo
import re

class MileStoneForm(forms.ModelForm):
    
    class Meta:
        model = MileStone
        exclude = ('add_time', ) 


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        exclude = ('created', 'updated', 'commented', 'state', 'order','subscribers','ignores',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('created', 'comment_type', )


class LabelForm(forms.ModelForm):

    def clean_name(self):
        cleaned_data = super(LabelForm, self).clean()
        name = cleaned_data.get("name")
        try:
            IssueLabel.objects.get(name=name, repo__id=cleaned_data.get("repo_id"))
            self._errors["name"] = self.error_class(["已存在"])
        except IssueLabel.DoesNotExist:
            pass

        return name

    def clean_color(self):
        cleaned_data = super(LabelForm, self).clean()
        color = cleaned_data.get("color")
        color_re = re.compile('#[_a-zA-Z0-9]+$')
        if color_re.match(color) is None:
            self._errors["name"] = self.error_class(['请填写"#000000"格式'])

        return color

    class Meta:
        model = IssueLabel