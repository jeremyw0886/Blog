"""
URL configuration for Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add鉄 an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Django admin imports
from django.contrib import admin

# Django URL imports
from django.urls import include, path

# Django configuration imports
from django.conf import settings
from django.conf.urls.static import static


# Main URL patterns for the project
urlpatterns = [
    # Admin site URLs
    path("admin/", admin.site.urls),
    # Accounts app URL patterns with namespace
    path("accounts/", include("accounts.urls", namespace="accounts")),
    # Blogs app URL patterns with namespace
    path("", include("blogs.urls", namespace="blogs")),
]

"""
Serve media files in development mode.
Only active when DEBUG is True in settings.
"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
