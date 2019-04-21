from rest_framework import serializers
from .message_model import Message


class PublicationSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField(read_only=True)
    audio_content = serializers.FileField(read_only=True)

    class Meta:
        model = Message
        fields = ('user', 'audio_content', 'text_content', 'created_at')
