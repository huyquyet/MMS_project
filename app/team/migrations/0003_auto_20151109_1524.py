# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0002_auto_20151109_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(related_name='team_leader', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='position',
            field=models.ForeignKey(default=1, null=True, related_name='team_position', to='position.Position'),
        ),
    ]
