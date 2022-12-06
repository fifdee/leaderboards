# django_celery/celery.py

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leaderboards_project.settings")
app = Celery("leaderboards_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'check-leaderboards': {
        'task': 'leaderboard_expired',
        'schedule': crontab()
    },
}
