"""
Moderation service layer for JustBaddo.
Manages user reporting, safety reviews, and sanctions using PostgreSQL.
"""

from moderation.models import Report, ModerationAction, UserRestriction
from django.contrib.auth.models import User
import uuid

class ModerationService:
    @classmethod
    def submit_report(cls, reporter_username, target_type, target_id, reason, details=''):
        reporter = User.objects.filter(username__iexact=reporter_username).first()
        report_id = f"rep-{uuid.uuid4().hex[:6]}"

        rep = Report.objects.create(
            report_id=report_id,
            reporter=reporter,
            target_type=target_type,
            target_id=target_id,
            reason=reason,
            details=details or '',
            status='PENDING'
        )

        return {
            'id': rep.report_id,
            'reporter_username': reporter_username,
            'target_type': rep.target_type,
            'target_id': rep.target_id,
            'reason': rep.reason,
            'details': rep.details,
            'timestamp': rep.created_at.isoformat(),
            'status': rep.status
        }

    @classmethod
    def list_reports(cls, status_filter=None):
        qs = Report.objects.all().select_related('reporter')
        if status_filter:
            qs = qs.filter(status=status_filter)

        results = []
        for r in qs:
            results.append({
                'id': r.report_id,
                'reporter_username': r.reporter.username if r.reporter else 'Anonymous',
                'target_type': r.target_type,
                'target_id': r.target_id,
                'reason': r.reason,
                'details': r.details,
                'timestamp': r.created_at.isoformat(),
                'status': r.status
            })
        return results

    @classmethod
    def apply_action(cls, report_id, action, moderator_username, notes=''):
        report = Report.objects.filter(report_id=report_id).first()
        if not report:
            return False, "Report not found."

        moderator, _ = User.objects.get_or_create(username=moderator_username, defaults={'email': f"{moderator_username}@justbaddo.local"})

        ModerationAction.objects.create(
            report=report,
            moderator=moderator,
            action=action,
            notes=notes or ''
        )

        report.status = 'RESOLVED'
        report.save()

        return True, f"Moderation action '{action}' applied successfully."

    @classmethod
    def get_user_status(cls, username):
        user = User.objects.filter(username__iexact=username).first()
        if not user:
            return {
                'username': username,
                'is_suspended': False,
                'is_banned': False,
                'warnings_count': 0
            }

        restriction = getattr(user, 'restriction', None)
        if restriction:
            return {
                'username': username,
                'is_suspended': restriction.is_suspended,
                'is_banned': restriction.is_banned,
                'warnings_count': restriction.warnings_count
            }

        return {
            'username': username,
            'is_suspended': False,
            'is_banned': False,
            'warnings_count': 0
        }
