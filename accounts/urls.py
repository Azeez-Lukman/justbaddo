"""
URL routes for accounts and authentication endpoints.
"""

from django.urls import path
from accounts.views import (
    RegisterView,
    LoginView,
    LogoutView,
    CurrentUserProfileView,
    PublicUserProfileView,
    AccountSettingsView,
    PasswordResetRequestView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', CurrentUserProfileView.as_view(), name='current-profile'),
    path('users/<str:username>/', PublicUserProfileView.as_view(), name='public-profile'),
    path('settings/', AccountSettingsView.as_view(), name='account-settings'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
]
