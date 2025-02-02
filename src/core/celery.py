from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.conf import settings

app = Celery("core")

app.conf.beat_schedule = {
    "delete-old-anonymous-carts-everyday": {
        "task": "cart.tasks.delete_old_anonymous_carts",
        "schedule": crontab(hour=0, minute=0),
    },
}


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
