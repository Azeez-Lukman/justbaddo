"""
Database models for user alerts, system updates, and notification tracking.
"""

from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    notification_id = models.CharField(max_length=50, unique=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    category = models.CharField(max_length=50, default='System')
    is_read = models.BooleanField(default=False)
    action_url = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=50, default='bell')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} -> {self.recipient.username} ({'Read' if self.is_read else 'Unread'})"
