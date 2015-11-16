from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.user.models import Profile

__author__ = 'FRAMGIA\nguyen.huy.quyet'


@receiver(post_save, sender=User)
def create_super_user(sender, instance, create, raw, using, update_fields, **kwargs):
    """
    Creat a Profile for User when a newly user is created,
    and create avatar and timeline folders.
    """
    if not create:
        return

    if instance.is_staff:
        profile = Profile.objects.create(user=instance)
        profile.save()
