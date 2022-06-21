import os

from celery import Celery

from django.apps import apps

__all__ = ["app"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("web")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: [cfg.name for cfg in apps.get_app_configs()])
app.conf.beat_schedule = {
    # "google_sheets": {
    #     "task": "apps.catalog.tasks.set_new_moderator",
    #     "schedule": crontab(minute="*/10"),
    # },
}
