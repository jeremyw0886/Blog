"""
WSGI config for Blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# Python standard library imports
import os

# Django imports
from django.core.wsgi import get_wsgi_application


# Set the default settings module for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Blog.settings")

# Initialize and expose the WSGI application
application = get_wsgi_application()
