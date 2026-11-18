"""
Notification service layer for JustBaddo.
Manages user alerts and notification lifecycles in PostgreSQL.
"""

from notifications.models import Notification
from django.contrib.auth.models import User
import uuid

class NotificationService:
    @classmethod
    def list_notifications(cls, username, unread_only=False):
        qs = Notification.objects.filter(recipient__username__iexact=username)
        if unread_only:
            qs = qs.filter(is_read=False)

        results = []
        for n in qs:
            results.append({
                'id': n.notification_id,
                'title': n.title,
                'message': n.message,
                'category': n.category,
                'timestamp': n.created_at.strftime('%B %d, %Y') if n.created_at else 'Recent',
                'is_read': n.is_read,
                'action_url': n.action_url,
                'icon': n.icon
            })
        return results

    @classmethod
    def get_unread_count(cls, username):
        return Notification.objects.filter(recipient__username__iexact=username, is_read=False).count()

    @classmethod
    def mark_as_read(cls, username, notif_id):
        n = Notification.objects.filter(recipient__username__iexact=username, notification_id=notif_id).first()
        if not n:
            return False, "Notification not found."
        n.is_read = True
        n.save()
        return True, "Notification marked as read."

    @classmethod
    def mark_all_as_read(cls, username):
        Notification.objects.filter(recipient__username__iexact=username).update(is_read=True)
        return True, "All notifications marked as read."

    @classmethod
    def create_notification(cls, username, title, message, category='System', action_url='', icon='bell'):
        user, _ = User.objects.get_or_create(username=username, defaults={'email': f"{username}@justbaddo.local"})
        notif_id = f"notif-{uuid.uuid4().hex[:6]}"

        n = Notification.objects.create(
            notification_id=notif_id,
            recipient=user,
            title=title,
            message=message,
            category=category,
            action_url=action_url,
            icon=icon,
            is_read=False
        )

        return {
            'id': n.notification_id,
            'title': n.title,
            'message': n.message,
            'category': n.category,
            'timestamp': 'Just now',
            'is_read': False,
            'action_url': n.action_url,
            'icon': n.icon
        }
