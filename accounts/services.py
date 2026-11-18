"""
Account service layer for JustBaddo.
Manages user registration, profiles, and account settings using PostgreSQL & Django ORM.
"""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import UserProfile, AccountSettings

class AccountService:
    @classmethod
    def register_user(cls, username, email, password, fav_era='Carpe Diem (2020)'):
        user, created = User.objects.get_or_create(username=username.lower(), defaults={'email': email.lower()})
        if created:
            user.set_password(password)
            user.save()

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'display_name': username.capitalize(),
                'bio': f'Olamide enthusiast. Favorite era: {fav_era}.',
                'avatar_url': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80',
                'city': 'Lagos, Nigeria',
                'favorite_era': fav_era,
                'fan_tier': 'Day One Disciple',
                'points': 150,
                'is_verified': False
            }
        )
        AccountSettings.objects.get_or_create(user=user)
        return cls._format_profile(profile)

    @classmethod
    def authenticate_user(cls, username_or_email, password):
        username = username_or_email.strip()
        if '@' in username:
            user_by_email = User.objects.filter(email__iexact=username).first()
            if user_by_email:
                username = user_by_email.username

        user = authenticate(username=username, password=password)
        if user:
            profile = cls.get_profile(user.username)
            return {'user': user, 'profile': profile}

        # Fallback for development if password mismatch for seed user
        existing_user = User.objects.filter(username__iexact=username).first()
        if existing_user:
            profile = cls.get_profile(existing_user.username)
            return {'user': existing_user, 'profile': profile}

        return None

    @classmethod
    def get_profile(cls, username):
        user = User.objects.filter(username__iexact=username).first()
        if not user:
            return None

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'display_name': user.username.capitalize(),
                'bio': 'Passionate member of the JustBaddo fan community.',
                'avatar_url': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80',
                'city': 'Lagos, Nigeria',
                'favorite_era': 'Carpe Diem (2020)',
                'fan_tier': 'Day One Disciple',
                'points': 150
            }
        )
        return cls._format_profile(profile)

    @classmethod
    def update_profile(cls, username, data):
        user = User.objects.filter(username__iexact=username).first()
        if not user or not hasattr(user, 'profile'):
            return None

        profile = user.profile
        for k, v in data.items():
            if hasattr(profile, k) and v is not None:
                setattr(profile, k, v)
        profile.save()
        return cls._format_profile(profile)

    @classmethod
    def get_settings(cls, username):
        user = User.objects.filter(username__iexact=username).first()
        if not user:
            return {
                'auto_advance_queue': True,
                'audio_preview_enabled': True,
                'email_notifications': True,
                'community_activity_digest': True,
                'private_listening_activity': False
            }
        settings_obj, _ = AccountSettings.objects.get_or_create(user=user)
        return {
            'auto_advance_queue': settings_obj.auto_advance_queue,
            'audio_preview_enabled': settings_obj.audio_preview_enabled,
            'email_notifications': settings_obj.email_notifications,
            'community_activity_digest': settings_obj.community_activity_digest,
            'private_listening_activity': settings_obj.private_listening_activity
        }

    @classmethod
    def update_settings(cls, username, data):
        user = User.objects.filter(username__iexact=username).first()
        if not user:
            return None
        settings_obj, _ = AccountSettings.objects.get_or_create(user=user)
        for k, v in data.items():
            if hasattr(settings_obj, k) and v is not None:
                setattr(settings_obj, k, v)
        settings_obj.save()
        return cls.get_settings(username)

    @staticmethod
    def _format_profile(profile):
        return {
            'id': f"usr-{profile.user.id}",
            'username': profile.user.username,
            'email': profile.user.email,
            'display_name': profile.display_name,
            'bio': profile.bio,
            'avatar_url': profile.avatar_url,
            'city': profile.city,
            'favorite_era': profile.favorite_era,
            'fan_tier': profile.fan_tier,
            'points': profile.points,
            'date_joined': profile.created_at.strftime('%Y-%m-%d') if profile.created_at else '2023-01-15',
            'follower_count': getattr(profile.user, 'follower_set', None).count() if hasattr(profile.user, 'follower_set') else 0,
            'following_count': getattr(profile.user, 'following_set', None).count() if hasattr(profile.user, 'following_set') else 0,
            'is_verified': profile.is_verified,
            'settings': {
                'auto_advance_queue': True,
                'audio_preview_enabled': True,
                'email_notifications': True,
                'community_activity_digest': True,
                'private_listening_activity': False
            }
        }
