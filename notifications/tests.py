from django.test import TestCase
from rest_framework import status

class NotificationsApiTests(TestCase):
    def test_list_notifications(self):
        res = self.client.get('/api/v1/notifications/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 2)

    def test_unread_count(self):
        res = self.client.get('/api/v1/notifications/unread-count/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('unread_count', res.json()['data'])

    def test_mark_read(self):
        res = self.client.post('/api/v1/notifications/notif-01/read/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_mark_all_read(self):
        res = self.client.post('/api/v1/notifications/mark-all-read/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
