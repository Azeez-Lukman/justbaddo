"""
API views for user accounts, registration, login, logout, password recovery,
member directory, public profiles, badges, reputation, and preferences.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import status
from django.contrib.auth import login, logout
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed

from accounts.forms import (
    LoginForm,
    RegistrationForm,
    PasswordResetRequestForm,
    SetPasswordForm,
    WelcomePersonalisationForm
)

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


# ==============================================================================
# DEDICATED TEMPLATE VIEWS (FULL AUTHENTICATION SUITE & SESSION LIFECYCLE)
# ==============================================================================

class AccountLoginTemplateView(View):
    """
    Renders the dedicated Sign In page (/accounts/login/) with inline validation,
    session fixation protection, safe next destination preservation, and remember_me.
    """
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            safe_next = AccountService.validate_safe_redirect(request.GET.get('next'), request, default='/')
            return redirect(safe_next)

        next_url = request.GET.get('next', '')
        form = LoginForm(initial={'next': next_url})
        return render(request, self.template_name, {
            'form': form,
            'next_url': next_url,
            'user': request.user,
            'is_authenticated': request.user.is_authenticated
        })

    def post(self, request):
        form = LoginForm(request.POST)
        next_url = request.POST.get('next', '')

        if form.is_valid():
            identifier = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            auth_result = AccountService.authenticate_user(
                username_or_email=identifier,
                password=password
            )

            if auth_result and auth_result.get('user'):
                user = auth_result['user']
                # Django's login() cycles session key automatically to prevent session fixation
                login(request, user)

                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser session

                safe_next = AccountService.validate_safe_redirect(
                    form.cleaned_data.get('next'),
                    request,
                    default='/'
                )

                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                    return JsonResponse({'status': 'success', 'redirect_url': safe_next, 'message': 'Login successful.'})

                messages.success(request, f"Welcome back, {user.profile.display_name or user.username}!")
                return redirect(safe_next)
            else:
                form.add_error(None, "Invalid username/email or password.")
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                    return JsonResponse({'status': 'error', 'message': 'Invalid username/email or password.'}, status=401)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        return render(request, self.template_name, {
            'form': form,
            'next_url': next_url,
            'user': request.user,
            'is_authenticated': request.user.is_authenticated
        })


class AccountRegisterTemplateView(View):
    """
    Renders dedicated Registration page (/accounts/register/).
    Creates single unified member account across platform & community with zero duplicate registration.
    """
    template_name = 'accounts/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')

        next_url = request.GET.get('next', '')
        form = RegistrationForm(initial={'next': next_url})
        return render(request, self.template_name, {
            'form': form,
            'next_url': next_url,
            'user': request.user,
            'is_authenticated': request.user.is_authenticated
        })

    def post(self, request):
        form = RegistrationForm(request.POST)
        next_url = request.POST.get('next', '')

        if form.is_valid():
            data = form.cleaned_data
            clean_username = data['username'].strip().lower()

            AccountService.register_user(
                username=clean_username,
                email=data['email'].strip().lower(),
                password=data['password'],
                display_name=data.get('display_name')
            )

            user = User.objects.get(username=clean_username)
            login(request, user)

            safe_next = AccountService.validate_safe_redirect(data.get('next'), request, default='/')
            welcome_target = f"/accounts/welcome/?next={safe_next}"

            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                return JsonResponse({'status': 'success', 'redirect_url': welcome_target})

            return redirect(welcome_target)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        return render(request, self.template_name, {
            'form': form,
            'next_url': next_url,
            'user': request.user,
            'is_authenticated': request.user.is_authenticated
        })


class AccountSignoutTemplateView(View):
    """
    Sign out currently authenticated user.
    Enforces POST-only method with CSRF protection. Invalidate session and clears private cache.
    Rejects GET requests per security specifications.
    """
    def get(self, request):
        # Explicitly reject GET requests with Method Not Allowed per Section 5 requirements
        return HttpResponseNotAllowed(['POST'])

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            request.session.flush()

        messages.info(request, "You've been signed out.")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            response = JsonResponse({'status': 'success', 'message': "You've been signed out.", 'redirect_url': '/'})
        else:
            response = redirect('/')

        # Ensure browser back navigation cannot reveal cached private content
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class AccountForgotPasswordTemplateView(View):
    """
    Renders password recovery page (/accounts/forgot-password/).
    Uses generic confirmation responses to defend against user enumeration.
    """
    template_name = 'accounts/forgot_password.html'

    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, self.template_name, {'form': form, 'submitted': False})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            AccountService.request_password_reset(form.cleaned_data['email'])

        # Always show uniform success state to prevent account enumeration
        return render(request, self.template_name, {'form': PasswordResetRequestForm(), 'submitted': True})


class AccountResetPasswordTemplateView(View):
    """
    Renders and processes password reset form (/accounts/reset-password/).
    Validates token and handles expired/invalid links safely.
    """
    template_name = 'accounts/reset_password.html'

    def _get_user_and_validate(self, uidb64, token):
        if not uidb64 or not token:
            return None, False
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            is_valid = default_token_generator.check_token(user, token)
            return user, is_valid
        except Exception:
            return None, False

    def get(self, request):
        uid = request.GET.get('uid', '')
        token = request.GET.get('token', '')
        user, is_valid = self._get_user_and_validate(uid, token)

        form = SetPasswordForm() if is_valid else None
        return render(request, self.template_name, {
            'form': form,
            'valid_token': is_valid,
            'reset_success': False,
            'uid': uid,
            'token': token
        })

    def post(self, request):
        uid = request.GET.get('uid', '')
        token = request.GET.get('token', '')
        user, is_valid = self._get_user_and_validate(uid, token)

        if not is_valid:
            return render(request, self.template_name, {
                'form': None,
                'valid_token': False,
                'reset_success': False
            })

        form = SetPasswordForm(request.POST)
        if form.is_valid():
            success, msg = AccountService.confirm_password_reset(
                uidb64=uid,
                token=token,
                new_password=form.cleaned_data['new_password']
            )
            if success:
                return render(request, self.template_name, {
                    'form': None,
                    'valid_token': True,
                    'reset_success': True
                })
            else:
                form.add_error(None, msg)

        return render(request, self.template_name, {
            'form': form,
            'valid_token': True,
            'reset_success': False,
            'uid': uid,
            'token': token
        })


class AccountVerifyEmailTemplateView(View):
    """
    Handles email verification links (/accounts/verify-email/).
    """
    template_name = 'accounts/verify_email.html'

    def get(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        next_url = request.GET.get('next', '/')

        if uid and token:
            success, msg = AccountService.verify_email_token(uidb64=uid, token=token)
            return render(request, self.template_name, {
                'verified': success,
                'error_message': None if success else msg,
                'next_url': next_url
            })

        return render(request, self.template_name, {
            'verified': False,
            'error_message': None,
            'next_url': next_url
        })


class AccountResendVerificationView(View):
    """
    Resends verification email with rate limiting.
    """
    def post(self, request):
        email = request.POST.get('email', '').strip()
        if email:
            AccountService.resend_verification_email(email)

        messages.info(request, "If an unverified account exists with this email, fresh verification instructions have been dispatched.")
        return redirect('/accounts/verify-email/')


class AccountWelcomeTemplateView(View):
    """
    Welcomes newly registered members and offers optional profile personalisation.
    Members may choose to personalise immediately or skip and continue.
    """
    template_name = 'accounts/welcome.html'

    def get(self, request):
        next_url = request.GET.get('next', '/')
        form = WelcomePersonalisationForm()
        return render(request, self.template_name, {
            'form': form,
            'next_url': next_url
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        action = request.POST.get('action', 'skip')
        next_url = request.POST.get('next', '/')
        safe_next = AccountService.validate_safe_redirect(next_url, request, default='/')

        if action == 'save' and hasattr(request.user, 'profile'):
            profile = request.user.profile
            country = request.POST.get('country', '').strip()
            bio = request.POST.get('bio', '').strip()
            fav_album = request.POST.get('favorite_album', '').strip()
            fav_track = request.POST.get('favorite_track', '').strip()

            if country:
                profile.country = country
            if bio:
                profile.bio = bio
            if fav_album:
                profile.favorite_album = fav_album
            if fav_track:
                profile.favorite_track = fav_track
            profile.save()

            messages.success(request, "Your profile preferences have been saved!")

        return redirect(safe_next)
