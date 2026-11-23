from core.test_base import JustBaddoTestCase
from rest_framework import status
from django.contrib.auth.models import User

class ArenaApiTests(JustBaddoTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.get(username='baddofan99')

    def test_list_polls_public_access(self):
        res = self.client.get('/api/v1/arena/polls/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 1)

    def test_vote_poll_unauthenticated_fails(self):
        res = self.client.post('/api/v1/arena/polls/poll-01/vote/', data={'option_id': 'opt-01'}, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vote_poll_authenticated_success(self):
        self.client.force_login(self.user)
        res = self.client.post('/api/v1/arena/polls/poll-01/vote/', data={'option_id': 'opt-01'}, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_battles_public_access(self):
        res = self.client.get('/api/v1/arena/battles/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 1)

    def test_vote_battle_unauthenticated_fails(self):
        res = self.client.post('/api/v1/arena/battles/battle-01/vote/', data={'selected_song': 'song_a'}, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vote_battle_authenticated_success(self):
        self.client.force_login(self.user)
        res = self.client.post('/api/v1/arena/battles/battle-01/vote/', data={'selected_song': 'song_a'}, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_trivia_and_scoring(self):
        # 1. Get questions as public guest
        q_res = self.client.get('/api/v1/arena/trivia/')
        self.assertEqual(q_res.status_code, status.HTTP_200_OK)
        questions = q_res.json()['data']
        self.assertGreaterEqual(len(questions), 5)

        # 2. Submit answers without auth should fail
        sub_payload = {'answers': {'q1': 1, 'q2': 1, 'q3': 1, 'q4': 2, 'q5': 1, 'q6': 1}}
        guest_res = self.client.post('/api/v1/arena/trivia/submit/', data=sub_payload, content_type='application/json')
        self.assertEqual(guest_res.status_code, status.HTTP_401_UNAUTHORIZED)

        # 3. Submit answers authenticated
        self.client.force_login(self.user)
        sub_res = self.client.post('/api/v1/arena/trivia/submit/', data=sub_payload, content_type='application/json')
        self.assertEqual(sub_res.status_code, status.HTTP_200_OK)
        score_data = sub_res.json()['data']
        self.assertGreaterEqual(score_data['score'], 5)
        self.assertEqual(score_data['points_awarded'], score_data['score'] * 50)

    def test_leaderboard(self):
        res = self.client.get('/api/v1/arena/leaderboard/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 2)
