from django.contrib import admin
from .models import Blog, Post

"""
Admin configuration for blog models.
Registers Blog and Post models with the admin site.
"""
# Register your models here.
admin.site.register(Blog)  # Enables admin interface for Blog model
admin.site.register(Post)  # Enables admin interface for Post model