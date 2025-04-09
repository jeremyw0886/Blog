"""
Django settings for Blog project.
"""

import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-#sw80_jwl031)^!54ecrd$ltatqkw3x-&w^029_n+9*w^!!&b1')
DEBUG = True  # Set to True for now to debug

# Allowed hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'main-bvxea6i-2hqacq3d4sf2m.us-4.platformsh.site',
    'www.main-bvxea6i-2hqacq3d4sf2m.us-4.platformsh.site',
]

# Application definition
INSTALLED_APPS = [
    "blogs",
    "accounts",
    "django_bootstrap5",
    "taggit",
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

# Database (SQLite locally, PostgreSQL on Platform.sh)
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

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "blogs" / "static"]
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom settings
LOGIN_REDIRECT_URL = "blogs:community"
LOGOUT_REDIRECT_URL = "blogs:index"

# Platform.sh settings
try:
    from platformshconfig import Config
    config = Config()
    if config.is_valid_platform():
        ALLOWED_HOSTS.append('.platformsh.site')
        DEBUG = False
        if config.appDir:
            STATIC_ROOT = Path(config.appDir) / 'static'
            MEDIA_ROOT = Path(config.appDir) / 'media'
        if config.projectEntropy:
            SECRET_KEY = config.projectEntropy
        if not config.in_build():
            db_settings = config.credentials('database')
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': db_settings['path'],
                    'USER': db_settings['username'],
                    'PASSWORD': db_settings['password'],
                    'HOST': db_settings['host'],
                    'PORT': db_settings['port'],
                }
            }
except ImportError:
    pass  # Use SQLite locally if platformshconfig isn’t available