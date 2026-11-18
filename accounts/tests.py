from django.test import TestCase
from rest_framework import status

class AccountsApiTests(TestCase):
    def test_register_user_success(self):
        payload = {
            'username': 'newdisciple',
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

    def test_register_missing_terms_fails(self):
        payload = {
            'username': 'notermsuser',
            'email': 'noterms@justbaddo.local',
            'password': 'SecurePassword123!',
            'agree_terms': False
        }
        response = self.client.post('/api/v1/accounts/register/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_demo_user(self):
        payload = {
            'username_or_email': 'baddofan99',
            'password': 'any-password'
        }
        response = self.client.post('/api/v1/accounts/login/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['username'], 'baddofan99')

    def test_get_profile(self):
        response = self.client.get('/api/v1/accounts/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['username'], 'baddofan99')

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
