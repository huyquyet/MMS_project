# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skill', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('level', models.IntegerField(default=0)),
                ('year', models.IntegerField(default=0)),
                ('skill', models.ForeignKey(to='skill.Skill', related_name='skill_user')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_skill')),
            ],
        ),
        migrations.AddField(
            model_name='skill',
            name='user',
            field=models.ManyToManyField(through='skill.UserSkill', to=settings.AUTH_USER_MODEL, related_name='skill_user'),
        ),
    ]
