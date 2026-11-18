from core.test_base import JustBaddoTestCase
from rest_framework import status

class CommunityApiTests(JustBaddoTestCase):
    def test_list_posts(self):
        response = self.client.get('/api/v1/community/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['data']), 1)

    def test_filter_by_category(self):
        response = self.client.get('/api/v1/community/posts/?category=Discography')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        for p in data['data']:
            self.assertEqual(p['category'], 'Discography')

    def test_create_post(self):
        payload = {
            'title': 'Is YBNL the greatest African hip-hop movement?',
            'category': 'General Fan Chat',
            'content': 'Looking back across the last 12 years of talent incubated under the label.'
        }
        res = self.client.post('/api/v1/community/posts/', data=payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['data']['title'], payload['title'])

    def test_post_comment(self):
        payload = {'content': 'Completely agree with this breakdown!'}
        res = self.client.post('/api/v1/community/posts/post-01/comments/', data=payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_toggle_like(self):
        res = self.client.post('/api/v1/community/posts/post-01/like/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('likes', res.json()['data'])
