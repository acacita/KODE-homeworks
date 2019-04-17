from __future__ import absolute_import, unicode_literals
import logging
from django.core.mail import send_mail
from src.celery import app
from models.user_models import User
from settings import EMAIL_HOST_USER


@app.task
def send_verification_email(user_id, subscribers_id):
    try:
        user = User.objects.get(user_id=user_id)
        send_mail(
            'Subscription notification',
            'You are now subscribed to {}'.format(subscribers_id),
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        logging.warning('Tried to send verification email to non-existing user {}'.format(user_id))