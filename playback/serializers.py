"""
Serializers for playback sessions, availability verification, and listening logs.
"""

from rest_framework import serializers

class PlaybackCheckSerializer(serializers.Serializer):
    track_id = serializers.CharField()
    territory = serializers.CharField(required=False, default='NG')

class PlaybackSessionInitSerializer(serializers.Serializer):
    track_id = serializers.CharField()
    client_provider = serializers.CharField(default='mock_synth')
    device_type = serializers.CharField(required=False, default='web_browser')

class PlaybackLogSerializer(serializers.Serializer):
    track_id = serializers.CharField()
    duration_seconds = serializers.IntegerField(min_value=1)
    completed_listen = serializers.BooleanField(default=False)
