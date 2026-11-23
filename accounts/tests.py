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

