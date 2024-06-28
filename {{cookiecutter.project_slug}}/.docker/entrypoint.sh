#!/usr/bin/env bash

cd /home/djangouser/app/src

if [[ -f "requirements_local.txt" ]];
then
    pip install --no-cache-dir --root-user-action=ignore -r requirements_local.txt
fi

# image can run in multiple modes
if [[ "${1}" == "run" ]]; then
    exec gunicorn {{cookiecutter.project_slug}}.wsgi --bind 0.0.0.0:8008
elif [[ "${1}" == "jupyterlab" ]]; then
    exec python manage.py shell_plus --lab
elif [[ "${1}" == "bash" ]]; then
    exec /bin/bash
elif [[ "${1}" == "devserver" ]]; then
    exec python manage.py runserver 0.0.0.0:{{ cookiecutter.django_running_port }}
elif [[ "${1}" == "makemigrations" ]]; then
    exec python manage.py makemigrations
elif [[ "${1}" == "migrate" ]]; then
    exec python manage.py migrate
elif [[ "${1}" == "collectstatic" ]]; then
    exec python manage.py collectstatic --noinput
elif [[ "${1}" == "celery_worker" ]]; then
    exec celery -A {{cookiecutter.project_slug}}.celery:app worker -l info  -Q $QUEUE_NAMES --autoscale $CELERY_AUTOSCALE -n $CELERY_WORKER_NAME
elif [[ "${1}" == "celery_beat" ]]; then
    exec celery -A {{cookiecutter.project_slug}}.celery:app beat -l info
elif [[ "${1}" == "celery_flower" ]]; then
    exec python -m flower -A {{cookiecutter.project_slug}}.celery:app flower --port=5555
fi

exec "$@"
