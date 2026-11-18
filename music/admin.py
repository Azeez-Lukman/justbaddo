from django.contrib import admin
from music.models import Artist, Genre, Album, Track, TimelineMilestone

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'name', 'origin', 'slug')
    prepopulated_fields = {'slug': ('stage_name',)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class TrackInline(admin.TabularInline):
    model = Track
    extra = 1
    fields = ('track_number', 'track_id', 'title', 'duration', 'featured', 'producer', 'playback_status', 'bpm', 'musical_key')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'album_type', 'label', 'distributor', 'track_count')
    list_filter = ('album_type', 'release_year', 'label')
    search_fields = ('title', 'description', 'featured_artists_text')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TrackInline]

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'track_id', 'album', 'track_number', 'duration', 'playback_status', 'is_playable', 'producer')
    list_filter = ('playback_status', 'is_playable', 'release_year')
    search_fields = ('title', 'track_id', 'featured', 'producer')

@admin.register(TimelineMilestone)
class TimelineMilestoneAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'category', 'badge', 'order')
    list_filter = ('category', 'year')
    search_fields = ('title', 'description')
