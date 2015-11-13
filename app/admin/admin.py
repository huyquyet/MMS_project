# Register your models here.

from import_export import resources
from app.user.models import Profile


class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
