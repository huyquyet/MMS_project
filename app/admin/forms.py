from django import forms
from django.forms import TextInput, Textarea, DateInput
from app.position.models import Position

from app.project.models import Project
from app.skill.models import Skill

from app.team.models import Team

__author__ = 'FRAMGIA\nguyen.huy.quyet'


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
