from django.db import models
from .user_models import User
from django.utils import timezone


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
