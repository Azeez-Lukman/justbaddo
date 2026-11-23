"""
Serializers for accounts, authentication, public profiles, badges, and reputation workflows.
Handles user registration, login credentials, profile editing, and password recovery.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
import re

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=30)
    display_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    agree_terms = serializers.BooleanField(required=True)
    fav_era = serializers.CharField(required=False, allow_blank=True, default='Carpe Diem (2020)')

    def validate_username(self, value):
        val = value.strip().lower()
        if not re.match(r'^[a-zA-Z0-9_]+$', val):
            raise serializers.ValidationError("Username can only contain alphanumeric characters and underscores.")
        if User.objects.filter(username__iexact=val).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return val

    def validate_email(self, value):
        val = value.strip().lower()
        if User.objects.filter(email__iexact=val).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return val

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate_agree_terms(self, value):
        if not value:
            raise serializers.ValidationError("You must agree to the JustBaddo terms and community guidelines.")
        return value

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)
    next = serializers.CharField(required=False, allow_blank=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

class EmailVerificationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

class BadgeSerializer(serializers.Serializer):
    badge_id = serializers.CharField()
    name = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()
    category = serializers.CharField()
    points_required = serializers.IntegerField(default=0)
    criteria_description = serializers.CharField(allow_blank=True)

class BadgeAwardSerializer(serializers.Serializer):
    badge_id = serializers.CharField()
    name = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()
    category = serializers.CharField()
    awarded_at = serializers.CharField()
    reason = serializers.CharField(allow_blank=True)

class UserProfileSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    display_name = serializers.CharField(max_length=50)
    bio = serializers.CharField(max_length=500, allow_blank=True)
    avatar_url = serializers.URLField(allow_blank=True)
    city = serializers.CharField(max_length=100, allow_blank=True)
    country = serializers.CharField(max_length=100, allow_blank=True)
    favorite_era = serializers.CharField(max_length=100, allow_blank=True)
    favorite_album = serializers.CharField(max_length=150, allow_blank=True)
    favorite_track = serializers.CharField(max_length=150, allow_blank=True)
    fan_tier = serializers.CharField(default='Day One Disciple')
    points = serializers.IntegerField(default=150)
    reputation_score = serializers.IntegerField(default=150)
    is_profile_public = serializers.BooleanField(default=True)
    accepted_community_guidelines = serializers.BooleanField(default=False)
    date_joined = serializers.CharField()
    follower_count = serializers.IntegerField(default=0)
    following_count = serializers.IntegerField(default=0)
    badges = BadgeAwardSerializer(many=True, required=False)

class ProfileUpdateSerializer(serializers.Serializer):
    display_name = serializers.CharField(required=False, max_length=50)
    bio = serializers.CharField(required=False, max_length=500, allow_blank=True)
    city = serializers.CharField(required=False, max_length=100, allow_blank=True)
    country = serializers.CharField(required=False, max_length=100, allow_blank=True)
    favorite_era = serializers.CharField(required=False, max_length=100, allow_blank=True)
    favorite_album = serializers.CharField(required=False, max_length=150, allow_blank=True)
    favorite_track = serializers.CharField(required=False, max_length=150, allow_blank=True)
    avatar_url = serializers.URLField(required=False, allow_blank=True)
    is_profile_public = serializers.BooleanField(required=False)

class AccountSettingsSerializer(serializers.Serializer):
    auto_advance_queue = serializers.BooleanField(default=True)
    audio_preview_enabled = serializers.BooleanField(default=True)
    email_notifications = serializers.BooleanField(default=True)
    community_activity_digest = serializers.BooleanField(default=True)
    private_listening_activity = serializers.BooleanField(default=False)

class AcceptGuidelinesSerializer(serializers.Serializer):
    accepted = serializers.BooleanField(required=True)

    def validate_accepted(self, value):
        if not value:
            raise serializers.ValidationError("You must accept the community guidelines to proceed.")
        return value

class AccountDeleteSerializer(serializers.Serializer):
    confirm_username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
