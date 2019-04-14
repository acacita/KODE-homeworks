from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
import uuid


class UserManager(models.Manager):
    def _create_user(self, username, password, email, **kwargs):
        username = self.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **kwargs):
        return self._create_user(username, password, **kwargs)

    def delete_user(self, user, raw_password, **kwargs):
        check = user.check_password(raw_password, **kwargs)

        if check:
            user.delete()
            return check


class User(AbstractBaseUser):
    user_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=40)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    password = models.CharField('password', max_length=128)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def delete(self, *args, **kwargs):
        super(User, self).delete(*args, **kwargs)


class Message(models.Model):
    audio_content = models.FileField(upload_to='uploads/')
    text_content = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Subscribers(models.Model):
    user_id = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
