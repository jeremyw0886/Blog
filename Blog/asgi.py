"""
ASGI config for Blog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application


# Set the default settings module for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Blog.settings")

# Initialize and expose the ASGI application
application = get_asgi_application()
