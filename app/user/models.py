from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from MMS_project import settings
from app.team.models import Team


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    avata = models.ImageField(upload_to=settings.AVATA_DIR, max_length=255, default='', blank=False)
    team = models.ForeignKey(Team, related_name='team')
