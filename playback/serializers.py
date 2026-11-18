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
    duration_seconds = serializers.IntegerField(min_value=1, required=False)
    duration_played = serializers.IntegerField(min_value=1, required=False)
    completed_listen = serializers.BooleanField(default=False, required=False)
    completed = serializers.BooleanField(default=False, required=False)

    def validate(self, attrs):
        if 'duration_seconds' not in attrs and 'duration_played' in attrs:
            attrs['duration_seconds'] = attrs['duration_played']
        if 'duration_seconds' not in attrs:
            attrs['duration_seconds'] = 180

        if 'completed_listen' not in attrs and 'completed' in attrs:
            attrs['completed_listen'] = attrs['completed']
        return attrs
