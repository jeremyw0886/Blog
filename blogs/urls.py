# Django URL imports
from django.urls import path

# Local app imports
from . import views

# Namespace for blog-related URL patterns
app_name = "blogs"

urlpatterns = [
    # Homepage listing all blogs
    path("", views.index, name="index"),
    # Detailed view of a specific blog
    path("blog/<int:blog_id>/", views.blog_detail, name="blog_detail"),
    # Create a new blog
    path("new_blog/", views.new_blog, name="new_blog"),
    # Edit an existing blog
    path("edit_blog/<int:blog_id>/", views.edit_blog, name="edit_blog"),
    # Create a new post for a blog
    path("new_post/<int:blog_id>/", views.new_post, name="new_post"),
    # Detailed view of a specific post
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    # Edit an existing post
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    # Delete a specific post
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    # View posts filtered by tag
    path("tag/<slug:tag_slug>/", views.posts_by_tag, name="posts_by_tag"),
    # Handle post reactions
    path("react/<int:post_id>/", views.react_to_post, name="react_to_post"),
    # Edit a specific comment
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    # Delete a specific comment
    path(
        "comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"
    ),
    # Explore public blogs
    path("explore/", views.public_home, name="public_home"),
    # Community view of blogs
    path("community/", views.community_view, name="community"),
    # Public detailed view of a blog
    path(
        "community/blog/<int:blog_id>/",
        views.public_blog_detail,
        name="public_blog_detail",
    ),
    # Trigger a 404 error for testing
    path("trigger-404/", views.trigger_404),
    # Trigger a 500 error for testing
    path("trigger-500/", views.trigger_500),
]
