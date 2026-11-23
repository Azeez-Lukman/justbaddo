from core.test_base import JustBaddoTestCase
from rest_framework import status
from django.contrib.auth.models import User

class StoriesApiTests(JustBaddoTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.get(username='baddofan99')

    def test_list_stories_public(self):
        res = self.client.get('/api/v1/stories/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 2)

    def test_story_detail_public(self):
        res = self.client.get('/api/v1/stories/story-01/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('content', res.json()['data'])

    def test_submit_story_unauthenticated_fails(self):
        payload = {
            'title': 'My Experience at Teslim Balogun Stadium (OLIC 4)',
            'content': 'Standing under the Lagos night sky with 25,000 other fans singing Wo in unison was an unforgettable life experience.',
            'read_time': '4 min read',
            'tags': 'OLIC, Concerts, Lagos'
        }
        res = self.client.post('/api/v1/stories/submit/', data=payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_submit_story_authenticated(self):
        self.client.force_login(self.user)
        payload = {
            'title': 'My Experience at Teslim Balogun Stadium (OLIC 4)',
            'content': 'Standing under the Lagos night sky with 25,000 other fans singing Wo in unison was an unforgettable life experience.',
            'read_time': '4 min read',
            'tags': 'OLIC, Concerts, Lagos'
        }
        res = self.client.post('/api/v1/stories/submit/', data=payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['data']['status'], 'PENDING_REVIEW')
