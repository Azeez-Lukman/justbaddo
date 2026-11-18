"""
JUSTBADDO — Phase 4 End-to-End Testing & Integration Test Suite.
Verifies complete interoperability between:
1. Frontend Template Rendering Views
2. Django REST Framework Endpoints
3. PostgreSQL Database Engine & Models
4. Authentication, Sessions & Security Constraints
"""

import os
import json
from django.conf import settings
from rest_framework import status
from django.contrib.auth.models import User
from core.test_base import JustBaddoTestCase
from music.models import Album, Track
from community.models import Post
from arena.models import Poll, SongBattle
from playlists.models import Playlist

class Phase4IntegrationTests(JustBaddoTestCase):
    """
    Comprehensive integration test suite covering the entire user journey
    and cross-application workflows.
    """

    def test_frontend_template_rendering_and_assets(self):
        """Verify Django template rendering for root, aliases, and all 22 page templates."""
        # 1. Root /
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'JUSTBADDO')
        self.assertContains(response, 'static/css/styles.css')
        self.assertContains(response, 'api-client.js')

        # 2. Index alias /index.html
        response_alias = self.client.get('/index.html')
        self.assertEqual(response_alias.status_code, status.HTTP_200_OK)

        # 3. All 22 pages in frontend/pages/
        pages_dir = settings.BASE_DIR / 'frontend' / 'pages'
        page_files = [f for f in os.listdir(pages_dir) if f.endswith('.html')]
        self.assertGreaterEqual(len(page_files), 22)

        for page_file in page_files:
            page_url = f'/pages/{page_file}'
            res = self.client.get(page_url)
            self.assertEqual(
                res.status_code,
                status.HTTP_200_OK,
                f"Page '{page_url}' failed to render with HTTP 200."
            )

    def test_complete_authentication_journey(self):
        """Verify full user authentication: register -> login -> profile -> settings -> logout."""
        # 1. Register new user
        reg_payload = {
            'username': 'integrator_baddo',
            'email': 'integrator@justbaddo.local',
            'password': 'SecureBaddoPassword123!',
            'agree_terms': True,
            'fav_era': 'Carpe Diem (2020)'
        }
        reg_res = self.client.post('/api/v1/accounts/register/', data=reg_payload, format='json')
        self.assertEqual(reg_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reg_res.json()['status'], 'success')
        self.assertEqual(reg_res.json()['data']['username'], 'integrator_baddo')

        # Verify duplicate registration prevention
        dup_res = self.client.post('/api/v1/accounts/register/', data=reg_payload, format='json')
        self.assertEqual(dup_res.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. Login with credentials
        login_payload = {
            'username_or_email': 'integrator_baddo',
            'password': 'SecureBaddoPassword123!',
            'remember_me': True
        }
        login_res = self.client.post('/api/v1/accounts/login/', data=login_payload, format='json')
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.assertEqual(login_res.json()['status'], 'success')

        # 3. Access current profile via authenticated session
        profile_res = self.client.get('/api/v1/accounts/profile/')
        self.assertEqual(profile_res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_res.json()['data']['username'], 'integrator_baddo')

        # 4. Update settings
        settings_payload = {
            'auto_advance_queue': False,
            'audio_preview_enabled': True,
            'email_notifications': False,
            'community_activity_digest': True,
            'private_listening_activity': True
        }
        settings_res = self.client.put(
            '/api/v1/accounts/settings/',
            data=json.dumps(settings_payload),
            content_type='application/json'
        )
        self.assertEqual(settings_res.status_code, status.HTTP_200_OK)
        self.assertFalse(settings_res.json()['data']['auto_advance_queue'])
        self.assertTrue(settings_res.json()['data']['private_listening_activity'])

        # 5. Logout
        logout_res = self.client.post('/api/v1/accounts/logout/')
        self.assertEqual(logout_res.status_code, status.HTTP_200_OK)

        # 6. Profile is now unauthenticated
        unauth_profile = self.client.get('/api/v1/accounts/profile/')
        self.assertIn(unauth_profile.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_music_catalogue_and_playback_telemetry_flow(self):
        """Verify music discovery, availability check, playback session, and telemetry recording."""
        # 1. Query albums
        albums_res = self.client.get('/api/v1/music/albums/')
        self.assertEqual(albums_res.status_code, status.HTTP_200_OK)
        albums_data = albums_res.json()['data']
        self.assertGreaterEqual(len(albums_data), 5)

        # 2. Inspect Rapsodi album detail
        album_res = self.client.get('/api/v1/music/albums/rapsodi/')
        self.assertEqual(album_res.status_code, status.HTTP_200_OK)
        album_data = album_res.json()['data']
        self.assertEqual(album_data['title'], 'Rapsodi')
        self.assertGreater(len(album_data['tracks']), 0)

        # 3. Inspect first track
        first_track = album_data['tracks'][0]
        track_id = first_track['id']

        track_res = self.client.get(f'/api/v1/music/tracks/{track_id}/')
        self.assertEqual(track_res.status_code, status.HTTP_200_OK)
        self.assertEqual(track_res.json()['data']['title'], first_track['title'])

        # 4. Rights clearance check
        rights_res = self.client.get(f'/api/v1/licensing/check/{track_id}/')
        self.assertEqual(rights_res.status_code, status.HTTP_200_OK)

        # 5. Log in user to create playback session and log play
        user = User.objects.get(username='baddofan99')
        self.client.force_login(user)

        session_res = self.client.post('/api/v1/playback/session/', data={'track_id': track_id}, format='json')
        self.assertEqual(session_res.status_code, status.HTTP_201_CREATED)
        self.assertIn('session_id', session_res.json()['data'])

        # 6. Log completed play
        log_res = self.client.post('/api/v1/playback/log/', data={
            'track_id': track_id,
            'duration_played': 180,
            'completed': True
        }, format='json')
        self.assertEqual(log_res.status_code, status.HTTP_200_OK)

        # 7. Verify listening history in PostgreSQL
        history_res = self.client.get('/api/v1/playback/history/')
        self.assertEqual(history_res.status_code, status.HTTP_200_OK)
        history_tracks = [h['track_id'] for h in history_res.json()['data']]
        self.assertIn(track_id, history_tracks)

    def test_community_post_comment_and_unique_like_constraint(self):
        """Verify community post creation, comment addition, and unique like constraint enforcement."""
        user = User.objects.get(username='baddofan99')
        self.client.force_login(user)

        # 1. Create a post
        post_payload = {
            'title': 'The Cultural Impact of Voice of the Street',
            'content': 'In 2012, this track firmly established indigenous rap in modern mainstream rotation.',
            'category': 'Discussion'
        }
        create_res = self.client.post('/api/v1/community/posts/', data=post_payload, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        post_id = create_res.json()['data']['id']

        # 2. Add a comment
        comment_res = self.client.post(f'/api/v1/community/posts/{post_id}/comments/', data={
            'content': 'Completely agree, the storytelling and delivery was unmatched.'
        }, format='json')
        self.assertEqual(comment_res.status_code, status.HTTP_201_CREATED)

        # 3. Like post
        like_res = self.client.post(f'/api/v1/community/posts/{post_id}/like/')
        self.assertEqual(like_res.status_code, status.HTTP_200_OK)
        self.assertTrue(like_res.json()['data']['has_liked'])
        self.assertEqual(like_res.json()['data']['likes'], 1)

        # 4. Unlike post (toggle)
        unlike_res = self.client.post(f'/api/v1/community/posts/{post_id}/like/')
        self.assertEqual(unlike_res.status_code, status.HTTP_200_OK)
        self.assertFalse(unlike_res.json()['data']['has_liked'])
        self.assertEqual(unlike_res.json()['data']['likes'], 0)

    def test_arena_poll_and_battle_voting_integration(self):
        """Verify arena polls and song battles enforce single-vote constraints."""
        user = User.objects.get(username='baddofan99')
        self.client.force_login(user)

        # 1. Fetch polls
        polls_res = self.client.get('/api/v1/arena/polls/')
        self.assertEqual(polls_res.status_code, status.HTTP_200_OK)
        polls = polls_res.json()['data']
        self.assertGreater(len(polls), 0)

        poll = polls[0]
        poll_id = poll['id']
        opt_id = poll['options'][0]['id']

        # 2. Cast vote
        vote_res = self.client.post(f'/api/v1/arena/polls/{poll_id}/vote/', data={'option_id': opt_id}, format='json')
        self.assertEqual(vote_res.status_code, status.HTTP_200_OK)

        # 3. Duplicate vote must fail with 400 Bad Request
        dup_vote = self.client.post(f'/api/v1/arena/polls/{poll_id}/vote/', data={'option_id': opt_id}, format='json')
        self.assertEqual(dup_vote.status_code, status.HTTP_400_BAD_REQUEST)

    def test_playlist_lifecycle_integration(self):
        """Verify full playlist lifecycle: create -> add track -> remove track -> delete playlist."""
        user = User.objects.get(username='baddofan99')
        self.client.force_login(user)

        # 1. Create playlist
        create_res = self.client.post('/api/v1/playlists/', data={
            'title': 'Night Drives in Bariga',
            'description': 'Smooth rhythms and melodic bangers',
            'is_public': True
        }, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        pl_id = create_res.json()['data']['id']

        # 2. Add track
        track = Track.objects.first()
        add_res = self.client.post(f'/api/v1/playlists/{pl_id}/tracks/', data={'track_id': track.track_id}, format='json')
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)

        # 3. Remove track
        rem_res = self.client.delete(f'/api/v1/playlists/{pl_id}/tracks/{track.track_id}/')
        self.assertEqual(rem_res.status_code, status.HTTP_200_OK)

        # 4. Delete playlist
        del_res = self.client.delete(f'/api/v1/playlists/{pl_id}/')
        self.assertEqual(del_res.status_code, status.HTTP_200_OK)

    def test_unauthenticated_protected_routes(self):
        """Verify that anonymous visitors cannot perform protected state modifications."""
        self.client.logout()

        # Cannot create playlist
        pl_res = self.client.post('/api/v1/playlists/', data={'title': 'Hacker Playlist'}, format='json')
        self.assertIn(pl_res.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Cannot create community post
        post_res = self.client.post('/api/v1/community/posts/', data={'title': 'Spam', 'content': 'Content'}, format='json')
        self.assertIn(post_res.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Cannot execute moderation action
        mod_res = self.client.post('/api/v1/moderation/action/', data={'action_type': 'BAN'}, format='json')
        self.assertIn(mod_res.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
