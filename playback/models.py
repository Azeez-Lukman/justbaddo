"""
Database models for playback sessions, device telemetry, and listening history.
"""

from django.db import models
from django.contrib.auth.models import User

class PlaybackSession(models.Model):
    session_id = models.CharField(max_length=64, unique=True)
    track = models.ForeignKey('music.Track', on_delete=models.CASCADE, related_name='playback_sessions')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='playback_sessions')
    provider = models.CharField(max_length=50, default='web_audio_synth')
    territory = models.CharField(max_length=10, default='NG')
    device_type = models.CharField(max_length=50, default='web_browser')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'playback_sessions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Session {self.session_id} ({self.track.title})"

class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_history')
    track = models.ForeignKey('music.Track', on_delete=models.CASCADE, related_name='listening_records')
    session = models.ForeignKey(PlaybackSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='history_records')
    playback_event = models.CharField(max_length=30, default='completed')
    duration_seconds = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    client_timestamp = models.DateTimeField(null=True, blank=True)
    listened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'playback_listening_history'
        ordering = ['-listened_at']

    def __str__(self):
        return f"{self.user.username} listened to {self.track.title}"
