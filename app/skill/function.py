from app.skill.models import Skill, UserSkill
from app.team.models import Team

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def return_total_skill_of_team(team):
    return Skill.objects.filter(team=team).count()


def count_user_of_skill(skill):
    result = UserSkill.objects.filter(skill=skill).count()
    return result


def count_team_of_skill(skill):
    result = Team.objects.filter(skill=skill).count()
    return result
