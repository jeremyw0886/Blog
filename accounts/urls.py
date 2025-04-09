# Django configuration imports
from django.conf import settings
from django.conf.urls.static import static

# Django URL imports
from django.urls import path

# Django authentication imports
from django.contrib.auth import views as auth_views

# Local app imports
from . import views

# Namespace for URL patterns
app_name = "accounts"

urlpatterns = [
    # User registration endpoint
    path("register/", views.register, name="register"),
    # User login endpoint with custom template
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    # User logout endpoint
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Endpoint for updating user avatar
    path("update-avatar/", views.update_avatar, name="update_avatar"),
    # Profile view with username parameter
    path("profile/<str:username>/", views.profile_detail, name="profile_detail"),
    # Default profile view (current user)
    path("profile/", views.profile_detail, name="profile"),
    # Endpoint for editing profile
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    # Password change endpoint with custom template
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/change_password.html",
            success_url="/accounts/password-changed/",
        ),
        name="change_password",
    ),
    # Password change confirmation view
    path(
        "password-changed/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_changed.html"
        ),
        name="password_changed",
    ),
]

"""
Configures static file serving in development mode.
Only active when DEBUG is True in settings.
"""
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
