"""
API views for user accounts, registration, login, logout, and profile management.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import login, logout

from core.response import api_success, api_error
from accounts.serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    UserProfileSerializer,
    ProfileUpdateSerializer,
    AccountSettingsSerializer
)
from accounts.services import AccountService

class RegisterView(APIView):
    """
    Register a new user account.
    POST /api/v1/accounts/register/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(
                message="Validation failed for registration.",
                code="VALIDATION_ERROR",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        profile = AccountService.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            fav_era=data.get('fav_era', 'Carpe Diem (2020)')
        )

        return api_success(
            data=profile,
            message="User registration successful. Welcome to JustBaddo!",
            status_code=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    """
    Authenticate and log in a user.
    POST /api/v1/accounts/login/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(
                message="Invalid login request payload.",
                code="VALIDATION_ERROR",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        auth_result = AccountService.authenticate_user(
            username_or_email=data['username_or_email'],
            password=data['password']
        )

        if not auth_result:
            return api_error(
                message="Invalid username/email or password.",
                code="INVALID_CREDENTIALS",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        if auth_result.get('user'):
            login(request, auth_result['user'])

        return api_success(
            data=auth_result['profile'],
            message="Login successful."
        )

class LogoutView(APIView):
    """
    Log out currently authenticated user.
    POST /api/v1/accounts/logout/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return api_success(message="Successfully logged out.")

class CurrentUserProfileView(APIView):
    """
    Retrieve or update currently logged in user profile.
    GET /api/v1/accounts/profile/
    PATCH /api/v1/accounts/profile/
    """
    permission_classes = [AllowAny]  # Supports demo user fallback if unauthenticated

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        profile = AccountService.get_profile(username)
        if not profile:
            return api_error(message="Profile not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)
        return api_success(data=profile)

    def patch(self, request):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_error(message="Invalid profile update data.", code="VALIDATION_ERROR", errors=serializer.errors)

        updated = AccountService.update_profile(username, serializer.validated_data)
        return api_success(data=updated, message="Profile updated successfully.")

class PublicUserProfileView(APIView):
    """
    Retrieve any fan profile by username.
    GET /api/v1/accounts/users/<username>/
    """
    permission_classes = [AllowAny]

    def get(self, request, username):
        profile = AccountService.get_profile(username)
        if not profile:
            return api_error(message=f"Fan profile '@{username}' not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)
        return api_success(data=profile)

class AccountSettingsView(APIView):
    """
    Retrieve or update user account preferences.
    GET /api/v1/accounts/settings/
    PATCH /api/v1/accounts/settings/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        user_settings = AccountService.get_settings(username)
        return api_success(data=user_settings)

    def patch(self, request):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        serializer = AccountSettingsSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_error(message="Invalid settings payload.", code="VALIDATION_ERROR", errors=serializer.errors)

        updated = AccountService.update_settings(username, serializer.validated_data)
        return api_success(data=updated, message="Settings updated successfully.")

class PasswordResetRequestView(APIView):
    """
    Request password reset instructions.
    POST /api/v1/accounts/password-reset/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid email address.", code="VALIDATION_ERROR", errors=serializer.errors)

        return api_success(
            message="If an account exists with this email, password reset instructions have been dispatched."
        )
