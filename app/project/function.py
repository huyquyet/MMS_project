from app.project.models import TeamProject
from app.team.function import return_total_user_of_team
from app.team.models import Team

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def return_total_project_of_team(team):
    if TeamProject.objects.filter(team=team).exists():
        result = TeamProject.objects.filter(team=team).count()
        return result
    else:
        return 100


def return_list_project_of_team(team):
    if TeamProject.objects.filter(team=team).exists():
        result = TeamProject.objects.filter(team=team)
        return result
    else:
        return []


def return_total_team_of_project(project):
    result = TeamProject.objects.filter(project=project).count()
    return result


def return_list_team_of_project(project):
    team = TeamProject.objects.filter(project=project).values_list('team', flat=True)
    # if len(team) == 0:
    #     return []
    # else:
    result = [Team.objects.get(id=i) for i in team]
    for i in result:
        i.member = return_total_user_of_team(i)
    return result


def return_list_team_not_of_project(project):
    team = TeamProject.objects.filter(project=project).values_list('team', flat=True)
    team_of = [Team.objects.get(id=i) for i in team]

    team_all = Team.objects.all().exclude(name='None')
    result = set(team_all).difference(set(team_of))
    for i in result:
        i.member = return_total_user_of_team(i)
    return result


def return_list_leader_of_project(project):
    list_leader = []
    list_team = return_list_team_of_project(project)
    list_leader.append(project.leader)
    for i in list_team:
        list_leader.append(i.leader)
    return list_leader
