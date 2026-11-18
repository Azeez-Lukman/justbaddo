"""
Database models for fan editorial essays, reflections, and story submissions.
"""

from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING_REVIEW', 'Pending Review'),
        ('PUBLISHED', 'Published'),
        ('REJECTED', 'Rejected')
    ]

    story_id = models.CharField(max_length=50, unique=True)
    author_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='stories')
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(max_length=100, default='Community Member')
    author_avatar = models.URLField(max_length=500, blank=True)
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    read_time = models.CharField(max_length=30, default='5 min read')
    cover_image = models.URLField(max_length=500, blank=True)
    tags = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PUBLISHED')
    likes_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stories_stories'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author_name} [{self.status}]"
