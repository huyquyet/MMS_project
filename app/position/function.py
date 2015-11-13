from django.shortcuts import get_object_or_404

from app.position.models import Position
from app.user.models import Profile

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def return_list_user_of_position(position):
    result = Profile.objects.filter(position=position)
    return result


def set_position_user(profile, id_position):
    position = get_object_or_404(Position, id=id_position)
    profile.objects.position = position


def set_position_list_user(list_profile, id_position):
    for i in list_profile:
        set_position_user(i, id_position)
