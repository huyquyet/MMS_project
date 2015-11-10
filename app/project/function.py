from app.project.models import TeamProject

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
