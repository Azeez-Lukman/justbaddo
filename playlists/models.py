"""
Database models for user and editorial playlists and ordered track memberships.
"""

from django.db import models
from django.contrib.auth.models import User

class Playlist(models.Model):
    playlist_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    is_editorial = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    cover_image = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'playlists_playlists'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} by {self.creator.username}"

    @property
    def track_count(self):
        return self.playlist_tracks.count()

class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='playlist_tracks')
    track = models.ForeignKey('music.Track', on_delete=models.CASCADE, related_name='playlist_memberships')
    order = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'playlists_playlist_tracks'
        ordering = ['order', 'added_at']
        unique_together = ('playlist', 'track')

    def __str__(self):
        return f"{self.track.title} in {self.playlist.title} (Order: {self.order})"
