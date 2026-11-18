from core.test_base import JustBaddoTestCase
from rest_framework import status

class PlaylistsApiTests(JustBaddoTestCase):
    def test_list_playlists(self):
        response = self.client.get('/api/v1/playlists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['data']), 2)

    def test_create_and_delete_playlist(self):
        create_payload = {
            'title': 'Test Night Drive',
            'description': 'Smooth tunes for late nights',
            'is_private': False
        }
        res = self.client.post('/api/v1/playlists/', data=create_payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        pl_id = res.json()['data']['id']

        # Add track
        add_res = self.client.post(f'/api/v1/playlists/{pl_id}/tracks/', data={'track_id': 'iki-01'}, content_type='application/json')
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)

        # Get detail
        detail_res = self.client.get(f'/api/v1/playlists/{pl_id}/')
        self.assertEqual(detail_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(detail_res.json()['data']['tracks']), 1)

        # Delete
        del_res = self.client.delete(f'/api/v1/playlists/{pl_id}/')
        self.assertEqual(del_res.status_code, status.HTTP_200_OK)
