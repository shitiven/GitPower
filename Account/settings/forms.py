# encoding: utf-8

from django import forms
import Common.gitolite as gitolite
from django.contrib.auth.models import User
from Account.models import UserProfile, SSHKey
import GitPower.settings as settings
import os, re

class TeamForm(forms.Form):
    name = forms.CharField(label="名称", max_length = 100, widget=forms.TextInput(attrs={'class':'input-xlarge'}))

    def clean(self):
        cleaned_data = super(TeamForm, self).clean()
        name = cleaned_data.get("name")

        users = User.objects.filter(username = name)
        if users.__len__():
            self._errors["name"] = self.error_class(["已存在，请换个名字"])

        return cleaned_data

    def save(self, owner):
        name = self.cleaned_data["name"]
        team = User.objects.create_user(name, "none@taobao.com", 'noneornone')
        team_profile = team.get_profile()
        team_profile.is_team = True
        team_profile.owners.add(owner)
        team_profile.save()

        owner_profile = owner.get_profile()
        owner_profile.teams.add(team)
        owner_profile.save()

        return team


class SSHkeyForm(forms.ModelForm):

    def clean_mac(self):
        cleaned_data = super(SSHkeyForm, self).clean()
        content = cleaned_data.get("content")

        keymac = gitolite.get_mac_address(content)

        if keymac is None:
            self._errors["content"] = self.error_class(["格式错误"])

        return keymac


    class Meta:
        model = SSHKey
        exclude = ('add_time', ) 