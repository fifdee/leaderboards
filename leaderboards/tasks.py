import datetime
from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from django.utils.timezone import now

from leaderboards.models import Leaderboard


@shared_task(name='leaderboard_expired')
def leaderboard_expired():
    leaderboards = Leaderboard.objects.all()
    for leaderboard in leaderboards:
        if now() - leaderboard.modified_date > datetime.timedelta(minutes=5):
            leaderboard.delete()
