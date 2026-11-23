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

    def test_time_and_space_catalogue_integration(self):
        # 1. Album detail
        res = self.client.get('/api/v1/music/albums/time-and-space/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        album = res.json()['data']
        self.assertEqual(album['title'], 'Time and Space')
        self.assertEqual(album['releaseYear'], 2026)
        self.assertEqual(album['label'], 'YBNL Nation / EMPIRE')

        # 2. Verify exactly 10 tracks
        tracks = album['tracks']
        self.assertEqual(len(tracks), 10)

        expected_titles = [
            'Elohim', 'Skoskola', 'Say Less', 'Burukutu', 'Alujon',
            'Mbiri', 'Jaiye', 'Oshey', 'Ring', 'Jogor'
        ]
        for idx, expected in enumerate(expected_titles):
            self.assertEqual(tracks[idx]['number'], idx + 1)
            self.assertEqual(tracks[idx]['title'], expected)

        # 3. Verify FOLA is featured on track 7 (Jaiye) ONLY
        self.assertEqual(tracks[6]['title'], 'Jaiye')
        self.assertIn('FOLA', tracks[6]['featured'])
        for idx, trk in enumerate(tracks):
            if idx != 6:
                self.assertNotIn('FOLA', trk.get('featured', ''))

