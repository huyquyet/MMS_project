from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from MMS_project import settings
from app.position.models import Position
from app.team.models import Team


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    avata = models.ImageField(upload_to=settings.AVATA_DIR, max_length=255, default='avata/default.jpg', blank=False)
    description = models.TextField(default='', null=True)
    team = models.ForeignKey(Team, related_name='user', default=4, null=True)
    position = models.ForeignKey(Position, related_name='profile', default=1, null=True)

    # def delete(self, *args, **kwargs):
    #     self.user.delete()
    #     return super(self.__class__, self).delete(*args, **kwargs)
