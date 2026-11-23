"""
URL routes for accounts, authentication, public profiles, members, badges, and guidelines.
"""

from django.urls import path
from accounts.views import (
    RegisterView,
    LoginView,
    LogoutView,
    CurrentUserProfileView,
    PublicUserProfileView,
    AccountSettingsView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    EmailVerificationView,
    MemberDirectoryView,
    BadgeListView,
    AcceptGuidelinesView,
    AccountDeleteView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', CurrentUserProfileView.as_view(), name='current-profile'),
    path('members/', MemberDirectoryView.as_view(), name='members-directory'),
    path('badges/', BadgeListView.as_view(), name='badges-list'),
    path('guidelines/accept/', AcceptGuidelinesView.as_view(), name='accept-guidelines'),
    path('delete/', AccountDeleteView.as_view(), name='account-delete'),
    path('users/<str:username>/', PublicUserProfileView.as_view(), name='public-profile'),
    path('settings/', AccountSettingsView.as_view(), name='account-settings'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
]
