from django.contrib.auth.models import User
from django.db import models



# Create your models here.
from app.team.models import Team


class Skill(models.Model):
    name = models.TextField(max_length=200)
    slug = models.SlugField()
    about_skill = models.TextField()
    team = models.ManyToManyField(Team, related_name='skill')
    user = models.ManyToManyField(User, related_name='skill_user', through='UserSkill')

    def __unicode__(self):
        return self.name


class UserSkill(models.Model):
    user = models.ForeignKey(User, related_name='user_skill')
    skill = models.ForeignKey(Skill, related_name='skill_user')
    level = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
