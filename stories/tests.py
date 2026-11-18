from core.test_base import JustBaddoTestCase
from rest_framework import status

class StoriesApiTests(JustBaddoTestCase):
    def test_list_stories(self):
        res = self.client.get('/api/v1/stories/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 2)

    def test_story_detail(self):
        res = self.client.get('/api/v1/stories/story-01/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('content', res.json()['data'])

    def test_submit_story(self):
        payload = {
            'title': 'My Experience at Teslim Balogun Stadium (OLIC 4)',
            'content': 'Standing under the Lagos night sky with 25,000 other fans singing Wo in unison was an unforgettable life experience.',
            'read_time': '4 min read',
            'tags': 'OLIC, Concerts, Lagos'
        }
        res = self.client.post('/api/v1/stories/submit/', data=payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['data']['status'], 'PENDING_REVIEW')
