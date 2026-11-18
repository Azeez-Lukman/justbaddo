"""
Notification service layer for JustBaddo.
Manages user alerts, unread counts, and notification lifecycle.
"""

import uuid
import datetime

class NotificationService:
    """
    In-memory notification repository for Phase 2.
    """

    _notifications = {
        'baddofan99': [
            {
                'id': 'notif-01',
                'title': 'New Song Battle Live!',
                'message': '"Wo!!" and "Science Student" are locked in a dead heat battle in Fan Arena.',
                'category': 'Arena',
                'timestamp': '10 minutes ago',
                'is_read': False,
                'action_url': '/pages/fan-arena.html',
                'icon': 'flame'
            },
            {
                'id': 'notif-02',
                'title': 'Reply to your comment',
                'message': 'Folake Adeleke replied to your comment on "Why Carpe Diem Remains Cohesive".',
                'category': 'Community',
                'timestamp': '45 minutes ago',
                'is_read': False,
                'action_url': '/pages/community.html',
                'icon': 'message-square'
            },
            {
                'id': 'notif-03',
                'title': 'Catalogue Update',
                'message': 'Verified producer and BPM credits updated for Ikigai, Vol. 1 tracks.',
                'category': 'Music',
                'timestamp': '1 day ago',
                'is_read': True,
                'action_url': '/pages/album.html?slug=ikigai-vol-1',
                'icon': 'disc-3'
            }
        ]
    }

    @classmethod
    def list_notifications(cls, username, unread_only=False):
        user_list = cls._notifications.get(username, [])
        if unread_only:
            return [n for n in user_list if not n['is_read']]
        return user_list

    @classmethod
    def get_unread_count(cls, username):
        user_list = cls._notifications.get(username, [])
        return sum(1 for n in user_list if not n['is_read'])

    @classmethod
    def mark_as_read(cls, username, notif_id):
        user_list = cls._notifications.get(username, [])
        for n in user_list:
            if n['id'] == notif_id:
                n['is_read'] = True
                return True, "Notification marked as read."
        return False, "Notification not found."

    @classmethod
    def mark_all_as_read(cls, username):
        user_list = cls._notifications.get(username, [])
        for n in user_list:
            n['is_read'] = True
        return True, "All notifications marked as read."

    @classmethod
    def create_notification(cls, username, title, message, category='System', action_url='', icon='bell'):
        if username not in cls._notifications:
            cls._notifications[username] = []
        notif_id = f"notif-{uuid.uuid4().hex[:6]}"
        entry = {
            'id': notif_id,
            'title': title,
            'message': message,
            'category': category,
            'timestamp': 'Just now',
            'is_read': False,
            'action_url': action_url,
            'icon': icon
        }
        cls._notifications[username].insert(0, entry)
        return entry
