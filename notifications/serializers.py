"""
Serializers for notifications and alert preferences.
"""

from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    message = serializers.CharField()
    category = serializers.CharField()
    timestamp = serializers.CharField()
    is_read = serializers.BooleanField()
    action_url = serializers.CharField(allow_blank=True, required=False)
    icon = serializers.CharField(default='bell')
