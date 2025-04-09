# Django core imports
from django.db import models

# Django authentication imports
from django.contrib.auth.models import User

# Third-party app imports
from taggit.managers import TaggableManager

# Default visibility setting for posts
is_public = models.BooleanField(default=True)


class Blog(models.Model):
    """Represents an overall blog."""

    # Links blog to its owner
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # Blog title with max length of 200 characters
    title = models.CharField(max_length=200)
    # Optional description of the blog
    description = models.TextField(blank=True)
    # Auto-set creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns the blog title as string representation."""
        return self.title


class Post(models.Model):
    """Represents an individual blog post."""

    # Links post to its parent blog
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")
    # Post title with max length of 200 characters
    title = models.CharField(max_length=200)
    # Optional content of the post
    content = models.TextField(blank=True)
    # Controls post visibility
    is_public = models.BooleanField(default=True)
    # Auto-set creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    # Auto-update modification timestamp
    updated_at = models.DateTimeField(auto_now=True)
    # Manages post tags
    tags = TaggableManager()
    # Count of likes on the post
    likes = models.PositiveIntegerField(default=0)
    # Count of love reactions on the post
    loves = models.PositiveIntegerField(default=0)
    # Count of laugh reactions on the post
    laughs = models.PositiveIntegerField(default=0)
    # Count of sad reactions on the post
    sads = models.PositiveIntegerField(default=0)

    def __str__(self):
        """Returns the post title as string representation."""
        return self.title


class Comment(models.Model):
    """Represents a comment on a blog post."""

    # Links comment to its parent post
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    # Links comment to its author
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Content of the comment
    content = models.TextField()
    # Auto-set creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders comments by creation date (newest first)
        ordering = ["-created_at"]

    def __str__(self):
        """Returns user and post title as string representation."""
        return f"{self.user.username} on {self.post.title}"
