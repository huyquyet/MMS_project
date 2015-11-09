from django.db import models


# Create your models here.
from app.team.models import Team


class Project(models.Model):
    name = models.TextField(max_length=300)
    slug = models.SlugField()
    content = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    team = models.ManyToManyField(Team, through="TeamProject", related_name='project')

    def __unicode__(self):
        return self.name


class TeamProject(models.Model):
    team = models.ForeignKey(Team, related_name='team_project')
    project = models.ForeignKey(Project)
    status = models.BooleanField(default=False)
