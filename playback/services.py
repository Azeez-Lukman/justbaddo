"""
Playback management and provider abstraction service.
Enforces playback access boundaries, rights restrictions, and provider resolution.
"""

from music.services import MusicService
import uuid
import datetime

class PlaybackService:
    """
    Orchestrates playback permissions and provider resolution.
    Does NOT distribute copyrighted recordings directly.
    """

    # In-memory session tracking for Phase 2
    _active_sessions = {}
    _listening_history = []

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
        """
        Determines whether a track can be played and which provider is designated.
        """
        track = MusicService.get_track_by_id(track_id)
        if not track:
            return {
                'exists': False,
                'can_play': False,
                'status': 'NOT_FOUND',
                'message': 'Track does not exist in catalogue.'
            }

        status_key = track.get('status', 'METADATA_ONLY')
        status_info = cls.ALLOWED_STATUSES.get(status_key, cls.ALLOWED_STATUSES['METADATA_ONLY'])

        return {
            'exists': True,
            'track_id': track_id,
            'title': track['title'],
            'can_play': status_info['can_play'],
            'status': status_key,
            'provider': status_info['provider'],
            'territory': territory,
            'message': status_info['message'],
            'is_synthetic_preview': (status_info['provider'] == 'web_audio_synth')
        }

    @classmethod
    def create_session(cls, track_id, client_provider='mock_synth', device='web_browser'):
        """
        Registers an active playback session for telemetry and provider coordination.
        """
        availability = cls.check_track_availability(track_id)
        if not availability['can_play']:
            return None, availability['message']

        session_id = f"play-sess-{uuid.uuid4().hex[:8]}"
        session_data = {
            'session_id': session_id,
            'track_id': track_id,
            'provider': availability['provider'],
            'device': device,
            'started_at': datetime.datetime.now().isoformat(),
            'status': 'ACTIVE'
        }
        cls._active_sessions[session_id] = session_data
        return session_data, "Playback session initialized."

    @classmethod
    def log_playback(cls, track_id, username, duration_seconds, completed=False):
        """
        Records listening analytics and dashboard stats.
        """
        record = {
            'id': f"hist-{uuid.uuid4().hex[:6]}",
            'track_id': track_id,
            'username': username,
            'duration_seconds': duration_seconds,
            'completed': completed,
            'timestamp': datetime.datetime.now().isoformat()
        }
        cls._listening_history.append(record)
        return record

    @classmethod
    def get_user_history(cls, username, limit=20):
        user_records = [r for r in cls._listening_history if r['username'] == username]
        user_records.reverse()
        return user_records[:limit]
