"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from users.views import ChangePasswordView
from users.views import LoginView
from users.views import ResendInvitationView
from users.views import UserProfileView

from backend.views import LandingView
from backend.views import PasswordResetView

app_name = "backend"

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("quotations/", include("quotations.urls")),
    path("product-or-part-numbers/", include("technologyoptions.urls")),
    path("settings/", include("settings.urls")),
    path("accounts/login/", LoginView.as_view(), name="user-login"),
    path("accounts/profile/", UserProfileView.as_view(), name="user-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path(
        "users/resend-invitation/<int:pk>/",
        ResendInvitationView.as_view(),
        name="resend-invitation",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
