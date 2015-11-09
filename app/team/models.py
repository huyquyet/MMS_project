from django.db import models


# Create your models here.
from app.position.models import Position


class Team(models.Model):
    name = models.TextField()
    slug = models.SlugField()
    about_team = models.TextField()
    position = models.ForeignKey(Position, related_name='team_position')

    def __unicode__(self):
        return self.name
