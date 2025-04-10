# Django core imports
from django import forms

# Third-party app imports
from taggit.forms import TagWidget

# Local app imports
from .models import Blog, Post, Comment


class BlogForm(forms.ModelForm):
    """Form for creating and updating a blog."""

    class Meta:
        # Specifies the model to use for the form
        model = Blog
        # Fields to include in the form
        fields = ["title", "description"]
        # Custom label for the title field
        labels = {"title": "Blog Title"}
        widgets = {
            # Title input with styling
            "title": forms.TextInput(attrs={"class": "form-control"}),
            # Description textarea with styling
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class BlogEditForm(forms.ModelForm):
    """Form for editing blog description."""

    class Meta:
        # Specifies the model for the form
        model = Blog
        # Field to include in the form
        fields = ["description"]
        widgets = {
            # Description textarea with styling and placeholder
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Update blog description...",
                }
            ),
        }


class PostForm(forms.ModelForm):
    """Form for creating and updating a blog post."""

    class Meta:
        # Specifies the model for the form
        model = Post
        # Fields to include in the form
        fields = ["title", "content", "tags"]
        widgets = {
            # Content textarea with rich-text class
            "content": forms.Textarea(attrs={"class": "rich-text"}),
            # Tags input with styling and placeholder
            "tags": TagWidget(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add tags seperated by commas",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form and set field requirements."""
        super().__init__(*args, **kwargs)
        # Make content field optional
        self.fields["content"].required = False
        # Make tags field optional
        self.fields["tags"].required = False

    def clean_content(self):
        """Validate that content is not empty."""
        content = self.cleaned_data.get("content")
        if not content or content.strip() == "":
            raise forms.ValidationError("Content cannot be empty.")
        return content


class CommentForm(forms.ModelForm):
    """Form for creating comments on blog posts."""

    class Meta:
        # Specifies the model for the form
        model = Comment
        # Field to include in the form
        fields = ["content"]
        widgets = {
            # Content textarea with styling and placeholder
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write a comment...",
                }
            )
        }

