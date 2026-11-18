from django.contrib import admin
from accounts.models import UserProfile, AccountSettings

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'fan_tier', 'points', 'city', 'is_verified', 'created_at')
    search_fields = ('user__username', 'display_name', 'city')
    list_filter = ('fan_tier', 'is_verified')

@admin.register(AccountSettings)
class AccountSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'auto_advance_queue', 'audio_preview_enabled', 'email_notifications')
