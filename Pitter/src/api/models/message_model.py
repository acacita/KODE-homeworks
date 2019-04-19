from django.db import models
from .user_models import User
from django.utils import timezone


class Message(models.Model):
    audio_content = models.FileField(upload_to='uploads/')
    text_content = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

