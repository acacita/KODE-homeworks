from rest_framework import serializers
from .message_model import Message


class PublicationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source="user.user_id")
    audio_content = serializers.FileField(read_only=True)

    class Meta:
        model = Message
        fields = ('user', 'audio_content', 'text_content', 'created_at')
