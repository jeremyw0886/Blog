import pytest
from blogs.models import Blog, Post
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_blog_creation():
    user = User.objects.create_user(username="tester", password="pass123")
    blog = Blog.objects.create(owner=user, title="Test Blog", description="Testing blog description.")
    assert blog.title == "Test Blog"
    assert str(blog) == "Test Blog"

@pytest.mark.django_db
def test_post_creation():
    user = User.objects.create_user(username="tester", password="pass123")
    blog = Blog.objects.create(owner=user, title="Blog Title")
    post = Post.objects.create(blog=blog, title="Test Post", content="Some content")
    assert post.blog.title == "Blog Title"
    assert str(post).startswith("Test Post")