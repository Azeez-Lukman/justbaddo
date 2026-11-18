"""
Account service layer for JustBaddo.
Encapsulates user registration, profile retrieval, setting persistence, and authentication logic.
"""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import uuid
import datetime

class AccountService:
    """
    Business logic interface for accounts and member profiles.
    Backed by Django auth and in-memory profile repositories during Phase 2.
    """

    # In-memory profile store for Phase 2 development
    _profiles = {
        'baddofan99': {
            'id': 'usr-001',
            'username': 'baddofan99',
            'email': 'baddofan99@justbaddo.local',
            'display_name': 'Tunde Baddo',
            'bio': 'Bariga native, listening since Eni Duro 2010. YBNL for life.',
            'avatar_url': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80',
            'city': 'Bariga, Lagos',
            'favorite_era': 'Carpe Diem (2020)',
            'fan_tier': 'Voice of the Street Ambassador',
            'points': 4850,
            'date_joined': '2023-01-15',
            'follower_count': 142,
            'following_count': 89,
            'is_verified': True,
            'settings': {
                'auto_advance_queue': True,
                'audio_preview_enabled': True,
                'email_notifications': True,
                'community_activity_digest': True,
                'private_listening_activity': False
            }
        }
    }

    @classmethod
    def register_user(cls, username, email, password, fav_era='Carpe Diem (2020)'):
        """
        Registers a new user and provisions their fan profile.
        """
        # Create standard Django user if not existing
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)
            user.save()

        user_id = f"usr-{uuid.uuid4().hex[:6]}"
        profile = {
            'id': user_id,
            'username': username,
            'email': email,
            'display_name': username.capitalize(),
            'bio': f'Olamide enthusiast. Favorite era: {fav_era}.',
            'avatar_url': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80',
            'city': 'Lagos, Nigeria',
            'favorite_era': fav_era,
            'fan_tier': 'Day One Disciple',
            'points': 150,
            'date_joined': datetime.date.today().isoformat(),
            'follower_count': 0,
            'following_count': 0,
            'is_verified': False,
            'settings': {
                'auto_advance_queue': True,
                'audio_preview_enabled': True,
                'email_notifications': True,
                'community_activity_digest': True,
                'private_listening_activity': False
            }
        }
        cls._profiles[username.lower()] = profile
        return profile

    @classmethod
    def authenticate_user(cls, username_or_email, password):
        """
        Authenticates via username or email against Django user store or demo accounts.
        """
        # Find username if email supplied
        username = username_or_email
        if '@' in username_or_email:
            matching_user = User.objects.filter(email__iexact=username_or_email).first()
            if matching_user:
                username = matching_user.username

        user = authenticate(username=username, password=password)
        if user:
            profile = cls.get_profile(user.username)
            return {'user': user, 'profile': profile}

        # Check demo in-memory accounts for testing
        uname = username_or_email.lower()
        if uname in cls._profiles:
            return {'user': None, 'profile': cls._profiles[uname]}

        return None

    @classmethod
    def get_profile(cls, username):
        """
        Retrieves a user profile by username.
        """
        uname = username.lower()
        if uname in cls._profiles:
            return cls._profiles[uname]

        # Dynamically create profile for existing Django user
        user = User.objects.filter(username__iexact=uname).first()
        if user:
            return cls.register_user(user.username, user.email, 'demo-password')

        return None

    @classmethod
    def update_profile(cls, username, data):
        """
        Updates profile fields.
        """
        profile = cls.get_profile(username)
        if not profile:
            return None

        for k, v in data.items():
            if k in profile and v is not None:
                profile[k] = v

        return profile

    @classmethod
    def get_settings(cls, username):
        """
        Retrieves user preferences and playback toggles.
        """
        profile = cls.get_profile(username)
        if profile:
            return profile.get('settings', {})
        return {
            'auto_advance_queue': True,
            'audio_preview_enabled': True,
            'email_notifications': True,
            'community_activity_digest': True,
            'private_listening_activity': False
        }

    @classmethod
    def update_settings(cls, username, data):
        """
        Updates user preferences.
        """
        profile = cls.get_profile(username)
        if not profile:
            return None
        current = profile.get('settings', {})
        current.update(data)
        profile['settings'] = current
        return current
