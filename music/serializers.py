"""
Serializers for Olamide discography, albums, tracks, and timeline milestones.
"""

from rest_framework import serializers

class TrackSummarySerializer(serializers.Serializer):
    id = serializers.CharField()
    number = serializers.IntegerField()
    title = serializers.CharField()
    duration = serializers.CharField()
    featured = serializers.CharField(allow_blank=True)
    producer = serializers.CharField(allow_blank=True)
    status = serializers.CharField()
    isPlayable = serializers.BooleanField()
    bpm = serializers.IntegerField(required=False)
    key = serializers.CharField(required=False, allow_blank=True)

class TrackDetailSerializer(TrackSummarySerializer):
    album_id = serializers.CharField(required=False)
    album_title = serializers.CharField(required=False)
    album_slug = serializers.CharField(required=False)
    cover_art = serializers.URLField(required=False)
    release_year = serializers.IntegerField(required=False)
    composer = serializers.CharField(required=False, default='Olamide Adedeji')
    recording_location = serializers.CharField(required=False, default='Lagos, Nigeria')
    rights_notice = serializers.CharField(required=False)

class AlbumSummarySerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    slug = serializers.CharField()
    type = serializers.CharField()
    releaseYear = serializers.IntegerField()
    releaseDate = serializers.CharField()
    trackCount = serializers.IntegerField()
    duration = serializers.CharField()
    coverArt = serializers.URLField()
    label = serializers.CharField()
    distributor = serializers.CharField()
    description = serializers.CharField()
    featuredArtists = serializers.ListField(child=serializers.CharField())
    producers = serializers.ListField(child=serializers.CharField())

class AlbumDetailSerializer(AlbumSummarySerializer):
    tracks = TrackSummarySerializer(many=True)

class SingleReleaseSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    releaseYear = serializers.IntegerField()
    type = serializers.CharField()
    duration = serializers.CharField()
    producer = serializers.CharField(allow_blank=True)
    featured = serializers.CharField(allow_blank=True)
    status = serializers.CharField()
    isPlayable = serializers.BooleanField()
    coverArt = serializers.URLField()

class TimelineMilestoneSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    date = serializers.CharField()
    title = serializers.CharField()
    category = serializers.CharField()
    description = serializers.CharField()
    badge = serializers.CharField()
    citation = serializers.CharField()
