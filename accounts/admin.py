from django.contrib import admin
from .models import Profile

# Registering the Profile model with the admin site to enable its management
# via the Django admin interface.
admin.site.register(Profile)