"""
Serializers for playlists, track additions, and playlist editing.
"""

from rest_framework import serializers

class PlaylistTrackSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    duration = serializers.CharField()
    albumTitle = serializers.CharField(required=False, allow_blank=True)
    coverArt = serializers.URLField(required=False)
    status = serializers.CharField(default='JUSTBADDO_STREAMING')

class PlaylistSummarySerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True)
    creator = serializers.CharField()
    is_editorial = serializers.BooleanField(default=False)
    is_private = serializers.BooleanField(default=False)
    track_count = serializers.IntegerField()
    cover_image = serializers.URLField(allow_blank=True)
    updated_at = serializers.CharField()

class PlaylistDetailSerializer(PlaylistSummarySerializer):
    tracks = PlaylistTrackSerializer(many=True)

class PlaylistCreateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True, max_length=300)
    is_private = serializers.BooleanField(default=False)
    cover_image = serializers.URLField(required=False, allow_blank=True)

class PlaylistAddTrackSerializer(serializers.Serializer):
    track_id = serializers.CharField()
