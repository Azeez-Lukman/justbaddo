from django.contrib import admin
from accounts.models import UserProfile, AccountSettings, Badge, BadgeAward, ReputationEvent

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'fan_tier', 'reputation_score', 'points', 'city', 'country', 'is_profile_public', 'accepted_community_guidelines', 'is_verified')
    search_fields = ('user__username', 'display_name', 'city', 'country')
    list_filter = ('fan_tier', 'is_profile_public', 'accepted_community_guidelines', 'is_verified')

@admin.register(AccountSettings)
class AccountSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'auto_advance_queue', 'audio_preview_enabled', 'email_notifications', 'community_activity_digest')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'icon', 'points_required', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BadgeAward)
class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ('badge', 'user', 'awarded_at', 'awarded_by', 'reason')
    search_fields = ('badge__name', 'user__username', 'reason')
    list_filter = ('badge', 'awarded_at')

@admin.register(ReputationEvent)
class ReputationEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'points_delta', 'source_type', 'source_id', 'is_reversed', 'created_at')
    search_fields = ('user__username', 'reason', 'source_id')
    list_filter = ('event_type', 'is_reversed', 'source_type', 'created_at')
    readonly_fields = ('created_at',)
