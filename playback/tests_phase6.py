"""
Comprehensive Automated Tests for Phase 6: Authorised Music Streaming & Player Activation.
Verifies provider resolution, availability states, rights validation, territory restrictions,
duplicate telemetry suppression, and privacy guardrails.
"""

from core.test_base import JustBaddoTestCase
from rest_framework import status
from music.models import Track, Album, Artist
from licensing.models import RightsRecord
from playback.models import PlaybackSession, ListeningHistory
from accounts.models import AccountSettings
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Phase6PlaybackIntegrationTests(JustBaddoTestCase):
    def setUp(self):
        super().setUp()
        self.artist = Artist.objects.filter(slug='olamide').first()
        self.album = Album.objects.filter(slug='ikigai-vol-1').first()

    def test_availability_states_all_five(self):
        """Verifies that all 5 availability states (metadata_only, provider_available, self_hosted_available, restricted, withdrawn) are correctly classified."""
        # 1. Metadata Only
        res_meta = self.client.get('/api/v1/playback/check/rap-04/')
        self.assertEqual(res_meta.status_code, status.HTTP_200_OK)
        self.assertEqual(res_meta.json()['data']['availability_state'], 'metadata_only')
        self.assertFalse(res_meta.json()['data']['can_play'])

        # 2. Provider Available
        res_prov = self.client.get('/api/v1/playback/check/iki-01/')
        self.assertEqual(res_prov.status_code, status.HTTP_200_OK)
        self.assertIn(res_prov.json()['data']['availability_state'], ['provider_available', 'self_hosted_available'])
        self.assertTrue(res_prov.json()['data']['can_play'])

        # 3. Restricted
        track_restr = Track.objects.create(
            track_id='test-restr-01',
            title='Restricted Track',
            playback_status='RESTRICTED'
        )
        RightsRecord.objects.create(
            track=track_restr,
            licensing_status='restricted',
            territories_allowed=['NG']
        )
        res_restr = self.client.get('/api/v1/playback/check/test-restr-01/')
        self.assertEqual(res_restr.status_code, status.HTTP_200_OK)
        self.assertEqual(res_restr.json()['data']['availability_state'], 'restricted')
        self.assertFalse(res_restr.json()['data']['can_play'])

        # 4. Withdrawn
        track_withdrawn = Track.objects.create(
            track_id='test-withdrawn-01',
            title='Withdrawn Track',
            playback_status='WITHDRAWN'
        )
        RightsRecord.objects.create(
            track=track_withdrawn,
            licensing_status='withdrawn'
        )
        res_with = self.client.get('/api/v1/playback/check/test-withdrawn-01/')
        self.assertEqual(res_with.status_code, status.HTTP_200_OK)
        self.assertEqual(res_with.json()['data']['availability_state'], 'withdrawn')
        self.assertFalse(res_with.json()['data']['can_play'])

        # 5. Self-Hosted Available (Direct Master Cleared)
        track_direct = Track.objects.create(
            track_id='test-direct-01',
            title='Direct Licensed Master',
            playback_status='JUSTBADDO_STREAMING'
        )
        RightsRecord.objects.create(
            track=track_direct,
            licensing_status='licensed',
            master_rights_cleared=True,
            composition_rights_cleared=True,
            playback_authorized=True,
            territories_allowed=['WORLD']
        )
        res_direct = self.client.get('/api/v1/playback/check/test-direct-01/')
        self.assertEqual(res_direct.status_code, status.HTTP_200_OK)
        self.assertEqual(res_direct.json()['data']['availability_state'], 'self_hosted_available')
        self.assertEqual(res_direct.json()['data']['provider'], 'self_hosted')
        self.assertTrue(res_direct.json()['data']['can_play'])

    def test_territory_restrictions_enforced(self):
        """Verifies server-side rejection when territory does not match rights record."""
        track_terr = Track.objects.create(
            track_id='test-terr-01',
            title='Nigeria Exclusive Track',
            playback_status='JUSTBADDO_STREAMING'
        )
        RightsRecord.objects.create(
            track=track_terr,
            licensing_status='licensed',
            territories_allowed=['NG', 'GH']
        )

        # Allowed territory: NG
        res_allowed = self.client.get('/api/v1/playback/check/test-terr-01/?territory=NG')
        self.assertEqual(res_allowed.status_code, status.HTTP_200_OK)
        self.assertTrue(res_allowed.json()['data']['can_play'])

        # Disallowed territory: US
        res_denied = self.client.get('/api/v1/playback/check/test-terr-01/?territory=US')
        self.assertEqual(res_denied.status_code, status.HTTP_200_OK)
        self.assertFalse(res_denied.json()['data']['can_play'])
        self.assertEqual(res_denied.json()['data']['availability_state'], 'restricted')

        # Session creation denied for disallowed territory
        res_session = self.client.post('/api/v1/playback/session/', data={
            'track_id': 'test-terr-01',
            'territory': 'US'
        }, content_type='application/json')
        self.assertEqual(res_session.status_code, status.HTTP_403_FORBIDDEN)

    def test_expired_licensing_permissions_block_session(self):
        """Verifies that expired valid_until date automatically blocks playback."""
        track_exp = Track.objects.create(
            track_id='test-exp-01',
            title='Expired Rights Track',
            playback_status='JUSTBADDO_STREAMING'
        )
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        RightsRecord.objects.create(
            track=track_exp,
            licensing_status='licensed',
            playback_authorized=True,
            valid_until=yesterday,
            territories_allowed=['WORLD']
        )

        res_check = self.client.get('/api/v1/playback/check/test-exp-01/')
        self.assertFalse(res_check.json()['data']['can_play'])
        self.assertEqual(res_check.json()['data']['rights_status'], 'expired')

        res_session = self.client.post('/api/v1/playback/session/', data={
            'track_id': 'test-exp-01'
        }, content_type='application/json')
        self.assertEqual(res_session.status_code, status.HTTP_403_FORBIDDEN)

    def test_future_start_date_blocks_playback(self):
        """Verifies that future valid_from date blocks playback until active."""
        track_fut = Track.objects.create(
            track_id='test-fut-01',
            title='Future Release Track',
            playback_status='JUSTBADDO_STREAMING'
        )
        tomorrow = datetime.date.today() + datetime.timedelta(days=2)
        RightsRecord.objects.create(
            track=track_fut,
            licensing_status='licensed',
            playback_authorized=True,
            valid_from=tomorrow,
            territories_allowed=['WORLD']
        )

        res_check = self.client.get('/api/v1/playback/check/test-fut-01/')
        self.assertFalse(res_check.json()['data']['can_play'])
        self.assertEqual(res_check.json()['data']['rights_status'], 'pending_start')

    def test_playback_session_capabilities_returned(self):
        """Verifies that session creation returns supported provider capabilities."""
        res = self.client.post('/api/v1/playback/session/', data={
            'track_id': 'iki-01',
            'territory': 'NG'
        }, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.json()['data']
        self.assertIn('session_id', data)
        self.assertIn('capabilities', data)
        self.assertTrue(data['capabilities']['can_seek'])
        self.assertTrue(data['capabilities']['can_change_volume'])

    def test_duplicate_completion_event_deduplication(self):
        """Verifies that duplicate completion events submitted within 60s are suppressed."""
        track = Track.objects.get(track_id='iki-01')
        user = User.objects.get(username='baddofan99')

        initial_count = ListeningHistory.objects.filter(user=user, track=track).count()

        # First completion submission
        payload = {
            'track_id': 'iki-01',
            'duration_seconds': 167,
            'completed': True
        }
        res1 = self.client.post('/api/v1/playback/log/', data=payload, content_type='application/json')
        self.assertEqual(res1.status_code, status.HTTP_200_OK)

        # Immediate second submission (should be suppressed as duplicate)
        res2 = self.client.post('/api/v1/playback/log/', data=payload, content_type='application/json')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.json()['data'].get('status'), 'duplicate_suppressed')

        final_count = ListeningHistory.objects.filter(user=user, track=track).count()
        self.assertEqual(final_count, initial_count + 1)

    def test_session_invalidation_after_completion(self):
        """Verifies that session becomes invalid after completion to prevent reuse."""
        res_sess = self.client.post('/api/v1/playback/session/', data={
            'track_id': 'iki-01'
        }, content_type='application/json')
        sess_id = res_sess.json()['data']['session_id']

        session_obj = PlaybackSession.objects.get(session_id=sess_id)
        self.assertTrue(session_obj.is_valid)
        self.assertIsNone(session_obj.ended_at)

        # Log completion with session_id
        res_log = self.client.post('/api/v1/playback/log/', data={
            'track_id': 'iki-01',
            'session_id': sess_id,
            'duration_seconds': 167,
            'completed': True
        }, content_type='application/json')
        self.assertEqual(res_log.status_code, status.HTTP_200_OK)

        session_obj.refresh_from_db()
        self.assertFalse(session_obj.is_valid)
        self.assertIsNotNone(session_obj.ended_at)

        # Re-attempting to log completion with now-invalid session
        res_log_again = self.client.post('/api/v1/playback/log/', data={
            'track_id': 'iki-01',
            'session_id': sess_id,
            'duration_seconds': 167,
            'completed': True
        }, content_type='application/json')
        self.assertEqual(res_log_again.json()['data'].get('status'), 'duplicate_suppressed')

    def test_user_history_privacy_guard(self):
        """Verifies that private listening history is hidden from third-party viewers."""
        user_owner = User.objects.get(username='kehinde_b')
        settings_owner, _ = AccountSettings.objects.get_or_create(user=user_owner)
        settings_owner.private_listening_activity = True
        settings_owner.save()

        track = Track.objects.get(track_id='iki-01')
        ListeningHistory.objects.create(
            user=user_owner,
            track=track,
            duration_seconds=120,
            completed=True
        )

        # Unauthenticated / third-party request for user_owner's history
        res_public = self.client.get('/api/v1/playback/history/?username=kehinde_b')
        self.assertEqual(res_public.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_public.json()['data']), 0)

        # Authenticated as the owner himself
        self.client.force_login(user_owner)
        res_owner = self.client.get('/api/v1/playback/history/?username=kehinde_b')
        self.assertEqual(res_owner.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res_owner.json()['data']), 1)
