# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.TextField(max_length=200)),
                ('slug', models.SlugField()),
                ('about_skill', models.TextField()),
                ('team', models.ManyToManyField(to='team.Team', related_name='skill')),
            ],
        ),
    ]
