"""
API views for user notifications, unread counts, and mark-as-read actions.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.response import api_success, api_error
from notifications.services import NotificationService
from notifications.serializers import NotificationSerializer

class NotificationListView(APIView):
    """
    List user notifications with unread filtering.
    GET /api/v1/notifications/?unread_only=true
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        unread_only = request.query_params.get('unread_only', 'false').lower() in ('true', '1')

        notifs = NotificationService.list_notifications(username, unread_only=unread_only)
        serializer = NotificationSerializer(notifs, many=True)
        return api_success(
            data=serializer.data,
            meta={
                'total_count': len(notifs),
                'unread_count': NotificationService.get_unread_count(username)
            }
        )

class UnreadNotificationCountView(APIView):
    """
    Get current unread notification count badge.
    GET /api/v1/notifications/unread-count/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        count = NotificationService.get_unread_count(username)
        return api_success(data={'unread_count': count})

class MarkNotificationReadView(APIView):
    """
    Mark a single notification as read.
    POST /api/v1/notifications/<id>/read/
    """
    permission_classes = [AllowAny]

    def post(self, request, notif_id):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        success, msg = NotificationService.mark_as_read(username, notif_id)
        if not success:
            return api_error(message=msg, code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)
        return api_success(message=msg)

class MarkAllNotificationsReadView(APIView):
    """
    Mark all user notifications as read.
    POST /api/v1/notifications/mark-all-read/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        NotificationService.mark_all_as_read(username)
        return api_success(message="All notifications marked as read.")
