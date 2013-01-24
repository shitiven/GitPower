# -*- coding:utf-8 -*-

from django import forms
from models import Repo
from django.contrib.auth.models import User
from django.forms.widgets import RadioSelect
from Common import regular
import re


class RepoForm(forms.ModelForm):

    is_public = forms.CharField(max_length = 10)

    def clean_name(self):
        cleaned_data = super(RepoForm, self).clean()

        name = cleaned_data.get("name")
        name_re = re.compile(regular["reponame"])
        
        if name_re.match(name) is None:
            self._errors["name"] = self.error_class(["包含非法字符"])

        return name

    def clean_is_public(self):
        cleaned_data = super(RepoForm, self).clean()
        is_public    = cleaned_data.get("is_public")

        return is_public == "public"

    class Meta:
        model = Repo
        exclude = ('services', 'add_time', 'labels', )