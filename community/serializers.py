"""
Serializers for community discussions, threaded replies, and post reactions.
"""

from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    id = serializers.CharField()
    author = serializers.CharField()
    author_username = serializers.CharField()
    avatar = serializers.URLField()
    content = serializers.CharField()
    timestamp = serializers.CharField()
    likes = serializers.IntegerField(default=0)

class PostSummarySerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()
    author = serializers.CharField()
    author_username = serializers.CharField()
    avatar = serializers.URLField()
    category = serializers.CharField()
    timestamp = serializers.CharField()
    likes = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    has_liked = serializers.BooleanField(default=False)

class PostDetailSerializer(PostSummarySerializer):
    comments = CommentSerializer(many=True)

class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=150)
    category = serializers.ChoiceField(choices=[
        'Discography',
        'Lyrics & Meaning',
        'Concerts & OLIC',
        'General Fan Chat'
    ])
    content = serializers.CharField(min_length=10, max_length=5000)

class CommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField(min_length=2, max_length=1000)
