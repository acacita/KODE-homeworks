from rest_framework import serializers
from .user_models import User, Subscribers


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        extra_field = {'password': {'write_only': True}}


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribers
        fields = '__all__'
        read_only_fields = ('user_id',)
