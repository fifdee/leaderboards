import datetime

from django.utils.timezone import now
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from leaderboards.models import Leaderboard


@db_periodic_task(crontab(hour='*/4'))
def leaderboard_expired():
    leaderboards = Leaderboard.objects.all()
    for leaderboard in leaderboards:
        if (now() - leaderboard.modified_date).days > 31:
            leaderboard.delete()
