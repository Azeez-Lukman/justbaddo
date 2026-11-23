"""
API views for user accounts, registration, login, logout, password recovery,
member directory, public profiles, badges, reputation, and preferences.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import status
from django.contrib.auth import login, logout

from core.response import api_success, api_error
from accounts.serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
    UserProfileSerializer,
    ProfileUpdateSerializer,
    AccountSettingsSerializer,
    AcceptGuidelinesSerializer,
    AccountDeleteSerializer,
    BadgeSerializer
)
from accounts.services import AccountService, BadgeService, MemberDirectoryService

class RegisterView(APIView):
    """
    Register a new user account.
    POST /api/v1/accounts/register/
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth_attempt'

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
            display_name=data.get('display_name'),
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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth_attempt'

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

        if not auth_result or not auth_result.get('user'):
            return api_error(
                message="Invalid username/email or password.",
                code="INVALID_CREDENTIALS",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        user = auth_result['user']
        # Django's login() cycles session key automatically to prevent session fixation
        login(request, user)

        # Session expiry based on remember_me
        remember_me = data.get('remember_me', False)
        if remember_me:
            request.session.set_expiry(1209600)  # 2 weeks
        else:
            request.session.set_expiry(0)  # Session expires on browser close

        # Safe return destination preservation
        safe_redirect = AccountService.validate_safe_redirect(
            redirect_url=data.get('next'),
            request=request,
            default='/pages/dashboard.html'
        )

        response_data = {
            'profile': auth_result['profile'],
            'redirect_url': safe_redirect,
            **auth_result['profile']
        }

        return api_success(
            data=response_data,
            message="Login successful."
        )

class LogoutView(APIView):
    """
    Log out currently authenticated user.
    POST /api/v1/accounts/logout/
    Enforces POST-only method, invalidates session, flushes CSRF and adds Cache-Control headers.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            request.session.flush()

        response = api_success(message="Successfully logged out.")
        # Ensure browser back navigation cannot reveal cached private content
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class PasswordResetRequestView(APIView):
    """
    Request password reset instructions.
    POST /api/v1/accounts/password-reset/
    Always returns uniform success message to prevent user enumeration.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth_attempt'

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid email address.", code="VALIDATION_ERROR", errors=serializer.errors)

        email = serializer.validated_data['email']
        AccountService.request_password_reset(email)

        return api_success(
            message="If an account exists with this email, password reset instructions have been dispatched."
        )

class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with uid and token.
    POST /api/v1/accounts/password-reset/confirm/
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth_attempt'

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid reset details.", code="VALIDATION_ERROR", errors=serializer.errors)

        data = serializer.validated_data
        success, msg = AccountService.confirm_password_reset(
            uidb64=data['uid'],
            token=data['token'],
            new_password=data['new_password']
        )

        if not success:
            return api_error(message=msg, code="RESET_FAILED", status_code=status.HTTP_400_BAD_REQUEST)

        return api_success(message=msg)

class EmailVerificationView(APIView):
    """
    Verify member email address with uid and token.
    POST /api/v1/accounts/verify-email/
    GET /api/v1/accounts/verify-email/
    """
    permission_classes = [AllowAny]

    def _verify(self, uid, token):
        success, msg = AccountService.verify_email_token(uidb64=uid, token=token)
        if not success:
            return api_error(message=msg, code="VERIFICATION_FAILED", status_code=status.HTTP_400_BAD_REQUEST)
        return api_success(message=msg)

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid verification parameters.", code="VALIDATION_ERROR", errors=serializer.errors)
        return self._verify(serializer.validated_data['uid'], serializer.validated_data['token'])

    def get(self, request):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        if not uid or not token:
            return api_error(message="Missing uid or token parameter.", code="VALIDATION_ERROR", status_code=status.HTTP_400_BAD_REQUEST)
        return self._verify(uid, token)

class CurrentUserProfileView(APIView):
    """
    Retrieve or update currently logged in user profile.
    GET /api/v1/accounts/profile/
    PATCH /api/v1/accounts/profile/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = AccountService.get_profile(request.user.username, viewer=request.user)
        if not profile:
            return api_error(message="Profile not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)
        return api_success(data=profile)

    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return api_error(message="Invalid profile update data.", code="VALIDATION_ERROR", errors=serializer.errors)

        updated = AccountService.update_profile(request.user.username, serializer.validated_data)
        return api_success(data=updated, message="Profile updated successfully.")

class PublicUserProfileView(APIView):
    """
    Retrieve any fan profile by username.
    Respects privacy controls (is_profile_public) and masks private details for guests/other users.
    GET /api/v1/accounts/users/<username>/
    """
    permission_classes = [AllowAny]

    def get(self, request, username):
        viewer = request.user if request.user.is_authenticated else None
        profile = AccountService.get_profile(username, viewer=viewer)
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

    def put(self, request):
        return self.patch(request)

class MemberDirectoryView(APIView):
    """
    List public JustBaddo members with filtering, search, and pagination.
    GET /api/v1/accounts/members/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q')
        tier = request.query_params.get('tier')
        badge_slug = request.query_params.get('badge')
        ordering = request.query_params.get('ordering', '-reputation_score')
        
        try:
            page = int(request.query_params.get('page', 1))
            page_size = min(int(request.query_params.get('page_size', 20)), 100)
        except (ValueError, TypeError):
            page = 1
            page_size = 20

        result = MemberDirectoryService.list_members(
            query=query,
            tier=tier,
            badge_slug=badge_slug,
            ordering=ordering,
            page=page,
            page_size=page_size
        )
        return api_success(data=result['members'], meta=result['meta'])

class BadgeListView(APIView):
    """
    List all active fan badges available on the platform.
    GET /api/v1/accounts/badges/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        badges = BadgeService.get_all_badges()
        serializer = BadgeSerializer(badges, many=True)
        return api_success(data=serializer.data, meta={'count': len(badges)})

class AcceptGuidelinesView(APIView):
    """
    Accept JustBaddo community guidelines before first contribution.
    POST /api/v1/accounts/guidelines/accept/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AcceptGuidelinesSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid guidelines submission.", code="VALIDATION_ERROR", errors=serializer.errors)

        success, msg = AccountService.accept_guidelines(request.user)
        if not success:
            return api_error(message=msg, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST)
        return api_success(message=msg)

class AccountDeleteView(APIView):
    """
    Deactivate account and invalidate sessions upon user request.
    POST /api/v1/accounts/delete/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AccountDeleteSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid account deletion payload.", code="VALIDATION_ERROR", errors=serializer.errors)

        if serializer.validated_data['confirm_username'].lower() != request.user.username.lower():
            return api_error(message="Confirmed username does not match current user.", code="CONFIRMATION_MISMATCH", status_code=status.HTTP_400_BAD_REQUEST)

        success, msg = AccountService.deactivate_account(request.user, serializer.validated_data['password'])
        if not success:
            return api_error(message=msg, code="DEACTIVATION_FAILED", status_code=status.HTTP_400_BAD_REQUEST)

        logout(request)
        request.session.flush()

        response = api_success(message="Your account has been deactivated successfully.")
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        return response
