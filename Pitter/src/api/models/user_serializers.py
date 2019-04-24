from rest_framework import serializers
from .user_models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('user_id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
