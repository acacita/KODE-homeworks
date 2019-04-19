from __future__ import absolute_import, unicode_literals
from celery import shared_task
from ..models.user_models import User
from django.core.mail import send_mail
from settings import EMAIL_HOST_USER
import logging


@shared_task()
def post_signup_welcome_email(user_id=None, subscribers_id=None):
    try:
        user = User.objects.get(username=user_id)

        send_mail(
            'Subscription notification',
            'You are now subscribed to {}'.format(subscribers_id),
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        logging.warning('Tried to send verification email to non-existing user {}'.format(user_id))
