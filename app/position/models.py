from django.db import models


# Create your models here.

class Position(models.Model):
    name = models.TextField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name

