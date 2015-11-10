# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0001_initial'),
        ('user', '0003_auto_20151109_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.ForeignKey(related_name='profile', default=1, null=True, to='position.Position'),
        ),
    ]
