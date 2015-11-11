from django.contrib.auth.models import User

from app.team.models import Team
from app.user.models import Profile

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def return_total_user_of_team(team):
    result_team = Team.objects.get(id=team.id)
    result = result_team.user.all().count()
    return result


def return_list_member_of_team(team):
    result_team = Team.objects.get(id=team.id)
    leader = User.objects.get(id=team.leader.id)
    result = result_team.user.all().exclude(user=leader)
    for i in result:
        i.position_name = i.position.name
        i.name = i.user.first_name + ' ' + i.user.last_name
    return result


def return_leader_of_team(team):
    return team.leader.profile


def return_list_member_leader(team):
    result = []
    result.append(return_leader_of_team(team))
    for i in Profile.objects.exclude(user=result[0].user):
        result.append(i)
    for i in result:
        i.name = i.user.first_name + ' ' + i.user.last_name
    return result
