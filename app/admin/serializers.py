from rest_framework import serializers

from app.user.models import Profile

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class UserSerializer(serializers.ModelSerializer):
    # owner = serializers.One(many=False, queryset=User.objects.get())
    team = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    position = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')

    class Meta:
        model = Profile
        fields = ('id', 'user', 'avata', 'description', 'team', 'position')
        read_only_fields = ('user', 'team', 'position')
        depth = 0
        # extra_kwargs = {'password': {'write_only': True}}
