"""
Database models for content reporting, safety review, and user moderation sanctions.
"""

from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    TARGET_TYPE_CHOICES = [
        ('POST', 'Community Post'),
        ('COMMENT', 'Comment / Reply'),
        ('USER', 'User Profile'),
        ('STORY', 'Fan Story')
    ]

    REASON_CHOICES = [
        ('SPAM', 'Spam / Commercial advertising'),
        ('HARASSMENT', 'Harassment / Hate speech'),
        ('MISINFORMATION', 'Misinformation regarding artist/releases'),
        ('COPYRIGHT_VIOLATION', 'Unauthorised audio link or leak'),
        ('INAPPROPRIATE', 'Inappropriate or vulgar content')
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('INVESTIGATING', 'Under Investigation'),
        ('RESOLVED', 'Resolved'),
        ('DISMISSED', 'Dismissed')
    ]

    report_id = models.CharField(max_length=50, unique=True)
    reporter = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='submitted_reports')
    target_type = models.CharField(max_length=30, choices=TARGET_TYPE_CHOICES)
    target_id = models.CharField(max_length=50)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'moderation_reports'
        ordering = ['-created_at']

    def __str__(self):
        return f"Report {self.report_id}: {self.reason} on {self.target_type} ({self.status})"

class ModerationAction(models.Model):
    ACTION_CHOICES = [
        ('DISMISS', 'Dismiss report'),
        ('REMOVE_CONTENT', 'Remove reported content'),
        ('WARN_USER', 'Issue formal warning'),
        ('SUSPEND_USER', 'Temporarily suspend user account'),
        ('BAN_USER', 'Permanently ban user account')
    ]

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='actions')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_actions')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'moderation_actions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} on Report {self.report.report_id} by {self.moderator.username}"

class UserRestriction(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restriction')
    is_suspended = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    warnings_count = models.PositiveIntegerField(default=0)
    reason = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'moderation_user_restrictions'

    def __str__(self):
        return f"Restriction for {self.user.username} (Banned: {self.is_banned}, Suspended: {self.is_suspended})"
