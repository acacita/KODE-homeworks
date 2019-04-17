from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
import uuid
from django.core.exceptions import ValidationError


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

    following_relation = models.ManyToManyField('self', through='Subscribers', symmetrical=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def delete(self, *args, **kwargs):
        super(User, self).delete(*args, **kwargs)

    def add_subscriber(self, person):  # todo change order
        if self != person:
            subscription, created = Subscribers.objects.get_or_create(
                from_person=self,
                to_person=person)
            return subscription
        else:
            raise ValidationError("You can not follow yourself")

    def del_subscription(self, person):
        Subscribers.objects.filter(
            user_id=self,
            follower_id=person).delete()
        return

    def get_connections(self):
        connections = Subscribers.objects.filter(user_id=self)
        return connections

    # def get_followers(self): #users the user is following
    #     followers = Subscribers.objects.filter(following=self.user)
    #     return followers


class Message(models.Model):
    audio_content = models.FileField(upload_to='uploads/')
    text_content = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Subscribers(models.Model):
    user_id = models.ForeignKey(User, related_name='whofollows', on_delete=models.CASCADE)
    follower_id = models.ForeignKey(User, related_name='whomfollows', on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'User {} follows {}'.format(self.user_id, self.follower_id)

    # def save(self, *args, **kwargs):
    #     if self.user_id == self.user_id:
    #         raise ValidationError("You can not follow yourself.")
    #     super(Subscribers, self).save(*args, **kwargs)
