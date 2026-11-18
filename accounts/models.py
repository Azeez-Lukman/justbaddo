"""
Database models for user accounts, profiles, and preferences.
"""

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True, max_length=500)
    avatar_url = models.URLField(blank=True, max_length=500)
    city = models.CharField(max_length=100, blank=True, default='Lagos, Nigeria')
    favorite_era = models.CharField(max_length=100, blank=True, default='Carpe Diem (2020)')
    fan_tier = models.CharField(max_length=50, default='Day One Disciple')
    points = models.PositiveIntegerField(default=150)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_user_profile'
        ordering = ['-points', '-created_at']

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
