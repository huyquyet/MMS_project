# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avata',
            field=models.ImageField(default='avata/default.jpg', upload_to='avata', max_length=255),
        ),
    ]
