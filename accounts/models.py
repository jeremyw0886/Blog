from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static

def default_avatar_path():
    return "accounts/img/default-avatar.png"

class Profile(models.Model):
    """
    Model representing a user's profile.
    Extends User model with additional fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default=default_avatar_path)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_avatar_url(self):
        """
        Returns the avatar URL or default static image URL.
        """
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return static("accounts/img/default-avatar.png")
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)
