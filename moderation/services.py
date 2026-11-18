"""
Moderation service layer for JustBaddo.
Manages user reporting, content safety, disciplinary sanctions, and audit logging.
"""

import uuid
import datetime

class ModerationService:
    """
    In-memory moderation repository for Phase 2.
    """

    _reports = [
        {
            'id': 'rep-001',
            'reporter_username': 'baddofan99',
            'target_type': 'POST',
            'target_id': 'post-spam-01',
            'reason': 'SPAM',
            'details': 'External gambling link posted in general fan chat.',
            'timestamp': '2024-07-02T10:30:00',
            'status': 'PENDING'
        }
    ]

    _user_restrictions = {}

    @classmethod
    def submit_report(cls, reporter_username, target_type, target_id, reason, details=''):
        report_id = f"rep-{uuid.uuid4().hex[:6]}"
        entry = {
            'id': report_id,
            'reporter_username': reporter_username,
            'target_type': target_type,
            'target_id': target_id,
            'reason': reason,
            'details': details or '',
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'PENDING'
        }
        cls._reports.append(entry)
        return entry

    @classmethod
    def list_reports(cls, status_filter=None):
        if status_filter:
            return [r for r in cls._reports if r['status'] == status_filter]
        return cls._reports

    @classmethod
    def apply_action(cls, report_id, action, moderator_username, notes=''):
        report = next((r for r in cls._reports if r['id'] == report_id), None)
        if not report:
            return False, "Report not found."

        report['status'] = 'RESOLVED'
        report['resolved_by'] = moderator_username
        report['resolution_action'] = action
        report['resolution_notes'] = notes
        report['resolved_at'] = datetime.datetime.now().isoformat()

        return True, f"Moderation action '{action}' applied successfully."

    @classmethod
    def get_user_status(cls, username):
        return cls._user_restrictions.get(username, {
            'username': username,
            'is_suspended': False,
            'is_banned': False,
            'warnings_count': 0
        })
