"""
Playback management and provider abstraction service.
Enforces playback access boundaries and persists telemetry to PostgreSQL.
"""

"""
Playback management and provider abstraction service.
Enforces playback access boundaries and persists telemetry to PostgreSQL.
"""

from music.models import Track
from playback.models import PlaybackSession, ListeningHistory
from licensing.services import LicensingService
from accounts.models import AccountSettings
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import uuid

class PlaybackService:
    PROVIDER_CAPABILITIES = {
        'web_audio_synth': {
            'provider_name': 'web_audio_synth',
            'display_name': 'Web Audio API Synth (Zero-Copyright Demo)',
            'can_seek': True,
            'can_change_volume': True,
            'supports_headless': True,
            'requires_user_gesture': False,
            'is_authorized_stream': False
        },
        'soundcloud': {
            'provider_name': 'soundcloud',
            'display_name': 'SoundCloud Official Embed Widget',
            'can_seek': True,
            'can_change_volume': True,
            'supports_headless': False,
            'requires_user_gesture': True,
            'is_authorized_stream': True
        },
        'youtube': {
            'provider_name': 'youtube',
            'display_name': 'YouTube IFrame Player (Official Visualizer)',
            'can_seek': True,
            'can_change_volume': True,
            'supports_headless': False,
            'requires_user_gesture': True,
            'is_authorized_stream': True
        },
        'self_hosted': {
            'provider_name': 'self_hosted',
            'display_name': 'JustBaddo Direct Licensed CDN Stream',
            'can_seek': True,
            'can_change_volume': True,
            'supports_headless': True,
            'requires_user_gesture': False,
            'is_authorized_stream': True
        }
    }

    @classmethod
    def check_track_availability(cls, track_id, territory='NG', tier='free'):
        """
        Server-side validation of track availability through licensing rules.
        """
        t = Track.objects.filter(track_id__iexact=track_id).first()
        if not t:
            return {
                'exists': False,
                'can_play': False,
                'status': 'NOT_FOUND',
                'availability_state': 'not_found',
                'message': 'Track does not exist in catalogue.',
                'provider': None,
                'capabilities': None
            }

        verification = LicensingService.verify_track_rights(
            track_id=track_id,
            territory=territory,
            tier=tier
        )

        provider_key = verification['provider'] or 'web_audio_synth'
        capabilities = cls.PROVIDER_CAPABILITIES.get(provider_key, cls.PROVIDER_CAPABILITIES['web_audio_synth'])

        return {
            'exists': True,
            'track_id': t.track_id,
            'title': t.title,
            'can_play': verification['can_play'],
            'status': t.playback_status,
            'availability_state': verification['availability_state'],
            'rights_status': verification['rights_status'],
            'rightsholder': verification['rightsholder'],
            'provider': verification['provider'],
            'provider_track_id': verification['provider_track_id'],
            'provider_embed_url': verification['provider_embed_url'],
            'territory': verification['territory'],
            'message': verification['message'],
            'capabilities': capabilities if verification['can_play'] else None,
            'is_synthetic_preview': (verification['provider'] == 'web_audio_synth')
        }

    @classmethod
    def create_session(cls, track_id, territory='NG', client_provider='mock_synth', device='web_browser', user=None, client_ip=None):
        """
        Initializes an authenticated, rights-validated playback session.
        """
        availability = cls.check_track_availability(track_id, territory=territory)
        if not availability['can_play']:
            return None, availability['message']

        t = Track.objects.filter(track_id__iexact=track_id).first()
        session_id = f"play-sess-{uuid.uuid4().hex[:12]}"
        provider_name = availability['provider'] or 'web_audio_synth'

        session_obj = PlaybackSession.objects.create(
            session_id=session_id,
            track=t,
            user=user if (user and user.is_authenticated) else None,
            provider=provider_name,
            territory=territory or 'NG',
            device_type=device or 'web_browser',
            ip_address=client_ip,
            is_valid=True
        )

        return {
            'session_id': session_obj.session_id,
            'track_id': track_id,
            'title': t.title,
            'provider': session_obj.provider,
            'provider_track_id': availability.get('provider_track_id', ''),
            'provider_embed_url': availability.get('provider_embed_url', ''),
            'territory': session_obj.territory,
            'device': session_obj.device_type,
            'availability_state': availability['availability_state'],
            'capabilities': availability['capabilities'],
            'started_at': session_obj.created_at.isoformat(),
            'status': 'ACTIVE'
        }, "Playback session initialized."

    @classmethod
    def log_playback(cls, track_id, username, duration_seconds, completed=False, session_id=None, playback_event='completed', client_timestamp=None):
        """
        Records verified playback telemetry with deduplication and session invalidation.
        """
        t = Track.objects.filter(track_id__iexact=track_id).first()
        user = User.objects.filter(username__iexact=username).first()

        # Session validation
        session = None
        if session_id:
            session = PlaybackSession.objects.filter(session_id=session_id).first()
            if session and not session.is_valid and completed:
                # Session was already marked completed / ended
                return {
                    'status': 'duplicate_suppressed',
                    'message': 'Playback completion already logged for this session.',
                    'session_id': session_id,
                    'track_id': track_id
                }

        if t and user:
            # Deduplication: Check if an identical completed listen was logged in the last 60 seconds
            if completed:
                recent_window = timezone.now() - datetime.timedelta(seconds=60)
                duplicate_exists = ListeningHistory.objects.filter(
                    user=user,
                    track=t,
                    completed=True,
                    listened_at__gte=recent_window
                ).exists()

                if duplicate_exists:
                    return {
                        'status': 'duplicate_suppressed',
                        'message': 'Duplicate completion event suppressed.',
                        'track_id': track_id,
                        'username': username
                    }

            record = ListeningHistory.objects.create(
                user=user,
                track=t,
                session=session,
                playback_event=playback_event or 'completed',
                duration_seconds=duration_seconds,
                completed=completed,
                client_timestamp=client_timestamp
            )

            # Invalidate session upon completion
            if completed and session:
                session.is_valid = False
                session.ended_at = timezone.now()
                session.save(update_fields=['is_valid', 'ended_at'])

            return {
                'id': f"hist-{record.id}",
                'track_id': track_id,
                'username': username,
                'duration_seconds': duration_seconds,
                'completed': completed,
                'event': record.playback_event,
                'timestamp': record.listened_at.isoformat()
            }

        return {
            'id': f"hist-{uuid.uuid4().hex[:6]}",
            'track_id': track_id,
            'username': username,
            'duration_seconds': duration_seconds,
            'completed': completed,
            'event': playback_event
        }

    @classmethod
    def get_user_history(cls, username, viewer=None, limit=20):
        """
        Fetches listening history with user privacy preference enforcement.
        """
        target_user = User.objects.filter(username__iexact=username).first()
        if not target_user:
            return []

        # Privacy check: If viewer is not the user, inspect AccountSettings.private_listening_activity
        if viewer != target_user:
            settings_obj = AccountSettings.objects.filter(user=target_user).first()
            if settings_obj and getattr(settings_obj, 'private_listening_activity', False):
                return []

        records = ListeningHistory.objects.filter(
            user=target_user
        ).select_related('track', 'track__album')[:limit]

        return [
            {
                'id': f"hist-{r.id}",
                'track_id': r.track.track_id,
                'title': r.track.title,
                'album_title': r.track.album.title if r.track.album else 'Single',
                'duration_seconds': r.duration_seconds,
                'completed': r.completed,
                'event': r.playback_event,
                'timestamp': r.listened_at.isoformat()
            }
            for r in records
        ]
