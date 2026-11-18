from django.test import TestCase
from rest_framework import status

class ArenaApiTests(TestCase):
    def test_list_polls(self):
        res = self.client.get('/api/v1/arena/polls/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 2)

    def test_vote_poll(self):
        res = self.client.post('/api/v1/arena/polls/poll-01/vote/', data={'option_id': 'opt-01'}, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_battles(self):
        res = self.client.get('/api/v1/arena/battles/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 1)

    def test_vote_battle(self):
        res = self.client.post('/api/v1/arena/battles/battle-01/vote/', data={'selected_song': 'song_a'}, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_trivia_and_scoring(self):
        # 1. Get questions
        q_res = self.client.get('/api/v1/arena/trivia/')
        self.assertEqual(q_res.status_code, status.HTTP_200_OK)
        questions = q_res.json()['data']
        self.assertEqual(len(questions), 5)

        # 2. Submit answers
        sub_payload = {'answers': {'q1': 1, 'q2': 1, 'q3': 1, 'q4': 2, 'q5': 1}}
        sub_res = self.client.post('/api/v1/arena/trivia/submit/', data=sub_payload, content_type='application/json')
        self.assertEqual(sub_res.status_code, status.HTTP_200_OK)
        score_data = sub_res.json()['data']
        self.assertEqual(score_data['score'], 5)
        self.assertEqual(score_data['points_awarded'], 250)

    def test_leaderboard(self):
        res = self.client.get('/api/v1/arena/leaderboard/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()['data']), 3)
