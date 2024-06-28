"""Celery configuration file"""

from os import environ as env

from celery.schedules import crontab


# Broker settings.
broker_url = env.get("CELERY_BROKER_URL")
broker_connection_retry_on_startup = True
# Using the database to store task state and results. (only available with redis broker)
# result_backend = env.get("CELERY_RESULT_BACKEND")

tasks_acks_late = True

# Celery beat periodic tasks definition
beat_schedule = {
    "core.task_scheduled_every_minute": {
        "task": "core.sample_scheduled_task",
        "schedule": crontab(minute="*/1"),
    },
}

timezone = "America/Mexico_City"
task_serialize = "json"
result_serialize = "json"
accept_content = ["json"]
result_accept_content = ["json"]
enable_utc = True
