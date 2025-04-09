import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from blogs.models import Blog

@pytest.mark.django_db
def test_blog_index_authenticated(client):
    user = User.objects.create_user(username="authuser", password="pass")
    client.login(username="authuser", password="pass")
    response = client.get(reverse("blogs:index"))
    assert response.status_code == 200
    assert b"Your Blogs" in response.content

@pytest.mark.django_db
def test_blog_detail_view(client):
    user = User.objects.create_user(username="authuser", password="pass")
    blog = Blog.objects.create(owner=user, title="Blog Detail Test")
    client.login(username="authuser", password="pass")
    response = client.get(reverse("blogs:blog_detail", args=[blog.id]))
    assert response.status_code == 200
    assert b"Blog Detail Test" in response.content