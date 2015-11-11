from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils import timezone
from app.team.models import Team


class Project(models.Model):
    name = models.TextField(max_length=300)
    slug = models.SlugField()
    leader = models.ForeignKey(User, related_name='project_leader', default=1)
    content = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)
    """
    0 : fail
    1 : success
    2 : progress
    3 : begin

    """
    team = models.ManyToManyField(Team, through="TeamProject", related_name='project')

    def __unicode__(self):
        return self.name


class TeamProject(models.Model):
    team = models.ForeignKey(Team, related_name='team_project')
    project = models.ForeignKey(Project)
    status = models.BooleanField(default=False)
