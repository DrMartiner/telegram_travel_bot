import os

import dj_database_url
import environ
import validators
from _socket import gethostbyname

root = environ.Path(__file__, "../..")

os.sys.path.insert(0, root())
os.sys.path.insert(0, os.path.join(root(), "apps"))

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["*"]),
    SECRET_KEY=(str, "=ees78&%^$i2gy6r576e4%^$%GF2UYRDfrtft=f=g0_bfe34&*^%!@fkuaoj!z#lleivq"),
    TIME_ZONE=(str, "Europe/Moscow"),
    LANGUAGE_CODE=(str, "ru-RU"),
    DB_DSN=(str, "postgres://user:pass@pg:5432/main"),
    BASE_URL=(str, "https://site.ru"),
    ROLE=(str, "prod"),
    BROKER_URL=(str, "redis://redis:6379/1"),
    CELERY_BROKER_URL=(str, "redis://redis:6379/1"),
    CELERY_RESULT_BACKEND=(str, "redis://redis:6379/1"),
    CELERY_RESULT_BACKEND_URL=(str, "redis://redis:6379/1"),
    CELERY_ALWAYS_EAGER=(bool, False),
    TELEGRAM_TOKEN=(str, None),
    TELEGRAM_USE_WEBHOOK=(bool, True),
    REDIS_HOST=(str, "redis"),
)

env_path = root(".env")
if os.path.exists(env_path):
    environ.Env.read_env(env_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROLE = env("ROLE")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")
allowed_hosts = set()
for host in ALLOWED_HOSTS:
    if not validators.domain(host):
        continue

    try:
        ip: str = gethostbyname(host)
        allowed_hosts.add(ip)
    except Exception as e:
        ...

INSTALLED_APPS = [
    "adminsortable",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "django_celery_results",
    "solo",
    "apps.bot.apps.BotConfig",
    "apps.common.apps.CommonConfig",
    "apps.trip.apps.TripConfig",
    "apps.users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [root("project/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {"default": dj_database_url.config(default=env("DB_DSN"))}
FIXTURE_DIRS = [root("project/fixtures")]
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

USE_TZ = True
TIME_ZONE = env("TIME_ZONE")

LANGUAGE_CODE = env("LANGUAGE_CODE")
USE_I18N = True
USE_L10N = True

MEDIA_URL = "/media/"
MEDIA_ROOT = root("media")

STATIC_URL = "/static/"
STATIC_ROOT = root("static")
STATICFILES_DIRS = [root("project/static")]

BASE_URL = env("BASE_URL")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "WARNING", "handlers": ["console"]},
    "formatters": {"verbose": {"format": "%(levelname)s  %(asctime)s  %(module)s: %(message)s"}},
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "celery": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "django.server": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "django.request": {"level": "INFO", "handlers": ["console"], "propagate": True},
        "django.db.backends": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "telegram": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "telegram.bot": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
    },
}

BROKER_URL = env("BROKER_URL")
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND_URL")
CELERY_ACCEPT_CONTENT = ["application/x-python-serialize"]
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_APP = "project"
CELERYD_LOG_LEVEL = "INFO"
CELERYD_OPTS = "--concurrency=20"
CELERYBEAT_OPTS = '--schedule="/tmp/celerybeat-schedule-%I"'
CELERY_ALWAYS_EAGER = env("CELERY_ALWAYS_EAGER")

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 * 3

AUTH_USER_MODEL = "users.User"

if ROLE == "test":
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

    class DisableMigrations(object):
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()

TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
TELEGRAM_USE_WEBHOOK = env("TELEGRAM_USE_WEBHOOK")

REDIS_HOST = env("REDIS_HOST")

APPEND_SLASH = True
