from rest_framework import serializers
from .message_model import Pitt


class PublicationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source="user.user_id")
    audio_content = serializers.FileField(read_only=True)
    id = serializers.UUIDField(read_only=False, source="pitt.id")

    class Meta:
        model = Pitt
        fields = ('id', 'user', 'audio_content', 'text_content', 'created_at')
