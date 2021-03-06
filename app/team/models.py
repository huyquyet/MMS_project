from django.contrib.auth.models import User
from django.db import models

from app.position.models import Position


# Create your models here.

class Team(models.Model):
    name = models.TextField()
    slug = models.SlugField()
    leader = models.ForeignKey(User, related_name='team_leader', null=True)
    about_team = models.TextField()

    def __unicode__(self):
        return self.name
