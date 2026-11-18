"""
Serializers for fan stories and community submissions.
"""

from rest_framework import serializers

class StorySummarySerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    author = serializers.CharField()
    author_role = serializers.CharField()
    author_avatar = serializers.URLField()
    date = serializers.CharField()
    read_time = serializers.CharField()
    cover_image = serializers.URLField()
    excerpt = serializers.CharField()
    likes = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.CharField())
    status = serializers.CharField()

class StoryDetailSerializer(StorySummarySerializer):
    content = serializers.CharField()

class StorySubmissionSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=150)
    read_time = serializers.CharField(default='5 min read')
    cover_image = serializers.URLField(required=False, allow_blank=True)
    tags = serializers.CharField(required=False, allow_blank=True)
    content = serializers.CharField(min_length=50, max_length=10000)
