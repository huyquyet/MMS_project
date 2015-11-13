from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, Textarea, DateInput, PasswordInput
from django.utils.translation import ugettext_lazy as _
from import_export import resources, fields

from app.position.models import Position
from app.project.models import Project
from app.skill.models import Skill
from app.team.models import Team
from app.user.models import Profile

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

    def clean_password_con(self):
        password = self.cleaned_data.get('password')
        password_com = self.cleaned_data.get('password_com')
        if password != password_com:
            raise forms.ValidationError('password ko trung khop')
        return password


class UserUpdateFormView(forms.ModelForm):
    email_confirm = forms.CharField(label=_("Email confirmation"), widget=forms.EmailInput, help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'email_confirm']
        widgets = {
            'first_name': TextInput(attrs={'size': 50, 'required': True}),
            'last_name': TextInput(attrs={'size': 50, 'required': True}),
            'email': TextInput(attrs={'size': 50, 'required': True}),
            'email_com': TextInput(attrs={'size': 50, 'required': True}),
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    email = forms.CharField(label=_("Email "), widget=forms.EmailInput)
    email_confirm = forms.CharField(label=_("Email confirmation"), widget=forms.EmailInput)
    # help_text=_("Enter the same password as above, for verification.")

    class Meta:
        model = Profile
        fields = ['avata', 'description']
        widgets = {
            'first_name': TextInput(attrs={'size': 50, 'required': True}),
            'last_name': TextInput(attrs={'size': 50, 'required': True}),
            'email': TextInput(attrs={'size': 50, 'required': True}),
            'email_confirm': TextInput(attrs={'size': 50, 'required': True}),
        }

    def clean_email_confirm(self):
        email1 = self.cleaned_data.get('email')
        email_con = self.cleaned_data.get('email_confirm')
        if email1 != email_con:
            raise forms.ValidationError('Email ko trung khop')
        return email1


class TeamCreateFormView(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'slug', 'about_team']
        widgets = {
            'name': TextInput(attrs={'size': 70, 'required': True}),
            'slug': TextInput(attrs={'size': 70, 'required': True}),
            'about_team': Textarea(attrs={'rows': 7, 'cols': 70}),
        }


class TeamEditFormView(forms.ModelForm):
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


class CountryResource(resources.ModelResource):
    full_title = fields.Field()

    class Meta:
        model = Profile
        fields = ('user__username', 'full_title', 'avata', 'description', 'team__name', 'position__name', '',)

    def dehydrate_full_title(self, profile):
        return '%s by %s' % (profile.user.first_name, profile.user.last_name)
