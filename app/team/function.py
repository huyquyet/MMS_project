from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

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
    for i in Profile.objects.exclude(user=result[0].user).exclude(position__name='Leader'):
        result.append(i)
    for i in result:
        i.name = i.user.first_name + ' ' + i.user.last_name
    return result


def set_team_user(member, id_team):
    team = get_object_or_404(Team, pk=id_team)
    member.team = team
    member.save()


def set_team_list_user(list_member, team):
    for i in list_member:
        set_team_user(i, team.id)
