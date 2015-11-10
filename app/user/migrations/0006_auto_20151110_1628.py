# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='team',
            field=models.ForeignKey(related_name='user', to='team.Team', null=True),
        ),
    ]
