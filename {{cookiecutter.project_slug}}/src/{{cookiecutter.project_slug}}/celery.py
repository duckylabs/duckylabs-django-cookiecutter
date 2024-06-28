from os import environ as env

from celery import Celery


env.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.project_slug}}.settings")
app = Celery("{{cookiecutter.project_slug}} celery app")
app.config_from_object("{{cookiecutter.project_slug}}.celery_config")
app.autodiscover_tasks()
