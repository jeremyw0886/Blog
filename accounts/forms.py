from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class RegistrationForm(UserCreationForm):
    """
    Form for user registration with username and email fields.
    Inherits from Django's UserCreationForm.
    """

    class Meta:
        # Specifies the model to be used for this form
        model = User
        # Defines the fields to include in the form
        fields = ("username", "email")


class AvatarForm(forms.ModelForm):
    """
    Form for uploading user avatar images.
    Handles file input for profile pictures.
    """

    class Meta:
        # Specifies the model for avatar storage
        model = Profile
        # Defines the field for avatar upload
        fields = ["avatar"]
        widgets = {
            # Configures the file input widget with CSS class
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            # Custom label for the avatar field
            "avatar": "Upload Avatar",
        }


class ProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.
    Provides a textarea for bio input.
    """

    class Meta:
        # Specifies the model for profile data
        model = Profile
        # Defines the field for bio input
        fields = ["avatar", "bio"]
        widgets = {
            # Configures the textarea widget with attributes
            "bio": forms.Textarea(
                attrs={
                    "class": "rich-text",
                    "rows": 4,
                    "form-control"
                    "placeholder": "Tell us about yourself...",
                }
            ),
        }
