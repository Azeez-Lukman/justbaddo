from django.contrib import admin
from playback.models import PlaybackSession, ListeningHistory

@admin.register(PlaybackSession)
class PlaybackSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'track', 'user', 'provider', 'device_type', 'created_at')
    list_filter = ('provider', 'device_type')
    search_fields = ('session_id', 'track__title', 'user__username')

@admin.register(ListeningHistory)
class ListeningHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'duration_seconds', 'completed', 'listened_at')
    list_filter = ('completed',)
    search_fields = ('user__username', 'track__title')
