# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20151109_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='team',
            field=models.ForeignKey(related_name='team', null=True, to='team.Team'),
        ),
    ]
