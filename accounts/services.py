"""
Account service layer for JustBaddo.
Manages user registration, profiles, badges, reputation events, member directory,
and account settings using PostgreSQL & Django ORM.
"""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, url_has_allowed_host_and_scheme
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils import timezone
import uuid

from accounts.models import UserProfile, AccountSettings, Badge, BadgeAward, ReputationEvent
from notifications.models import Notification

class AccountService:
    @classmethod
    def register_user(cls, username, email, password, display_name=None, fav_era='Carpe Diem (2020)'):
        clean_username = username.strip().lower()
        clean_email = email.strip().lower()
        
        user = User.objects.create_user(
            username=clean_username,
            email=clean_email,
            password=password
        )

        final_display_name = display_name.strip() if display_name and display_name.strip() else clean_username.capitalize()

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'display_name': final_display_name,
                'bio': f'Olamide enthusiast. Favorite era: {fav_era}.',
                'avatar_url': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80',
                'city': 'Lagos, Nigeria',
                'country': 'Nigeria',
                'favorite_era': fav_era,
                'favorite_album': 'Time and Space (2026)',
                'favorite_track': 'Jaiye (feat. FOLA)',
                'fan_tier': 'Day One Disciple',
                'points': 150,
                'reputation_score': 150,
                'is_profile_public': True,
                'accepted_community_guidelines': False,
                'is_verified': False
            }
        )
        AccountSettings.objects.get_or_create(user=user)

        # Generate email verification token
        verification_token = cls.generate_verification_token(user)

        formatted = cls._format_profile(profile, include_private=True)
        formatted['verification'] = verification_token
        return formatted

    @classmethod
    def authenticate_user(cls, username_or_email, password):
        lookup = username_or_email.strip()
        username = lookup
        if '@' in lookup:
            user_by_email = User.objects.filter(email__iexact=lookup).first()
            if user_by_email:
                username = user_by_email.username
            else:
                return None

        # Authenticate with credentials strictly checked
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            profile = cls.get_profile(user.username, viewer=user)
            return {'user': user, 'profile': profile}

        return None

    @classmethod
    def generate_verification_token(cls, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return {'uid': uid, 'token': token}

    @classmethod
    def verify_email_token(cls, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return False, "Invalid verification token or user."

        if default_token_generator.check_token(user, token):
            profile = getattr(user, 'profile', None)
            if profile:
                profile.is_verified = True
                profile.save()
            return True, "Email successfully verified. Welcome to JustBaddo!"
        return False, "Verification token has expired or is invalid."

    @classmethod
    def request_password_reset(cls, email):
        clean_email = email.strip().lower()
        user = User.objects.filter(email__iexact=clean_email).first()
        if user and user.is_active:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            try:
                reset_link = f"/pages/reset-password.html?uid={uid}&token={token}"
                send_mail(
                    subject="JustBaddo Password Reset Request",
                    message=f"Hello {user.username},\n\nPlease reset your password using the following link:\n{reset_link}\n\nIf you did not request this, please ignore this email.",
                    from_email="no-reply@justbaddo.com",
                    recipient_list=[user.email],
                    fail_silently=True
                )
            except Exception:
                pass
            return {'uid': uid, 'token': token}
        return None

    @classmethod
    def confirm_password_reset(cls, uidb64, token, new_password):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return False, "Invalid password reset request."

        if not default_token_generator.check_token(user, token):
            return False, "Password reset token has expired or has already been used."

        user.set_password(new_password)
        user.save()
        return True, "Password has been reset successfully. You may now sign in."

    @staticmethod
    def validate_safe_redirect(redirect_url, request, default='/'):
        if not redirect_url:
            return default
        redirect_url = redirect_url.strip()
        host = request.get_host() if request else None
        allowed_hosts = {host} if host else set()
        
        if url_has_allowed_host_and_scheme(url=redirect_url, allowed_hosts=allowed_hosts, require_https=request.is_secure() if request else False):
            return redirect_url
        return default

    @classmethod
    def get_profile(cls, username, viewer=None):
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
                'country': 'Nigeria',
                'favorite_era': 'Carpe Diem (2020)',
                'favorite_album': 'Time and Space (2026)',
                'favorite_track': 'Jaiye (feat. FOLA)',
                'fan_tier': 'Day One Disciple',
                'points': 150,
                'reputation_score': 150,
                'is_profile_public': True
            }
        )

        is_owner_or_staff = (viewer and (viewer.id == user.id or viewer.is_staff))
        if not profile.is_profile_public and not is_owner_or_staff:
            return {
                'id': f"usr-{profile.user.id}",
                'username': profile.user.username,
                'display_name': profile.display_name,
                'avatar_url': profile.avatar_url,
                'fan_tier': profile.fan_tier,
                'is_profile_public': False,
                'is_private': True,
                'message': 'This member profile is set to private.'
            }

        return cls._format_profile(profile, include_private=is_owner_or_staff)

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
        return cls._format_profile(profile, include_private=True)

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

    @classmethod
    def accept_guidelines(cls, user):
        profile = getattr(user, 'profile', None)
        if not profile:
            return False, "Profile not found."
        profile.accepted_community_guidelines = True
        profile.save()
        # Award First Steps badge if not already awarded
        BadgeService.award_badge(user, 'first-steps', reason='Accepted JustBaddo community guidelines')
        return True, "Community guidelines accepted."

    @classmethod
    def deactivate_account(cls, user, password=None):
        if password:
            if not user.check_password(password):
                return False, "Invalid password confirmation."
        user.is_active = False
        user.save()
        return True, "Account successfully deactivated."

    @staticmethod
    def _format_profile(profile, include_private=False):
        badges = [
            {
                'badge_id': a.badge.badge_id,
                'name': a.badge.name,
                'slug': a.badge.slug,
                'icon': a.badge.icon,
                'category': a.badge.category,
                'description': a.badge.description,
                'awarded_at': a.awarded_at.isoformat() if a.awarded_at else ''
            }
            for a in profile.user.badges.all().select_related('badge')
        ] if hasattr(profile.user, 'badges') else []

        data = {
            'id': f"usr-{profile.user.id}",
            'username': profile.user.username,
            'display_name': profile.display_name,
            'bio': profile.bio,
            'avatar_url': profile.avatar_url,
            'city': profile.city,
            'country': profile.country,
            'favorite_era': profile.favorite_era,
            'favorite_album': profile.favorite_album,
            'favorite_track': profile.favorite_track,
            'fan_tier': profile.fan_tier,
            'points': profile.points,
            'reputation_score': profile.reputation_score,
            'is_profile_public': profile.is_profile_public,
            'accepted_community_guidelines': profile.accepted_community_guidelines,
            'badges': badges,
            'date_joined': profile.created_at.strftime('%Y-%m-%d') if profile.created_at else '2023-01-15',
            'follower_count': getattr(profile.user, 'follower_set', None).count() if hasattr(profile.user, 'follower_set') else 0,
            'following_count': getattr(profile.user, 'following_set', None).count() if hasattr(profile.user, 'following_set') else 0,
            'is_verified': profile.is_verified,
        }

        if include_private:
            data['email'] = profile.user.email
            data['settings'] = {
                'auto_advance_queue': True,
                'audio_preview_enabled': True,
                'email_notifications': True,
                'community_activity_digest': True,
                'private_listening_activity': False
            }

        return data


class BadgeService:
    @classmethod
    def get_all_badges(cls):
        badges = Badge.objects.filter(is_active=True).order_by('category', 'name')
        return [
            {
                'badge_id': b.badge_id,
                'name': b.name,
                'slug': b.slug,
                'description': b.description,
                'icon': b.icon,
                'category': b.category,
                'points_required': b.points_required,
                'criteria_description': b.criteria_description
            }
            for b in badges
        ]

    @classmethod
    def get_user_badges(cls, user):
        awards = BadgeAward.objects.filter(user=user).select_related('badge')
        return [
            {
                'badge_id': a.badge.badge_id,
                'name': a.badge.name,
                'slug': a.badge.slug,
                'description': a.badge.description,
                'icon': a.badge.icon,
                'category': a.badge.category,
                'awarded_at': a.awarded_at.isoformat(),
                'reason': a.reason
            }
            for a in awards
        ]

    @classmethod
    def award_badge(cls, user, badge_identifier, awarded_by=None, reason=""):
        badge = Badge.objects.filter(
            models.Q(badge_id=badge_identifier) | models.Q(slug=badge_identifier)
        ).first()
        if not badge:
            return None, False

        award, created = BadgeAward.objects.get_or_create(
            badge=badge,
            user=user,
            defaults={'awarded_by': awarded_by, 'reason': reason or badge.criteria_description}
        )

        if created:
            # Create notification for user
            Notification.objects.create(
                notification_id=f"notif-badge-{uuid.uuid4().hex[:8]}",
                recipient=user,
                title=f"New Badge Earned: {badge.name}!",
                message=f"Congratulations! You were awarded the '{badge.name}' badge. {badge.description}",
                category="Achievement",
                action_url="/pages/profile.html",
                icon=badge.icon or "award"
            )
        return award, created

    @classmethod
    def revoke_badge(cls, user, badge_identifier, revoked_by=None):
        badge = Badge.objects.filter(
            models.Q(badge_id=badge_identifier) | models.Q(slug=badge_identifier)
        ).first()
        if not badge:
            return False
        deleted, _ = BadgeAward.objects.filter(badge=badge, user=user).delete()
        return deleted > 0


class ReputationService:
    WEIGHTS = {
        'REACTION_RECEIVED': 10,
        'HELPFUL_CONTRIBUTION': 15,
        'POST_PUBLISHED': 25,
        'CONSISTENT_PARTICIPATION': 20,
        'SPAM_PENALTY': -50,
        'MODERATION_REVERSAL': 0,
        'ADMIN_ADJUSTMENT': 0
    }
    DAILY_CAP = 100

    @classmethod
    def record_event(cls, user, event_type, source_type="", source_id="", reason="", points_delta=None, actor=None):
        """
        Record an auditable reputation event. Enforces daily earning caps, duplicate event protection,
        and updates UserProfile reputation_score and points.
        """
        if not user or not user.is_authenticated:
            return None

        # Prevent duplicate processing for same non-empty source
        if source_id and source_type:
            existing = ReputationEvent.objects.filter(
                user=user,
                event_type=event_type,
                source_type=source_type,
                source_id=str(source_id),
                is_reversed=False
            ).first()
            if existing:
                return existing

        # Determine points delta
        if points_delta is None:
            points_delta = cls.WEIGHTS.get(event_type, 0)

        # Enforce daily earning cap for positive community actions
        if points_delta > 0 and event_type not in ['ADMIN_ADJUSTMENT']:
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            earned_today = ReputationEvent.objects.filter(
                user=user,
                created_at__gte=today_start,
                points_delta__gt=0,
                is_reversed=False
            ).exclude(event_type='ADMIN_ADJUSTMENT').aggregate(total=Sum('points_delta'))['total'] or 0

            if earned_today >= cls.DAILY_CAP:
                points_delta = 0  # Capped out for today
            elif earned_today + points_delta > cls.DAILY_CAP:
                points_delta = max(0, cls.DAILY_CAP - earned_today)

        event = ReputationEvent.objects.create(
            user=user,
            event_type=event_type,
            points_delta=points_delta,
            source_type=source_type,
            source_id=str(source_id) if source_id else "",
            reason=reason or f"Event: {event_type}"
        )

        profile = getattr(user, 'profile', None)
        if profile:
            profile.reputation_score += points_delta
            if points_delta > 0:
                profile.points += points_delta
            profile.save()

        return event

    @classmethod
    def reverse_event(cls, event_id, reversed_by=None, reason=""):
        event = ReputationEvent.objects.filter(id=event_id, is_reversed=False).first()
        if not event:
            return False, "Active event not found."

        event.is_reversed = True
        event.reversed_by = reversed_by
        event.reversed_at = timezone.now()
        event.save()

        # Reversal compensating event
        compensating_delta = -event.points_delta
        ReputationEvent.objects.create(
            user=event.user,
            event_type='MODERATION_REVERSAL',
            points_delta=compensating_delta,
            source_type='reputation_event',
            source_id=str(event.id),
            reason=reason or f"Reversal of event #{event.id} ({event.event_type}) by moderator {reversed_by.username if reversed_by else 'system'}"
        )

        profile = getattr(event.user, 'profile', None)
        if profile:
            profile.reputation_score += compensating_delta
            if compensating_delta < 0:
                profile.points = max(0, profile.points + compensating_delta)
            profile.save()

        return True, "Reputation event successfully reversed."

    @classmethod
    def reconcile_user_reputation(cls, user):
        active_sum = ReputationEvent.objects.filter(
            user=user,
            is_reversed=False
        ).aggregate(total=Sum('points_delta'))['total'] or 0

        profile = getattr(user, 'profile', None)
        if profile:
            profile.reputation_score = active_sum
            profile.save()
        return active_sum


class MemberDirectoryService:
    @classmethod
    def list_members(cls, query=None, tier=None, badge_slug=None, ordering='-reputation_score', page=1, page_size=20):
        qs = UserProfile.objects.filter(
            is_profile_public=True,
            user__is_active=True
        ).select_related('user').prefetch_related('user__badges__badge')

        if query:
            q = query.strip()
            qs = qs.filter(
                models.Q(user__username__icontains=q) |
                models.Q(display_name__icontains=q) |
                models.Q(city__icontains=q)
            )

        if tier:
            qs = qs.filter(fan_tier__iexact=tier)

        if badge_slug:
            qs = qs.filter(user__badges__badge__slug=badge_slug)

        valid_orderings = {
            '-reputation_score': '-reputation_score',
            'reputation_score': 'reputation_score',
            '-created_at': '-created_at',
            'created_at': 'created_at',
            'display_name': 'display_name'
        }
        order_field = valid_orderings.get(ordering, '-reputation_score')
        qs = qs.order_by(order_field)

        total_count = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_items = qs[start:end]

        members_data = []
        for p in page_items:
            earned_badges = [
                {
                    'badge_id': a.badge.badge_id,
                    'name': a.badge.name,
                    'slug': a.badge.slug,
                    'icon': a.badge.icon,
                    'category': a.badge.category
                }
                for a in p.user.badges.all()
            ]
            members_data.append({
                'id': f"usr-{p.user.id}",
                'username': p.user.username,
                'display_name': p.display_name,
                'bio': p.bio,
                'avatar_url': p.avatar_url,
                'city': p.city,
                'country': p.country,
                'favorite_era': p.favorite_era,
                'favorite_album': p.favorite_album,
                'favorite_track': p.favorite_track,
                'fan_tier': p.fan_tier,
                'points': p.points,
                'reputation_score': p.reputation_score,
                'badges': earned_badges,
                'date_joined': p.created_at.strftime('%Y-%m-%d') if p.created_at else ''
            })

        total_pages = (total_count + page_size - 1) // page_size if page_size else 1
        return {
            'members': members_data,
            'meta': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }
