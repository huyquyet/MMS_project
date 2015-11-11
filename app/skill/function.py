from app.skill.models import Skill, UserSkill
from app.team.models import Team

__author__ = 'FRAMGIA\nguyen.huy.quyet'

"""------------------------------------------------------------
    Skill
------------------------------------------------------------"""


def count_user_of_skill(skill):
    result = UserSkill.objects.filter(skill=skill).count()
    return result


"""------------------------------------------------------------
    Team
------------------------------------------------------------"""


def return_total_skill_of_team(team):
    return Skill.objects.filter(team=team).count()


def count_team_of_skill(skill):
    result = Team.objects.filter(skill=skill).count()
    return result


def return_list_skill_of_team(team):
    result_team = Team.objects.get(id=team.id)
    result = result_team.skill.all()
    return result


def return_list_skill_not_of_team(team):
    # list skill of team
    team_skill = Skill.objects.filter(team=team)

    # list all skill
    all_skill = Skill.objects.all()

    # list skill not of user
    result = set(all_skill).difference(set(team_skill))

    return result


"""------------------------------------------------------------
    User
------------------------------------------------------------"""


def count_skill_of_user(user):
    result = UserSkill.objects.filter(user=user).count()
    return result


def return_list_skill_of_user(user):
    user_skill = UserSkill.objects.filter(user=user)
    # .values_list('skill', flat=True)
    # result = [Skill.objects.get(id=i) for i in user_skill]
    return user_skill


def return_list_skill_not_of_user(user):
    # list skill of user
    user_skill = UserSkill.objects.filter(user=user).values_list('skill', flat=True)
    skill = [Skill.objects.get(id=i) for i in user_skill]

    # list all skill
    all_skill = Skill.objects.all()

    # list skill not of user
    result = set(all_skill).difference(set(skill))
    return result
