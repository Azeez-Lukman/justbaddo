from core.test_base import JustBaddoTestCase
from rest_framework import status

class LicensingApiTests(JustBaddoTestCase):
    def test_list_rights_records(self):
        res = self.client.get('/api/v1/licensing/rights/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 2)

    def test_rights_detail(self):
        res = self.client.get('/api/v1/licensing/rights/iki-01/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(res.json()['data']['licensing_status'], ['licensed', 'permission_requested'])

    def test_submit_rights_inquiry(self):
        payload = {
            'claimant_name': 'A&R Department',
            'organization': 'Legal Reps',
            'email': 'legal@licensing-reps.com',
            'track_or_album': 'Metaverse',
            'inquiry_type': 'LICENSING_OFFER',
            'message': 'Proposal regarding statutory mechanical and digital preview clearance terms.'
        }
        res = self.client.post('/api/v1/licensing/inquiry/', data=payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['data']['status'], 'PENDING_LEGAL_REVIEW')
