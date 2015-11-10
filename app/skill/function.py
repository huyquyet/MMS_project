from app.skill.models import Skill, UserSkill
from app.team.models import Team

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def return_total_skill_of_team(team):
    return Skill.objects.filter(team=team).count()


def count_user_of_skill(skill):
    result = UserSkill.objects.filter(skill=skill).count()
    return result


def count_skill_of_user(user):
    result = UserSkill.objects.filter(user=user).count()
    return result


def return_list_skill_of_user(user):
    user_skill = UserSkill.objects.filter(user=user).values_list('skill', flat=True)
    result = [Skill.objects.get(id=i) for i in user_skill]
    return result


def count_team_of_skill(skill):
    result = Team.objects.filter(skill=skill).count()
    return result
