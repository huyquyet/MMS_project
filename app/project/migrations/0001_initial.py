# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.TextField(max_length=300)),
                ('slug', models.SlugField()),
                ('content', models.TextField()),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('project', models.ForeignKey(to='project.Project')),
                ('team', models.ForeignKey(to='team.Team', related_name='team_project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ManyToManyField(through='project.TeamProject', to='team.Team', related_name='project'),
        ),
    ]
