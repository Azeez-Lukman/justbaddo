from core.test_base import JustBaddoTestCase
from rest_framework import status
from django.contrib.auth.models import User
from accounts.models import UserProfile
from accounts.services import AccountService

class AccountsApiTests(JustBaddoTestCase):
    def setUp(self):
        super().setUp()
        from django.core.cache import cache
        cache.clear()

    def test_register_user_success(self):
        payload = {
            'username': 'newdisciple',
            'display_name': 'New Disciple',
            'email': 'newdisciple@justbaddo.local',
            'password': 'SecurePassword123!',
            'agree_terms': True,
            'fav_era': 'UY Scuti (2021)'
        }
        response = self.client.post('/api/v1/accounts/register/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['username'], 'newdisciple')
        self.assertEqual(data['data']['display_name'], 'New Disciple')
        self.assertIn('verification', data['data'])

    def test_register_missing_terms_fails(self):
        payload = {
            'username': 'notermsuser',
            'email': 'noterms@justbaddo.local',
            'password': 'SecurePassword123!',
            'agree_terms': False
        }
        response = self.client.post('/api/v1/accounts/register/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username_fails(self):
        payload = {
            'username': 'baddofan99',
            'email': 'anotheremail@justbaddo.local',
            'password': 'SecurePassword123!',
            'agree_terms': True
        }
        response = self.client.post('/api/v1/accounts/register/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json()['errors'])

    def test_register_duplicate_email_fails(self):
        payload = {
            'username': 'uniquename99',
            'email': 'baddofan99@justbaddo.local',
            'password': 'SecurePassword123!',
            'agree_terms': True
        }
        response = self.client.post('/api/v1/accounts/register/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json()['errors'])

    def test_register_weak_password_fails(self):
        payload = {
            'username': 'weakpassuser',
            'email': 'weakpass@justbaddo.local',
            'password': '123',
            'agree_terms': True
        }
        response = self.client.post('/api/v1/accounts/register/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.json()['errors'])

    def test_login_demo_user(self):
        payload = {
            'username_or_email': 'baddofan99',
            'password': 'DemoPassword123!'
        }
        response = self.client.post('/api/v1/accounts/login/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['username'], 'baddofan99')
        self.assertIn('redirect_url', data['data'])

    def test_login_with_email(self):
        payload = {
            'username_or_email': 'baddofan99@justbaddo.local',
            'password': 'DemoPassword123!'
        }
        response = self.client.post('/api/v1/accounts/login/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['username'], 'baddofan99')

    def test_login_invalid_password_rejected(self):
        payload = {
            'username_or_email': 'baddofan99',
            'password': 'WrongPassword999!'
        }
        response = self.client.post('/api/v1/accounts/login/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['code'], 'INVALID_CREDENTIALS')

    def test_login_nonexistent_user_rejected(self):
        payload = {
            'username_or_email': 'ghostuser999',
            'password': 'RandomPassword123!'
        }
        response = self.client.post('/api/v1/accounts/login/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['code'], 'INVALID_CREDENTIALS')

    def test_rate_limiting_enforced_after_repeated_attempts(self):
        # 5 attempts allowed by 'auth_attempt': '5/min'
        for _ in range(5):
            self.client.post('/api/v1/accounts/login/', data={'username_or_email': 'fake', 'password': 'bad'}, content_type='application/json')
        # 6th attempt must be throttled with 429
        resp = self.client.post('/api/v1/accounts/login/', data={'username_or_email': 'fake', 'password': 'bad'}, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_login_safe_redirect_preservation(self):
        payload = {
            'username_or_email': 'baddofan99',
            'password': 'DemoPassword123!',
            'next': '/pages/community.html?post=post-1'
        }
        response = self.client.post('/api/v1/accounts/login/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['redirect_url'], '/pages/community.html?post=post-1')

    def test_login_rejects_open_redirect(self):
        payload = {
            'username_or_email': 'baddofan99',
            'password': 'DemoPassword123!',
            'next': 'https://evil-phishing-site.com/steal'
        }
        response = self.client.post('/api/v1/accounts/login/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['redirect_url'], '/pages/dashboard.html')

    def test_logout_post_invalidates_session(self):
        # First log in
        login_resp = self.client.post('/api/v1/accounts/login/', data={
            'username_or_email': 'baddofan99',
            'password': 'DemoPassword123!'
        }, content_type='application/json')
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)

        # Profile is accessible while authenticated
        prof_resp = self.client.get('/api/v1/accounts/profile/')
        self.assertEqual(prof_resp.status_code, status.HTTP_200_OK)

        # Now logout via POST
        logout_resp = self.client.post('/api/v1/accounts/logout/')
        self.assertEqual(logout_resp.status_code, status.HTTP_200_OK)
        self.assertIn('no-cache', logout_resp['Cache-Control'])

        # Profile is now unauthorized
        prof_after = self.client.get('/api/v1/accounts/profile/')
        self.assertIn(prof_after.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_password_reset_request_nonexistent_email_no_enumeration(self):
        response = self.client.post(
            '/api/v1/accounts/password-reset/',
            data={'email': 'doesnotexist@unknown.com'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'success')

    def test_password_reset_and_confirm_flow(self):
        # 1. Generate reset token for existing user
        user = User.objects.get(username='baddofan99')
        reset_info = AccountService.request_password_reset(user.email)
        self.assertIsNotNone(reset_info)
        uid = reset_info['uid']
        token = reset_info['token']

        # 2. Confirm reset with new strong password
        confirm_resp = self.client.post(
            '/api/v1/accounts/password-reset/confirm/',
            data={
                'uid': uid,
                'token': token,
                'new_password': 'BrandNewPassword999!'
            },
            content_type='application/json'
        )
        self.assertEqual(confirm_resp.status_code, status.HTTP_200_OK)

        # 3. Authenticate with new password
        login_resp = self.client.post('/api/v1/accounts/login/', data={
            'username_or_email': 'baddofan99',
            'password': 'BrandNewPassword999!'
        }, content_type='application/json')
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)

    def test_email_verification_flow(self):
        # 1. Register a new user
        reg_payload = {
            'username': 'verifytester',
            'email': 'verifytester@justbaddo.local',
            'password': 'SecurePassword123!',
            'agree_terms': True
        }
        reg_resp = self.client.post('/api/v1/accounts/register/', data=reg_payload, content_type='application/json')
        self.assertEqual(reg_resp.status_code, status.HTTP_201_CREATED)
        verification = reg_resp.json()['data']['verification']

        # User is initially unverified
        user = User.objects.get(username='verifytester')
        self.assertFalse(user.profile.is_verified)

        # 2. Verify email via endpoint
        verify_resp = self.client.post(
            '/api/v1/accounts/verify-email/',
            data={'uid': verification['uid'], 'token': verification['token']},
            content_type='application/json'
        )
        self.assertEqual(verify_resp.status_code, status.HTTP_200_OK)

        # User profile should now be verified
        user.profile.refresh_from_db()
        self.assertTrue(user.profile.is_verified)

    def test_get_profile(self):
        user = User.objects.get(username='baddofan99')
        self.client.force_login(user)
        response = self.client.get('/api/v1/accounts/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['username'], 'baddofan99')

    def test_get_profile_unauthenticated(self):
        self.client.logout()
        response = self.client.get('/api/v1/accounts/profile/')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_get_public_profile(self):
        response = self.client.get('/api/v1/accounts/users/baddofan99/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['username'], 'baddofan99')

    def test_get_and_update_settings(self):
        response = self.client.get('/api/v1/accounts/settings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        patch_resp = self.client.patch(
            '/api/v1/accounts/settings/',
            data={'auto_advance_queue': False},
            content_type='application/json'
        )
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)
        self.assertFalse(patch_resp.json()['data']['auto_advance_queue'])

    def test_member_directory_public_access(self):
        response = self.client.get('/api/v1/accounts/members/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertGreaterEqual(len(data['data']), 1)
        self.assertIn('meta', data)
        self.assertIn('total_count', data['meta'])
        # Ensure email is never exposed in member directory
        for m in data['data']:
            self.assertNotIn('email', m)

    def test_member_directory_search_and_filter(self):
        response = self.client.get('/api/v1/accounts/members/?q=baddofan99')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(any(m['username'] == 'baddofan99' for m in data['data']))

    def test_badge_list_public_access(self):
        response = self.client.get('/api/v1/accounts/badges/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['data']), 5)
        slugs = [b['slug'] for b in data['data']]
        self.assertIn('first-steps', slugs)
        self.assertIn('conversation-starter', slugs)

    def test_badge_award_idempotency(self):
        from accounts.services import BadgeService
        user = User.objects.get(username='baddofan99')
        # Award badge once
        award1, created1 = BadgeService.award_badge(user, 'first-steps')
        self.assertIsNotNone(award1)
        # Award second time - must be idempotent (created == False)
        award2, created2 = BadgeService.award_badge(user, 'first-steps')
        self.assertFalse(created2)
        self.assertEqual(award1.id, award2.id)

    def test_accept_guidelines_flow(self):
        # 1. Register a user who has not accepted guidelines
        reg_payload = {
            'username': 'guidelineuser',
            'email': 'guideline@justbaddo.local',
            'password': 'SecurePassword123!',
            'agree_terms': True
        }
        self.client.post('/api/v1/accounts/register/', data=reg_payload, content_type='application/json')
        user = User.objects.get(username='guidelineuser')
        self.assertFalse(user.profile.accepted_community_guidelines)

        # 2. Accept guidelines endpoint
        self.client.force_login(user)
        res = self.client.post(
            '/api/v1/accounts/guidelines/accept/',
            data={'accepted': True},
            content_type='application/json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user.profile.refresh_from_db()
        self.assertTrue(user.profile.accepted_community_guidelines)

    def test_profile_privacy_enforcement(self):
        # User sets profile to private
        user = User.objects.get(username='baddofan99')
        user.profile.is_profile_public = False
        user.profile.save()

        # Anonymous guest viewing private profile receives restricted view
        self.client.logout()
        guest_res = self.client.get('/api/v1/accounts/users/baddofan99/')
        self.assertEqual(guest_res.status_code, status.HTTP_200_OK)
        guest_data = guest_res.json()['data']
        self.assertTrue(guest_data.get('is_private'))
        self.assertNotIn('email', guest_data)
        self.assertNotIn('badges', guest_data)

        # Owner viewing their own private profile gets full details
        self.client.force_login(user)
        owner_res = self.client.get('/api/v1/accounts/users/baddofan99/')
        self.assertEqual(owner_res.status_code, status.HTTP_200_OK)
        self.assertIn('badges', owner_res.json()['data'])

        # Reset back to public
        user.profile.is_profile_public = True
        user.profile.save()

    def test_reputation_daily_cap_and_reversal(self):
        from accounts.services import ReputationService
        user = User.objects.get(username='baddofan99')
        initial_score = user.profile.reputation_score

        # Record a 25 point post event
        ev1 = ReputationService.record_event(
            user=user,
            event_type='POST_PUBLISHED',
            source_type='test',
            source_id='test-p1',
            reason='Valuable test post'
        )
        self.assertIsNotNone(ev1)
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.reputation_score, initial_score + 25)

        # Moderator reverses the event
        success, msg = ReputationService.reverse_event(ev1.id, reversed_by=user, reason='Test moderation reversal')
        self.assertTrue(success)
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.reputation_score, initial_score)

    def test_account_deactivation(self):
        # Create a user to deactivate
        user = User.objects.create_user(username='deleteme', email='delete@justbaddo.local', password='Password123!')
        self.client.force_login(user)

        res = self.client.post(
            '/api/v1/accounts/delete/',
            data={'confirm_username': 'deleteme', 'password': 'Password123!'},
            content_type='application/json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertFalse(user.is_active)


class AuthenticationPageAndSessionTests(JustBaddoTestCase):
    """
    Integration tests for dedicated authentication templates, session lifecycle,
    server-side navigation states, and onboarding flows (Section 10).
    """
    def setUp(self):
        super().setUp()
        from django.core.cache import cache
        cache.clear()

    def test_login_page_renders_form(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Welcome Back')
        self.assertContains(response, 'Sign In to Account')
        self.assertContains(response, 'name="username_or_email"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'name="remember_me"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_login_page_post_success_with_username(self):
        response = self.client.post('/accounts/login/', {
            'username_or_email': 'baddofan99',
            'password': 'DemoPassword123!',
            'next': '/pages/music.html'
        })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/pages/music.html')
        # Check user is logged in
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_page_post_success_with_email(self):
        response = self.client.post('/accounts/login/', {
            'username_or_email': 'baddofan99@justbaddo.local',
            'password': 'DemoPassword123!',
            'next': '/pages/community.html'
        })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/pages/community.html')
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_page_post_invalid_credentials_generic_error(self):
        response = self.client.post('/accounts/login/', {
            'username_or_email': 'baddofan99',
            'password': 'WrongPassword123!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Invalid username/email or password.')

    def test_login_page_post_rejects_open_redirect(self):
        response = self.client.post('/accounts/login/', {
            'username_or_email': 'baddofan99',
            'password': 'DemoPassword123!',
            'next': 'https://malicious-external-site.com/exploit'
        })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

    def test_register_page_renders_fields(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Join JustBaddo')
        self.assertContains(response, 'Create Member Account')
        self.assertContains(response, 'name="display_name"')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'name="terms_accepted"')

    def test_register_page_post_success_redirects_to_welcome(self):
        payload = {
            'display_name': 'Tunde Savage',
            'username': 'tundesavage',
            'email': 'tunde@justbaddo.local',
            'password': 'StrongPassword2026!',
            'terms_accepted': 'on',
            'next': '/pages/fan-arena.html'
        }
        response = self.client.post('/accounts/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('/accounts/welcome/?next=/pages/fan-arena.html', response.url)

        # Confirm user created and logged in automatically
        user = User.objects.get(username='tundesavage')
        self.assertEqual(user.email, 'tunde@justbaddo.local')
        self.assertEqual(user.profile.display_name, 'Tunde Savage')
        self.assertIn('_auth_user_id', self.client.session)

    def test_register_page_post_terms_required(self):
        payload = {
            'display_name': 'No Terms User',
            'username': 'notermsuser2',
            'email': 'noterms2@justbaddo.local',
            'password': 'StrongPassword2026!'
        }
        response = self.client.post('/accounts/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'You must accept the Terms of Service and Privacy Policy to create an account.')

    def test_register_page_post_duplicate_username_rejected(self):
        payload = {
            'display_name': 'Duplicate User',
            'username': 'baddofan99',
            'email': 'differentemail@justbaddo.local',
            'password': 'StrongPassword2026!',
            'terms_accepted': 'on'
        }
        response = self.client.post('/accounts/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'This username is already taken.')

    def test_register_page_post_duplicate_email_rejected(self):
        payload = {
            'display_name': 'Duplicate User',
            'username': 'uniquehandle42',
            'email': 'baddofan99@justbaddo.local',
            'password': 'StrongPassword2026!',
            'terms_accepted': 'on'
        }
        response = self.client.post('/accounts/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'An account with this email address already exists.')

    def test_signout_rejects_get_with_405(self):
        """Section 5 strictly mandates: Instant POST-only sign-out with CSRF protection. Never implement logout as a GET action."""
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_signout_post_invalidates_session_and_clears_cache(self):
        # Authenticate first
        user = User.objects.get(username='baddofan99')
        self.client.force_login(user)
        self.assertIn('_auth_user_id', self.client.session)

        # POST to sign-out
        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

        # Verify session is flushed
        self.assertNotIn('_auth_user_id', self.client.session)

        # Verify Cache-Control headers prevent browser back navigation
        self.assertIn('no-cache', response['Cache-Control'])
        self.assertIn('no-store', response['Cache-Control'])
        self.assertEqual(response['Pragma'], 'no-cache')

    def test_forgot_password_page_flow_and_no_enumeration(self):
        get_resp = self.client.get('/accounts/forgot-password/')
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)
        self.assertContains(get_resp, 'Forgot Password')

        # POST with non-existent email gives uniform confirmation
        post_unknown = self.client.post('/accounts/forgot-password/', {'email': 'nonexistent@nowhere.com'})
        self.assertEqual(post_unknown.status_code, status.HTTP_200_OK)
        self.assertContains(post_unknown, 'Recovery Instructions Dispatched')

        # POST with existing email gives same uniform confirmation
        post_existing = self.client.post('/accounts/forgot-password/', {'email': 'baddofan99@justbaddo.local'})
        self.assertEqual(post_existing.status_code, status.HTTP_200_OK)
        self.assertContains(post_existing, 'Recovery Instructions Dispatched')

    def test_reset_password_page_flow(self):
        user = User.objects.get(username='baddofan99')
        reset_info = AccountService.request_password_reset(user.email)
        uid = reset_info['uid']
        token = reset_info['token']

        # GET reset password with valid token
        get_valid = self.client.get(f'/accounts/reset-password/?uid={uid}&token={token}')
        self.assertEqual(get_valid.status_code, status.HTTP_200_OK)
        self.assertContains(get_valid, 'name="new_password"')

        # GET reset password with invalid token
        get_invalid = self.client.get(f'/accounts/reset-password/?uid={uid}&token=invalid-token-xyz')
        self.assertEqual(get_invalid.status_code, status.HTTP_200_OK)
        self.assertContains(get_invalid, 'Invalid or Expired Reset Link')

        # POST reset password with matching valid password
        post_resp = self.client.post(f'/accounts/reset-password/?uid={uid}&token={token}', {
            'new_password': 'BrandNewPass2026!',
            'confirm_password': 'BrandNewPass2026!'
        })
        self.assertEqual(post_resp.status_code, status.HTTP_200_OK)
        self.assertContains(post_resp, 'Password Successfully Updated')

        # Verify new password can authenticate
        login_res = self.client.post('/accounts/login/', {
            'username_or_email': 'baddofan99',
            'password': 'BrandNewPass2026!'
        })
        self.assertEqual(login_res.status_code, status.HTTP_302_FOUND)

    def test_verify_email_page_flow(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator

        # Create unverified user with profile
        new_user = User.objects.create_user(username='unverifiedguy', email='unverified@justbaddo.local', password='Password123!')
        UserProfile.objects.create(user=new_user, is_verified=False)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))
        token = default_token_generator.make_token(new_user)

        # GET with valid verification token
        verify_resp = self.client.get(f'/accounts/verify-email/?uid={uid}&token={token}')
        self.assertEqual(verify_resp.status_code, status.HTTP_200_OK)
        self.assertContains(verify_resp, 'Email Verified!')

        new_user.profile.refresh_from_db()
        self.assertTrue(new_user.profile.is_verified)

        # GET with invalid token
        bad_resp = self.client.get(f'/accounts/verify-email/?uid={uid}&token=wrongtoken')
        self.assertEqual(bad_resp.status_code, status.HTTP_200_OK)
        self.assertContains(bad_resp, 'Verification Failed')

    def test_resend_verification_page_post(self):
        resp = self.client.post('/accounts/resend-verification/', {'email': 'baddofan99@justbaddo.local'})
        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)
        self.assertEqual(resp.url, '/accounts/verify-email/')

    def test_welcome_onboarding_save_and_skip(self):
        user = User.objects.get(username='baddofan99')
        self.client.force_login(user)

        # GET welcome page
        get_welcome = self.client.get('/accounts/welcome/?next=/pages/timeline.html')
        self.assertEqual(get_welcome.status_code, status.HTTP_200_OK)
        self.assertContains(get_welcome, 'Welcome to the Family')
        self.assertContains(get_welcome, 'Optional Profile Personalisation')

        # POST action='save' with preferences
        post_save = self.client.post('/accounts/welcome/', {
            'action': 'save',
            'next': '/pages/timeline.html',
            'country': 'Nigeria',
            'bio': 'Day-one Olamide enthusiast from Bariga.',
            'favorite_album': 'Time and Space (2026)',
            'favorite_track': 'Infinity'
        })
        self.assertEqual(post_save.status_code, status.HTTP_302_FOUND)
        self.assertEqual(post_save.url, '/pages/timeline.html')

        user.profile.refresh_from_db()
        self.assertEqual(user.profile.country, 'Nigeria')
        self.assertEqual(user.profile.favorite_album, 'Time and Space (2026)')
        self.assertEqual(user.profile.favorite_track, 'Infinity')
        self.assertEqual(user.profile.bio, 'Day-one Olamide enthusiast from Bariga.')

        # POST action='skip'
        post_skip = self.client.post('/accounts/welcome/', {
            'action': 'skip',
            'next': '/pages/community.html'
        })
        self.assertEqual(post_skip.status_code, status.HTTP_302_FOUND)
        self.assertEqual(post_skip.url, '/pages/community.html')

    def test_server_side_navigation_guest_vs_authenticated(self):
        # 1. Unauthenticated guest visiting homepage
        self.client.logout()
        guest_home = self.client.get('/')
        self.assertEqual(guest_home.status_code, status.HTTP_200_OK)
        # Guest sees Sign In and Join JustBaddo links
        self.assertContains(guest_home, '/accounts/login/')
        self.assertContains(guest_home, '/accounts/register/')
        # Guest does not see member monogram or sign-out form
        self.assertNotContains(guest_home, '/accounts/logout/')

        # 2. Authenticated member visiting homepage
        user = User.objects.get(username='baddofan99')
        self.client.force_login(user)
        member_home = self.client.get('/')
        self.assertEqual(member_home.status_code, status.HTTP_200_OK)
        # Member sees their initials monogram or display name
        self.assertContains(member_home, user.profile.initials)
        # Member navigation includes the POST sign-out form
        self.assertContains(member_home, '/accounts/logout/')


