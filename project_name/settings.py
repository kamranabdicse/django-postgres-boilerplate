import json
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from decouple import config
from ninja import NinjaAPI

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config("SECRET_KEY", default="", cast=str)

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps
    "rest_framework",
    "corsheaders",
    "db_api.apps.DbApiConfig",
]

MIDDLEWARE = [
    # our middleware
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # our middleware
    "django.middleware.locale.LocaleMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "db_api.lib.authentication.CustomAuthentication",
    ],
}

ROOT_URLCONF = "project_name.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["static"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project_name.wsgi.application"

DATABASES = json.loads(config("DATABASE"))

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Tehran"


USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [("en", _("English")), ("fa", _("Persian"))]

LOCALE_PATHS = (BASE_DIR.joinpath("locale/"),)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "fmt": {
            "format": "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] -> [%(funcName)s] %(message)s",
            "datefmt": "%Y-%m-%d:%H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "fmt",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
        "propagate": False,
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": config("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
    },
}


AUTH_USER_MODEL = "db_api.UserORM"

JWT_SECRET_KEY = config("JWT_SECRET_KEY")

JWT = {
    "SIGNING_KEY": JWT_SECRET_KEY,
}

CORS_ALLOWED_ORIGINS = json.loads(config("CORS_ALLOWED_ORIGINS"))
CORS_ALLOW_HEADERS = json.loads(config("CORS_ALLOW_HEADERS"))
CORS_ALLOW_CREDENTIALS = config("CORS_ALLOW_CREDENTIALS", default=True, cast=bool)
CSRF_TRUSTED_ORIGINS = json.loads(config("CSRF_TRUSTED_ORIGINS"))
CORS_ALLOW_METHODS = json.loads(config("CORS_ALLOW_METHODS"))

import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str


from django.utils.translation import gettext, gettext_lazy
django.utils.translation.ugettext = gettext
django.utils.translation.ugettext_lazy = gettext_lazy