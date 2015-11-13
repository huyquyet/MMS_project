from django.contrib.auth.models import User

from app.project.models import TeamProject
from app.user.models import Profile

__author__ = 'FRAMGIA\nguyen.huy.quyet'


#
def return_user(user):
    if User.objects.filter(user=user).exists():
        return User.objects.get(user=user)
    else:
        return User.objects.get(id=1)


def return_team_of_user(user):
    return Profile.objects.get(user=user).team


def return_position_of_user(user):
    return Profile.objects.get(user=user).position


def return_current_project_of_user(user):
    team = user.team
    project = TeamProject.objects.get(team=team, status=True).project
    return project


def check_leader(user):
    profile = Profile.objects.get(user=user)
    if profile.position.name == 'Leader':
        return True
    else:
        return False
