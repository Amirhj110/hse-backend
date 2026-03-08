from .base import *
import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-temporary-key")

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600)
}

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")