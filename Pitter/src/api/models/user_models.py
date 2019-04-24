from __future__ import unicode_literals
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
import uuid
from django.core.exceptions import ValidationError


class UserManager(models.Manager):
    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError("Username must be provided")

        with transaction.atomic():
            username = self.normalize_username(username)
            email = self.normalize_email(email)
            user = self.model(username=username, email=email, **kwargs)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, username, password, **kwargs):
        return self._create_user(username, password, **kwargs)

    @staticmethod
    def delete_user(self, user, raw_password, **kwargs):
        check = user.check_password(raw_password, **kwargs)
        if check:
            user.delete()
            return check

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser):
    user_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=40)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    following_relation = models.ManyToManyField('self', through='Subscribers', symmetrical=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def delete(self, *args, **kwargs):
        super(User, self).delete(*args, **kwargs)

    def add_relationship(self, person):
        if self != person:
            relationship, created = User.objects.get_or_create(
                from_person=self,
                to_person=person)
            return relationship
        else:
            raise ValidationError("You can not follow yourself")

    def remove_relationship(self, person):
        User.objects.filter(
            from_person=self,
            to_person=person).delete()
        return

    def get_relationships(self):
        return self.following_relation.filter(
            whomfollows__user_id=self)

    def get_related_to(self):
        return self.following_relation.filter(
            whofollows__follower_id=self)

    def get_connections(self):
        return self.get_relationships()

    def get_followers(self):
        return self.get_related_to()


class Subscribers(models.Model):
    user_id = models.ForeignKey(User, related_name='whofollows', on_delete=models.CASCADE)
    follower_id = models.ForeignKey(User, related_name='whomfollows', on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'User {} follows {}'.format(self.user_id, self.follower_id)
