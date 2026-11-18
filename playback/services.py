"""
Playback management and provider abstraction service.
Enforces playback access boundaries and persists telemetry to PostgreSQL.
"""

from music.models import Track
from playback.models import PlaybackSession, ListeningHistory
from django.contrib.auth.models import User
import uuid

class PlaybackService:
    ALLOWED_STATUSES = {
        'JUSTBADDO_STREAMING': {
            'can_play': True,
            'provider': 'web_audio_synth',
            'message': 'Playable via developer synthetic preview or direct stream.'
        },
        'AUTHORISED_PROVIDER': {
            'can_play': True,
            'provider': 'external_embed',
            'message': 'Streamable via licensed partner embed (Spotify / Apple Music).'
        },
        'METADATA_ONLY': {
            'can_play': False,
            'provider': None,
            'message': 'Metadata-only listing; audio rights not cleared for web streaming.'
        },
        'RESTRICTED': {
            'can_play': False,
            'provider': None,
            'message': 'Track is currently restricted in this territory.'
        },
        'WITHDRAWN': {
            'can_play': False,
            'provider': None,
            'message': 'Track has been withdrawn from digital playback.'
        }
    }

    @classmethod
    def check_track_availability(cls, track_id, territory='NG'):
        t = Track.objects.filter(track_id__iexact=track_id).first()
        if not t:
            return {
                'exists': False,
                'can_play': False,
                'status': 'NOT_FOUND',
                'message': 'Track does not exist in catalogue.'
            }

        status_key = t.playback_status
        status_info = cls.ALLOWED_STATUSES.get(status_key, cls.ALLOWED_STATUSES['METADATA_ONLY'])

        return {
            'exists': True,
            'track_id': t.track_id,
            'title': t.title,
            'can_play': status_info['can_play'],
            'status': status_key,
            'provider': status_info['provider'],
            'territory': territory,
            'message': status_info['message'],
            'is_synthetic_preview': (status_info['provider'] == 'web_audio_synth')
        }

    @classmethod
    def create_session(cls, track_id, client_provider='mock_synth', device='web_browser', user=None):
        availability = cls.check_track_availability(track_id)
        if not availability['can_play']:
            return None, availability['message']

        t = Track.objects.filter(track_id__iexact=track_id).first()
        session_id = f"play-sess-{uuid.uuid4().hex[:8]}"

        session_obj = PlaybackSession.objects.create(
            session_id=session_id,
            track=t,
            user=user if user and user.is_authenticated else None,
            provider=availability['provider'] or 'web_audio_synth',
            device_type=device
        )

        return {
            'session_id': session_obj.session_id,
            'track_id': track_id,
            'provider': session_obj.provider,
            'device': session_obj.device_type,
            'started_at': session_obj.created_at.isoformat(),
            'status': 'ACTIVE'
        }, "Playback session initialized."

    @classmethod
    def log_playback(cls, track_id, username, duration_seconds, completed=False):
        t = Track.objects.filter(track_id__iexact=track_id).first()
        user = User.objects.filter(username__iexact=username).first()

        if t and user:
            record = ListeningHistory.objects.create(
                user=user,
                track=t,
                duration_seconds=duration_seconds,
                completed=completed
            )
            return {
                'id': f"hist-{record.id}",
                'track_id': track_id,
                'username': username,
                'duration_seconds': duration_seconds,
                'completed': completed,
                'timestamp': record.listened_at.isoformat()
            }

        return {
            'id': f"hist-{uuid.uuid4().hex[:6]}",
            'track_id': track_id,
            'username': username,
            'duration_seconds': duration_seconds,
            'completed': completed
        }

    @classmethod
    def get_user_history(cls, username, limit=20):
        records = ListeningHistory.objects.filter(user__username__iexact=username).select_related('track')[:limit]
        return [
            {
                'id': f"hist-{r.id}",
                'track_id': r.track.track_id,
                'title': r.track.title,
                'duration_seconds': r.duration_seconds,
                'completed': r.completed,
                'timestamp': r.listened_at.isoformat()
            }
            for r in records
        ]
