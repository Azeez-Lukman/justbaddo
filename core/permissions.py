"""
Core security permissions for JustBaddo REST endpoints.
Defines role-based and ownership-based access control.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission allowing only owners of an object to edit or delete it.
    Assumes the model instance has an `author`, `user`, or `creator` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = getattr(obj, 'user', None) or getattr(obj, 'author', None) or getattr(obj, 'creator', None)
        return owner == request.user

class IsAdminOrModerator(BasePermission):
    """
    Allows access only to staff, superusers, or users with moderator status.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return (
            request.user.is_staff or 
            request.user.is_superuser or 
            request.user.groups.filter(name='Moderators').exists()
        )

class IsVerifiedFan(BasePermission):
    """
    Allows interaction (e.g. Song Battle voting or Quiz participation)
    only to authenticated users with confirmed accounts.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        # Profile check for active/verified status
        profile = getattr(request.user, 'profile', None)
        if profile and hasattr(profile, 'is_verified'):
            return profile.is_verified
        return True  # Fallback to authenticated if profile isn't populated yet
