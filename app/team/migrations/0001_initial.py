# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.TextField()),
                ('slug', models.SlugField()),
                ('about_team', models.TextField()),
                ('position', models.ForeignKey(to='position.Position', related_name='team_position')),
            ],
        ),
    ]
