from core.test_base import JustBaddoTestCase
from rest_framework import status

class ModerationApiTests(JustBaddoTestCase):
    def test_submit_report(self):
        payload = {
            'target_type': 'POST',
            'target_id': 'post-01',
            'reason': 'SPAM',
            'details': 'Automated promotional link'
        }
        res = self.client.post('/api/v1/moderation/report/', data=payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['data']['status'], 'PENDING')

    def test_list_queue(self):
        res = self.client.get('/api/v1/moderation/reports/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 1)

    def test_apply_action(self):
        payload = {
            'report_id': 'rep-001',
            'action': 'REMOVE_CONTENT',
            'notes': 'Violated zero-spam guidelines.'
        }
        res = self.client.post('/api/v1/moderation/action/', data=payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
