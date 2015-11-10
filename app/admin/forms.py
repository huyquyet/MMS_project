from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, Textarea, DateInput, PasswordInput

from app.position.models import Position
from app.project.models import Project
from app.skill.models import Skill
from app.team.models import Team
from django.utils.translation import ugettext_lazy as _

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class UserCreateFormView(forms.ModelForm):
    password_com = forms.CharField(label=_("Confirm password"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_com']
        widgets = {
            'username': TextInput(attrs={'size': 40, 'required': True}),
            'password': PasswordInput(attrs={'size': 20, 'required': True}),
            'password_com': PasswordInput(attrs={'size': 70, 'required': True}),
        }


class TeamCreateFormView(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'slug', 'about_team']
        widgets = {
            'name': TextInput(attrs={'size': 70, 'required': True}),
            'slug': TextInput(attrs={'size': 70, 'required': True}),
            'about_team': Textarea(attrs={'rows': 7, 'cols': 70}),
        }


class ProjectCreateFormView(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'slug', 'content', 'start_date', 'end_date']
        widgets = {
            'name': TextInput(attrs={'size': 70, 'required': True}),
            'slug': TextInput(attrs={'size': 70, 'required': True}),
            'content': Textarea(attrs={'rows': 7, 'cols': 70}),
            'start_date': DateInput(attrs={}, format="%Y-%m-%d"),
            'end_date': DateInput(attrs={}, format="%Y-%m-%d"),
        }


class SkillCreateFormView(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'slug', 'about_skill']
        widgets = {
            'name': TextInput(attrs={'size': 70, 'required': True}),
            'slug': TextInput(attrs={'size': 70, 'required': True}),
            'about_skill': Textarea(attrs={'rows': 7, 'cols': 70}),
        }


class PositionCreateFormView(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': TextInput(attrs={'size': 70, 'required': True}),
            'slug': TextInput(attrs={'size': 70, 'required': True}),
            'description': Textarea(attrs={'rows': 7, 'cols': 70}),
        }
