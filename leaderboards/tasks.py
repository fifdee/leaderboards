import datetime

from django.utils.timezone import now
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from leaderboards.models import Leaderboard


@db_periodic_task(crontab(minute='*/5'))
def leaderboard_expired():
    leaderboards = Leaderboard.objects.all()
    for leaderboard in leaderboards:
        if now() - leaderboard.modified_date > datetime.timedelta(minutes=15):
            leaderboard.delete()
