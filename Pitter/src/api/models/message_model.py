from django.db import models
from .user_models import User
from django.utils import timezone
import uuid


class Pitt(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=128)
    audio_content = models.FileField(upload_to='static')
    text_content = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
