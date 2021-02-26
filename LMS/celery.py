import os

from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMS.settings')

app = Celery('LMS')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'delete-logs-at-midnight': {
        'task': 'logger.tasks.delete_log',
        'schedule': crontab(minute=0, hour=0)
    }
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
