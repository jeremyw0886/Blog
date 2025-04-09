"""
Django settings for Blog project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import json
import logging
from pathlib import Path
from decouple import config
import dj_database_url

# Set up logging
logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default="django-insecure-#sw80_jwl031)^!54ecrd$ltatqkw3x-&w^029_n+9*w^!!&b1")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Base allowed hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'main-bvxea6i-2hqacq3d4sf2m.us-4.platformsh.site',
    'www.main-bvxea6i-2hqacq3d4sf2m.us-4.platformsh.site',
]

# Load from environment variable (optional)
if 'ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS.extend(config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')]))

# Platform.sh dynamic routes with robust parsing (still included for flexibility)
if 'PLATFORM_ROUTES' in os.environ:
    try:
        routes = json.loads(os.environ['PLATFORM_ROUTES'])
        if routes:  # Ensure it's not an empty dict
            for route_url in routes.keys():
                host = route_url.split('//')[1].rstrip('/')
                ALLOWED_HOSTS.append(host)
        else:
            logger.warning("PLATFORM_ROUTES is empty; skipping dynamic host addition.")
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.warning(f"Failed to parse PLATFORM_ROUTES: {e}. Using default ALLOWED_HOSTS.")

# Ensure no duplicates
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

# Application definition
INSTALLED_APPS = [
    # My apps
    "blogs",
    "accounts",

    # Third-party apps
    "django_bootstrap5",
    "taggit",

    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Blog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "Blog.wsgi.application"

# Database
# Use DATABASE_URL if available (Platform.sh), otherwise fallback to SQLite
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(default=os.environ['DATABASE_URL'], conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "blogs" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# My Settings
LOGIN_REDIRECT_URL = "blogs:community"
LOGOUT_REDIRECT_URL = "blogs:index"