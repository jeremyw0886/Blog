# Import the admin module from Django to manage models in the admin interface.
from django.contrib import admin

# Import the Profile model from the current app's models.
from .models import Profile

# Registering the Profile model with the admin site to enable its management
# via the Django admin interface.
admin.site.register(Profile)