"""
Serializers for accounts and authentication workflows.
Handles user registration, login credentials, profile editing, and password recovery.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
import re

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    agree_terms = serializers.BooleanField(required=True)
    fav_era = serializers.CharField(required=False, allow_blank=True, default='Carpe Diem (2020)')

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain alphanumeric characters and underscores.")
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value.lower()

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return value.lower()

    def validate_agree_terms(self, value):
        if not value:
            raise serializers.ValidationError("You must agree to the JustBaddo terms and community guidelines.")
        return value

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

class UserProfileSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    display_name = serializers.CharField(max_length=50)
    bio = serializers.CharField(max_length=300, allow_blank=True)
    avatar_url = serializers.URLField(allow_blank=True)
    city = serializers.CharField(max_length=50, allow_blank=True)
    favorite_era = serializers.CharField(max_length=50, allow_blank=True)
    fan_tier = serializers.CharField(default='Day One Disciple')
    points = serializers.IntegerField(default=120)
    date_joined = serializers.CharField()
    follower_count = serializers.IntegerField(default=0)
    following_count = serializers.IntegerField(default=0)

class ProfileUpdateSerializer(serializers.Serializer):
    display_name = serializers.CharField(required=False, max_length=50)
    bio = serializers.CharField(required=False, max_length=300, allow_blank=True)
    city = serializers.CharField(required=False, max_length=50, allow_blank=True)
    favorite_era = serializers.CharField(required=False, max_length=50, allow_blank=True)
    avatar_url = serializers.URLField(required=False, allow_blank=True)

class AccountSettingsSerializer(serializers.Serializer):
    auto_advance_queue = serializers.BooleanField(default=True)
    audio_preview_enabled = serializers.BooleanField(default=True)
    email_notifications = serializers.BooleanField(default=True)
    community_activity_digest = serializers.BooleanField(default=True)
    private_listening_activity = serializers.BooleanField(default=False)
