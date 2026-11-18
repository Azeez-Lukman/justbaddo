"""
Licensing service layer for JustBaddo.
Manages master recordings clearance workflows and rights inquiries in PostgreSQL.
"""

from licensing.models import RightsRecord, RightsInquiry
from music.models import Track
import uuid
import datetime

class LicensingService:
    @classmethod
    def verify_track_rights(cls, track_id, territory='NG', tier='free', requested_provider=None):
        """
        Evaluates whether a track has active, territory-compliant, non-withdrawn
        licensing approval for streaming.
        """
        t = Track.objects.filter(track_id__iexact=track_id).select_related('album').first()
        if not t:
            return {
                'can_play': False,
                'availability_state': 'not_found',
                'message': 'Track does not exist in catalogue.',
                'rights_status': 'unknown',
                'rightsholder': 'Unknown',
                'territory': territory,
                'provider': None,
                'provider_track_id': '',
                'provider_embed_url': '',
                'master_cleared': False,
                'composition_cleared': False
            }

        r = RightsRecord.objects.filter(track=t).first()
        status_key = t.playback_status.upper() if t.playback_status else 'METADATA_ONLY'
        licensing_status = r.licensing_status.lower() if r else 'contact_identified'
        rightsholder = r.rightsholder_label if r else 'YBNL Nation / EMPIRE'

        # 1. Withdrawn track check
        if status_key == 'WITHDRAWN' or licensing_status == 'withdrawn':
            return {
                'can_play': False,
                'availability_state': 'withdrawn',
                'message': 'Track has been withdrawn from digital playback by the rightsholder.',
                'rights_status': 'withdrawn',
                'rightsholder': rightsholder,
                'territory': territory,
                'provider': None,
                'provider_track_id': '',
                'provider_embed_url': '',
                'master_cleared': False,
                'composition_cleared': False
            }

        # 2. Explicit Restricted check
        if status_key == 'RESTRICTED' or licensing_status == 'restricted':
            return {
                'can_play': False,
                'availability_state': 'restricted',
                'message': 'Track is restricted from playback in this territory.',
                'rights_status': 'restricted',
                'rightsholder': rightsholder,
                'territory': territory,
                'provider': None,
                'provider_track_id': '',
                'provider_embed_url': '',
                'master_cleared': False,
                'composition_cleared': False
            }

        # 3. Date validity check (Start & Expiration dates)
        today = datetime.date.today()
        if r:
            if r.valid_from and today < r.valid_from:
                return {
                    'can_play': False,
                    'availability_state': 'restricted',
                    'message': 'Licensing agreement for this track is not yet active.',
                    'rights_status': 'pending_start',
                    'rightsholder': rightsholder,
                    'territory': territory,
                    'provider': None,
                    'provider_track_id': '',
                    'provider_embed_url': '',
                    'master_cleared': False,
                    'composition_cleared': False
                }
            if r.valid_until and today > r.valid_until:
                return {
                    'can_play': False,
                    'availability_state': 'restricted',
                    'message': 'Licensing permissions for this track have expired.',
                    'rights_status': 'expired',
                    'rightsholder': rightsholder,
                    'territory': territory,
                    'provider': None,
                    'provider_track_id': '',
                    'provider_embed_url': '',
                    'master_cleared': False,
                    'composition_cleared': False
                }

        # 4. Territory restriction check
        user_territory = (territory or 'NG').strip().upper()
        allowed_territories = r.territories_allowed if (r and r.territories_allowed) else t.availability_territories
        if allowed_territories:
            norm_allowed = [str(x).strip().upper() for x in allowed_territories]
            if 'WORLD' not in norm_allowed and 'GLOBAL' not in norm_allowed and user_territory not in norm_allowed:
                return {
                    'can_play': False,
                    'availability_state': 'restricted',
                    'message': f'Recording is not licensed for playback in territory: {user_territory}.',
                    'rights_status': 'territory_restricted',
                    'rightsholder': rightsholder,
                    'territory': user_territory,
                    'provider': None,
                    'provider_track_id': '',
                    'provider_embed_url': '',
                    'master_cleared': False,
                    'composition_cleared': False
                }

        # 5. Metadata-only check
        if status_key == 'METADATA_ONLY' or (r and licensing_status in ('unverified', 'contact_identified', 'permission_requested')):
            return {
                'can_play': False,
                'availability_state': 'metadata_only',
                'message': 'Metadata-only listing; audio rights not cleared for web streaming.',
                'rights_status': licensing_status,
                'rightsholder': rightsholder,
                'territory': user_territory,
                'provider': None,
                'provider_track_id': '',
                'provider_embed_url': '',
                'master_cleared': bool(r and r.master_rights_cleared),
                'composition_cleared': bool(r and r.composition_rights_cleared)
            }

        # 6. Usage tier check (free vs premium)
        if r and tier == 'free' and not r.free_tier_permitted:
            return {
                'can_play': False,
                'availability_state': 'restricted',
                'message': 'Track is restricted to premium subscribers.',
                'rights_status': 'tier_restricted',
                'rightsholder': rightsholder,
                'territory': user_territory,
                'provider': None,
                'provider_track_id': '',
                'provider_embed_url': '',
                'master_cleared': bool(r.master_rights_cleared),
                'composition_cleared': bool(r.composition_rights_cleared)
            }

        # 7. Resolve provider
        # If track has direct licensed master rights -> self_hosted_available
        if r and r.playback_authorized and r.master_rights_cleared and r.composition_rights_cleared:
            return {
                'can_play': True,
                'availability_state': 'self_hosted_available',
                'message': 'Authorized for direct JustBaddo licensed audio delivery.',
                'rights_status': 'licensed',
                'rightsholder': rightsholder,
                'territory': user_territory,
                'provider': 'self_hosted',
                'provider_track_id': t.provider_track_id or t.track_id,
                'provider_embed_url': t.provider_embed_url,
                'master_cleared': True,
                'composition_cleared': True
            }

        # If track is configured for external authorized provider (SoundCloud / YouTube)
        if status_key == 'AUTHORISED_PROVIDER' or t.provider_name in ('soundcloud', 'youtube'):
            chosen_provider = t.provider_name if t.provider_name in ('soundcloud', 'youtube') else 'soundcloud'
            return {
                'can_play': True,
                'availability_state': 'provider_available',
                'message': f'Authorized for stream delivery via official {chosen_provider} embed player.',
                'rights_status': licensing_status,
                'rightsholder': rightsholder,
                'territory': user_territory,
                'provider': chosen_provider,
                'provider_track_id': t.provider_track_id,
                'provider_embed_url': t.provider_embed_url,
                'master_cleared': bool(r and r.master_rights_cleared),
                'composition_cleared': bool(r and r.composition_rights_cleared)
            }

        # Default fallback: Developer synthetic preview pulse (zero-copyright Web Audio API)
        return {
            'can_play': True,
            'availability_state': 'provider_available',
            'message': 'Playable via developer synthetic preview pulse (Web Audio API).',
            'rights_status': licensing_status,
            'rightsholder': rightsholder,
            'territory': user_territory,
            'provider': 'web_audio_synth',
            'provider_track_id': t.track_id,
            'provider_embed_url': '',
            'master_cleared': False,
            'composition_cleared': False
        }

    @classmethod
    def list_rights_records(cls):
        records = RightsRecord.objects.all().select_related('track')
        results = []
        for r in records:
            results.append({
                'track_id': r.track.track_id,
                'title': r.track.title,
                'release_year': r.track.release_year,
                'rightsholder_label': r.rightsholder_label,
                'licensing_status': r.licensing_status,
                'territories_allowed': r.territories_allowed,
                'allowed_playback_modes': r.allowed_playback_modes,
                'disclaimer': r.disclaimer or f"Master and publishing rights retained by {r.rightsholder_label}."
            })
        return results

    @classmethod
    def get_rights_record(cls, track_id):
        r = RightsRecord.objects.filter(track__track_id__iexact=track_id).select_related('track').first()
        if not r:
            return None

        return {
            'track_id': r.track.track_id,
            'title': r.track.title,
            'release_year': r.track.release_year,
            'rightsholder_label': r.rightsholder_label,
            'licensing_status': r.licensing_status,
            'territories_allowed': r.territories_allowed,
            'allowed_playback_modes': r.allowed_playback_modes,
            'disclaimer': r.disclaimer or f"Master and publishing rights retained by {r.rightsholder_label}."
        }

    @classmethod
    def submit_inquiry(cls, claimant_name, organization, email, track_or_album, inquiry_type, message):
        inquiry_id = f"inq-{uuid.uuid4().hex[:6]}"
        entry = RightsInquiry.objects.create(
            inquiry_id=inquiry_id,
            claimant_name=claimant_name,
            organization=organization,
            email=email,
            track_or_album=track_or_album,
            inquiry_type=inquiry_type,
            message=message,
            status='PENDING_LEGAL_REVIEW'
        )

        return {
            'id': entry.inquiry_id,
            'claimant_name': entry.claimant_name,
            'organization': entry.organization,
            'email': entry.email,
            'track_or_album': entry.track_or_album,
            'inquiry_type': entry.inquiry_type,
            'message': entry.message,
            'submitted_at': entry.created_at.isoformat(),
            'status': entry.status
        }
