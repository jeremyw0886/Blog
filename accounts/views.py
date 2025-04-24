
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AvatarForm, ProfileForm, RegistrationForm
from blogs.models import Blog, Post, Comment


def register(request):
    """Register a new user."""
    if request.method != "POST":
        # Display empty registration form
        form = RegistrationForm()
    else:
        # Process submitted form data
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page after successful registration
            return redirect("accounts:login")
    context = {"form": form}
    return render(request, "accounts/register.html", context)


@login_required
def update_avatar(request):
    """Update the user's avatar."""
    # Get the user's profile
    profile = request.user.profile

    if request.method == "POST":
        # Process avatar upload form
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to blog index after successful upload
            return redirect("blogs:index")
    else:
        # Display avatar upload form
        form = AvatarForm(instance=profile)

    return render(request, "accounts/update_avatar.html", {"form": form})


def profile_detail(request, username):
    """
    Display a user's profile details.
    Includes blog, post, and comment counts.
    """
    # Fetch user or return 404 if not found
    profile_user = get_object_or_404(User, username=username)

    # Check if the viewer owns the profile
    is_owner = profile_user == request.user

    # Count user's blogs, posts, and comments
    blog_count = Blog.objects.filter(owner=profile_user).count()
    post_count = Post.objects.filter(blog__owner=profile_user).count()
    comment_count = Comment.objects.filter(user=profile_user).count()

    return render(
        request,
        "accounts/profile_detail.html",
        {
            "profile_user": profile_user,
            "is_owner": is_owner,
            "blog_count": blog_count,
            "post_count": post_count,
            "comment_count": comment_count,
        },
    )


@login_required
def edit_profile(request):
    """Allow users to edit their profile information."""
    # Get the user's profile
    profile = request.user.profile
    if request.method == "POST":
        # Process profile edit form
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to profile detail after saving
            return redirect("accounts:profile_detail", username=request.user.username)
    else:
        # Display profile edit form
        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
            "title": "Edit Profile",
            "cancel_url": reverse(
                "accounts:profile_detail", args=[request.user.username]
            ),
        },
    )
