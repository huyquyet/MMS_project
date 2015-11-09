from django.db import models


# Create your models here.
from app.team.models import Team


class Skill(models.Model):
    name = models.TextField(max_length=200)
    slug = models.SlugField()
    about_skill = models.TextField()
    team = models.ManyToManyField(Team, related_name='skill')
