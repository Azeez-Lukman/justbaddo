from django.contrib import admin
from playlists.models import Playlist, PlaylistTrack

class PlaylistTrackInline(admin.TabularInline):
    model = PlaylistTrack
    extra = 1
    fields = ('order', 'track', 'added_at')
    readonly_fields = ('added_at',)

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'playlist_id', 'creator', 'is_editorial', 'is_private', 'track_count', 'updated_at')
    list_filter = ('is_editorial', 'is_private')
    search_fields = ('title', 'description', 'creator__username')
    inlines = [PlaylistTrackInline]

@admin.register(PlaylistTrack)
class PlaylistTrackAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'track', 'order', 'added_at')
