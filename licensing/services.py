"""
Licensing service layer for JustBaddo.
Manages master recordings clearance workflows and rights inquiries in PostgreSQL.
"""

from licensing.models import RightsRecord, RightsInquiry
from music.models import Track
import uuid

class LicensingService:
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
