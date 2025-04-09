# Django core imports
from django.shortcuts import render, redirect

# Django authentication imports
from django.contrib.auth.decorators import login_required

# Local app imports
from .forms import AvatarForm, RegistrationForm
from .models import Profile


def register(request):
    """Register a new user."""
    if request.method != "POST":
        # Display empty registration form
        form = RegistrationForm()
    else:
        # Process submitted registration data
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally log the user in automatically here
            return redirect("accounts:login")
    # Prepare context for template rendering
    context = {"form": form}
    return render(request, "accounts/register.html", context)


@login_required
def update_avatar(request):
    """Update the user's avatar image."""
    # Get the current user's profile
    profile = request.user.profile
    if request.method == "POST":
        # Process avatar upload form
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to blogs index after successful upload
            return redirect("blogs:index")
    else:
        # Display avatar upload form with current data
        form = AvatarForm(instance=profile)

    return render(request, "accounts/update_avatar.html", {"form": form})
