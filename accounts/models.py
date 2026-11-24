"""
Database models for user accounts, profiles, badges, reputation, and preferences.
"""

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True, max_length=500)
    avatar_url = models.URLField(blank=True, max_length=500)
    city = models.CharField(max_length=100, blank=True, default='Lagos, Nigeria')
    country = models.CharField(max_length=100, blank=True, default='Nigeria')
    favorite_era = models.CharField(max_length=100, blank=True, default='Carpe Diem (2020)')
    favorite_album = models.CharField(max_length=150, blank=True, default='Time and Space (2026)')
    favorite_track = models.CharField(max_length=150, blank=True, default='Jaiye (feat. FOLA)')
    fan_tier = models.CharField(max_length=50, default='Day One Disciple')
    points = models.PositiveIntegerField(default=150)
    reputation_score = models.IntegerField(default=150)
    is_profile_public = models.BooleanField(default=True)
    accepted_community_guidelines = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_user_profile'
        ordering = ['-reputation_score', '-points', '-created_at']

    @property
    def initials(self):
        name = self.display_name or self.user.username or 'BC'
        parts = name.strip().split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[1][0]).upper()
        return name[:2].upper()

    def __str__(self):
        return f"{self.user.username} ({self.fan_tier})"

class AccountSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    auto_advance_queue = models.BooleanField(default=True)
    audio_preview_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    community_activity_digest = models.BooleanField(default=True)
    private_listening_activity = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_user_settings'

    def __str__(self):
        return f"Settings for {self.user.username}"

class Badge(models.Model):
    CATEGORY_CHOICES = [
        ('community', 'Community & Discussion'),
        ('music', 'Music & Discography'),
        ('reputation', 'Reputation & Longevity'),
        ('arena', 'Fan Arena & Trivia')
    ]

    badge_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='award')  # Lucide icon name
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='community')
    points_required = models.PositiveIntegerField(default=0)
    criteria_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts_badges'
        ordering = ['name']

    def __str__(self):
        return self.name

class BadgeAward(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awards')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    awarded_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True)
    awarded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='badges_granted')

    class Meta:
        db_table = 'accounts_badge_awards'
        unique_together = ('badge', 'user')
        ordering = ['-awarded_at']

    def __str__(self):
        return f"{self.badge.name} awarded to {self.user.username}"

class ReputationEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('REACTION_RECEIVED', 'Positive Reaction Received'),
        ('HELPFUL_CONTRIBUTION', 'Recognised as Helpful'),
        ('POST_PUBLISHED', 'Valuable Post Published'),
        ('CONSISTENT_PARTICIPATION', 'Consistent Activity Streak'),
        ('SPAM_PENALTY', 'Spam / Rule Violation Penalty'),
        ('MODERATION_REVERSAL', 'Moderation Action Reversal'),
        ('ADMIN_ADJUSTMENT', 'Administrative Adjustment')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reputation_events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    points_delta = models.IntegerField()
    source_type = models.CharField(max_length=50, blank=True)  # 'post', 'comment', 'poll', 'moderation'
    source_id = models.CharField(max_length=100, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reversed = models.BooleanField(default=False)
    reversed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reputations_reversed')
    reversed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'accounts_reputation_events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['event_type']),
        ]

    def __str__(self):
        sign = '+' if self.points_delta >= 0 else ''
        return f"{self.user.username}: {sign}{self.points_delta} ({self.event_type})"
