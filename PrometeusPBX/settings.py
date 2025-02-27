"""
Django settings for PrometeusPBX project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

from django.urls import reverse_lazy

from PrometeusPBX.helpers import load_config

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("PROMETEUSPBX_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("PROMETEUSPBX_DEBUG", default=0)

ALLOWED_HOSTS = os.environ.get("PROMETEUSPBX_ALLOWED_HOSTS", default="*").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "core",
    "channels",
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

ROOT_URLCONF = "PrometeusPBX.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "core.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "PrometeusPBX.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("PROMETEUSPBX_DATABASE_HOST", default="localhost"),
        "NAME": os.environ.get("PROMETEUSPBX_DATABASE", default="prometeuspbx"),
        "USER": os.environ.get("POSTGRES_USER", default="prometeuspbx"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", default="prometeuspbx"),
        "PORT": os.environ.get("PROMETEUSPBX_DATABASE_PORT", default=55432),
    },
    "asterisk": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("ASTERISK_DATABASE_HOST", default="localhost"),
        "NAME": os.environ.get("ASTERISK_DATABASE", default="asterisk"),
        "USER": os.environ.get("POSTGRES_USER", default="prometeuspbx"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", default="prometeuspbx"),
        "PORT": os.environ.get("ASTERISK_DATABASE_PORT", default=55432),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# PrometeusPBX Settings

AUTH_USER_MODEL = "core.User"

PROMETEUSPBX_CONFIG = load_config()

INSTALLED_APPS = INSTALLED_APPS + PROMETEUSPBX_CONFIG["modules"]


if "ui" in PROMETEUSPBX_CONFIG["modules"]:
    LOGIN_URL = reverse_lazy("ui:login")
    LOGIN_REDIRECT_URL = reverse_lazy("ui:dashboard-home")

if PROMETEUSPBX_CONFIG["routes"]:
    DATABASE_ROUTERS = PROMETEUSPBX_CONFIG["routes"]

# Channels Support
ASGI_APPLICATION = "PrometeusPBX.asgi.application"

PROMETEUSPBX_REDIS_HOST = os.environ.get("PROMETEUSPBX_REDIS_HOST", "127.0.0.1")
PROMETEUSPBX_REDIS_PORT = os.environ.get("PROMETEUSPBX_REDIS_PORT", 6379)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                "redis://%s:%s" % (PROMETEUSPBX_REDIS_HOST, PROMETEUSPBX_REDIS_PORT)
            ],
        },
    }
}
