from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class CoreApiTests(TestCase):
    def test_health_check(self):
        response = self.client.get('/api/v1/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['status'], 'healthy')
        self.assertEqual(data['data']['service'], 'justbaddo-backend')

    def test_platform_metadata(self):
        response = self.client.get('/api/v1/platform/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('Olamide', data['data']['artist'])
        self.assertIn('Phase 2', data['data']['active_phase'])
