"""
Database models for Olamide discography, albums, tracks, and career timeline.
"""

from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    stage_name = models.CharField(max_length=100, default='Olamide')
    slug = models.SlugField(unique=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    origin = models.CharField(max_length=100, default='Bariga, Lagos, Nigeria')
    image_url = models.URLField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'music_artists'

    def __str__(self):
        return self.stage_name

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'music_genres'

    def __str__(self):
        return self.name

class Album(models.Model):
    TYPE_CHOICES = [
        ('Studio Album', 'Studio Album'),
        ('EP', 'EP'),
        ('Compilation', 'Compilation')
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=150)
    album_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Studio Album')
    release_year = models.PositiveIntegerField()
    release_date = models.CharField(max_length=50, blank=True)
    cover_art = models.URLField(max_length=500)
    label = models.CharField(max_length=100, default='YBNL Nation')
    distributor = models.CharField(max_length=100, default='EMPIRE')
    description = models.TextField()
    featured_artists_text = models.CharField(max_length=300, blank=True)
    producers_text = models.CharField(max_length=300, blank=True)
    genres = models.ManyToManyField(Genre, blank=True, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'music_albums'
        ordering = ['-release_year', 'title']

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    @property
    def track_count(self):
        return self.tracks.count()

class Track(models.Model):
    STATUS_CHOICES = [
        ('JUSTBADDO_STREAMING', 'JustBaddo Streaming'),
        ('AUTHORISED_PROVIDER', 'Authorised Provider'),
        ('METADATA_ONLY', 'Metadata Only'),
        ('RESTRICTED', 'Restricted'),
        ('WITHDRAWN', 'Withdrawn')
    ]

    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.CASCADE, related_name='tracks')
    track_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    track_number = models.PositiveIntegerField(default=1)
    duration = models.CharField(max_length=10, default='3:00')
    duration_seconds = models.PositiveIntegerField(default=180)
    featured = models.CharField(max_length=200, blank=True)
    producer = models.CharField(max_length=100, blank=True)
    bpm = models.PositiveIntegerField(null=True, blank=True)
    musical_key = models.CharField(max_length=10, blank=True)
    playback_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='JUSTBADDO_STREAMING')
    is_playable = models.BooleanField(default=True)
    cover_art = models.URLField(max_length=500, blank=True)
    composer = models.CharField(max_length=150, default='Olamide Adedeji')
    recording_location = models.CharField(max_length=100, default='Lagos, Nigeria')
    release_year = models.PositiveIntegerField(default=2024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'music_tracks'
        ordering = ['album', 'track_number']

    def __str__(self):
        return f"{self.title} - {self.album.title if self.album else 'Single'}"

class TimelineMilestone(models.Model):
    year = models.PositiveIntegerField()
    date = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    description = models.TextField()
    badge = models.CharField(max_length=50)
    citation = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'music_timeline_milestones'
        ordering = ['year', 'order']

    def __str__(self):
        return f"{self.year}: {self.title}"
