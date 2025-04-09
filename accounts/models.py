# Django core imports
from django.db import models

# Django authentication imports
from django.contrib.auth.models import User

# Django signal imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# Django template imports
from django.templatetags.static import static


def default_avatar_path():
    """Returns the default avatar image path."""
    return "accounts/img/default-avatar.png"


class Profile(models.Model):
    """
    Model representing a user's profile.
    Extends User model with additional fields.
    """

    # One-to-one relationship with User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Image field for user avatar with default
    avatar = models.ImageField(upload_to="avatars/", default=default_avatar_path)
    # Optional text field for user bio
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        """Returns a string representation of the profile."""
        return f"{self.user.username}'s Profile"

    def get_avatar_url(self):
        """
        Returns the avatar URL or default static image URL.
        Checks if avatar exists before returning URL.
        """
        if self.avatar and self.avatar.name:
            return self.avatar.url
        return static("accounts/img/default-avatar.png")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """Create a Profile instance when a User is created."""
        if created:
            Profile.objects.create(user=instance)
