from rest_framework import serializers
from .app_models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        extra_field = {'password': {'write_only': True }}