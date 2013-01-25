# encoding: utf-8

from django import forms
from Account.models import User, UserProfile
from Common import regular
import re


class UserForm(forms.ModelForm):

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email: 
            raise forms.ValidationError("这个字段是必填项。")

        return email


    def clean_username(self):
        username = self.cleaned_data["username"]
        if re.match(regular["username"], username) is None:
            raise forms.ValidationError("只能以字母开头且只能包含字母、数字、下划线或点")

        return username


    def clean_password(self):
        password = self.cleaned_data["password"]
        if password.__len__() < 6:
            raise forms.ValidationError("长度不能小于6个字符")

        return password

    class Meta:
        model = User
        exclude = ('last_login', 'date_joined', )
