"""
Licensing service layer for JustBaddo.
Manages master recordings clearance workflows, rights records, and legal inquiry routing.
Strictly implements the principles laid down in docs/music/JUSTBADDO_MUSIC_LICENSING.md.
"""

import uuid
import datetime

class LicensingService:
    """
    In-memory rights clearance repository for Phase 2.
    """

    _records = [
        {
            'track_id': 'iki-01',
            'title': 'Metaverse',
            'release_year': 2024,
            'rightsholder_label': 'YBNL Nation / EMPIRE',
            'licensing_status': 'permission_requested',
            'territories_allowed': ['NG', 'GH', 'GB', 'US'],
            'allowed_playback_modes': ['web_audio_synth', 'authorised_provider_embed'],
            'disclaimer': 'Master and publishing rights retained by YBNL / EMPIRE.'
        },
        {
            'track_id': 's-03',
            'title': 'Wo!!',
            'release_year': 2017,
            'rightsholder_label': 'YBNL Nation',
            'licensing_status': 'contact_identified',
            'territories_allowed': ['GLOBAL'],
            'allowed_playback_modes': ['web_audio_synth', 'authorised_provider_embed'],
            'disclaimer': 'Production composition by Young Jonn; master by YBNL.'
        },
        {
            'track_id': 'rap-01',
            'title': 'Eni Duro',
            'release_year': 2011,
            'rightsholder_label': 'Coded Tunes / NotJustOk',
            'licensing_status': 'contact_identified',
            'territories_allowed': ['GLOBAL'],
            'allowed_playback_modes': ['web_audio_synth'],
            'disclaimer': 'Historic catalog track; produced by ID Cabasa.'
        }
    ]

    _inquiries = []

    @classmethod
    def list_rights_records(cls):
        return cls._records

    @classmethod
    def get_rights_record(cls, track_id):
        return next((r for r in cls._records if r['track_id'].lower() == track_id.lower()), None)

    @classmethod
    def submit_inquiry(cls, claimant_name, organization, email, track_or_album, inquiry_type, message):
        inquiry_id = f"inq-{uuid.uuid4().hex[:6]}"
        entry = {
            'id': inquiry_id,
            'claimant_name': claimant_name,
            'organization': organization,
            'email': email,
            'track_or_album': track_or_album,
            'inquiry_type': inquiry_type,
            'message': message,
            'submitted_at': datetime.datetime.now().isoformat(),
            'status': 'PENDING_LEGAL_REVIEW'
        }
        cls._inquiries.append(entry)
        return entry
