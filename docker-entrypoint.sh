#!/usr/bin/env bash

args=("$@")

case "${1}" in
    "bash")
        shift
        exec bash -c "${args[@]:1}"
        ;;
    "sleep")
        exec bash -c "while true; do sleep 2; done"
        ;;
    "run-web")
        exec gunicorn project.wsgi:application -w 10 --log-level=info --bind=0.0.0.0:8000
        ;;
    "run-celery-beat")
        exec bash -c "celery -A project beat --scheduler django_celery_beat.schedulers:DatabaseScheduler -l INFO"
        ;;
    "run-celery-worker")
        exec bash -c "celery -A project worker -l INFO --concurrency=10 -E"
        ;;
esac
