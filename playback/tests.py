from django.test import TestCase
from rest_framework import status

class PlaybackApiTests(TestCase):
    def test_check_playable_track(self):
        response = self.client.get('/api/v1/playback/check/iki-01/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data['data']['can_play'])
        self.assertEqual(data['data']['status'], 'JUSTBADDO_STREAMING')

    def test_check_metadata_only_track(self):
        response = self.client.get('/api/v1/playback/check/rap-04/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertFalse(data['data']['can_play'])
        self.assertEqual(data['data']['status'], 'METADATA_ONLY')

    def test_session_init_playable(self):
        payload = {'track_id': 'iki-01', 'client_provider': 'mock_synth'}
        response = self.client.post('/api/v1/playback/session/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn('session_id', data['data'])

    def test_session_init_restricted_fails(self):
        payload = {'track_id': 'rap-04', 'client_provider': 'mock_synth'}
        response = self.client.post('/api/v1/playback/session/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_log_playback(self):
        payload = {'track_id': 'iki-01', 'duration_seconds': 140, 'completed_listen': True}
        response = self.client.post('/api/v1/playback/log/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
