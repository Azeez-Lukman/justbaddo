"""
Serializers for community moderation, content reports, and disciplinary actions.
"""

from rest_framework import serializers

class ContentReportSerializer(serializers.Serializer):
    target_type = serializers.ChoiceField(choices=[
        ('POST', 'Community Post'),
        ('COMMENT', 'Comment / Reply'),
        ('USER', 'User Profile'),
        ('STORY', 'Fan Story')
    ])
    target_id = serializers.CharField()
    reason = serializers.ChoiceField(choices=[
        ('SPAM', 'Spam / Commercial advertising'),
        ('HARASSMENT', 'Harassment / Hate speech'),
        ('MISINFORMATION', 'Misinformation regarding artist/releases'),
        ('COPYRIGHT_VIOLATION', 'Unauthorised audio link or leak'),
        ('INAPPROPRIATE', 'Inappropriate or vulgar content')
    ])
    details = serializers.CharField(required=False, allow_blank=True, max_length=1000)

class ModerationActionSerializer(serializers.Serializer):
    report_id = serializers.CharField()
    action = serializers.ChoiceField(choices=[
        ('DISMISS', 'Dismiss report'),
        ('REMOVE_CONTENT', 'Remove reported content'),
        ('WARN_USER', 'Issue formal warning'),
        ('SUSPEND_USER', 'Temporarily suspend user account'),
        ('BAN_USER', 'Permanently ban user account')
    ])
    notes = serializers.CharField(required=False, allow_blank=True)
