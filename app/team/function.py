from django.contrib.auth.models import User

from app.team.models import Team

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def return_total_user_of_team(team):
    result_team = Team.objects.get(id=team.id)
    result = result_team.user.all().count()
    return result


def return_list_member_of_team(team):
    result_team = Team.objects.get(id=team.id)
    leader = User.objects.get(id=team.leader.id)
    result = result_team.user.all().exclude(user=leader)
    # result = set(result_user).difference(set(leader.profile))
    for i in result:
        i.position_name = i.position.name
        i.name = i.user.first_name + ' ' + i.user.last_name
    return result
