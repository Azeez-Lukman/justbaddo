from core.test_base import JustBaddoTestCase
from rest_framework import status

class MusicApiTests(JustBaddoTestCase):
    def test_get_artist_info(self):
        response = self.client.get('/api/v1/music/artist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['name'], 'Olamide Adedeji')

    def test_list_albums(self):
        response = self.client.get('/api/v1/music/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['data']), 5)

    def test_get_album_detail(self):
        response = self.client.get('/api/v1/music/albums/ikigai-vol-1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['title'], 'Ikigai / 生き甲斐, Vol. 1')
        self.assertEqual(len(data['data']['tracks']), 7)

    def test_album_not_found(self):
        response = self.client.get('/api/v1/music/albums/non-existent-album/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_track_detail(self):
        response = self.client.get('/api/v1/music/tracks/iki-07/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['data']['title'], 'Morowore')
        self.assertEqual(data['data']['bpm'], 98)

    def test_catalogue_search(self):
        response = self.client.get('/api/v1/music/search/?q=rapsodi')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['data']['albums']), 1)

    def test_timeline(self):
        response = self.client.get('/api/v1/music/timeline/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data['data']), 5)
