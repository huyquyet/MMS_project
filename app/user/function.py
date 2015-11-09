from django.contrib.auth.models import User

__author__ = 'FRAMGIA\nguyen.huy.quyet'


#
def return_user(user):
    if User.objects.filter(user=user).exists():
        return User.objects.get(user=user)
    else:
        return User.objects.get(id=1)
