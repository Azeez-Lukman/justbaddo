from django.contrib import admin
from stories.models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'story_id', 'author_name', 'status', 'read_time', 'likes_count', 'published_at', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'author_name', 'content', 'excerpt')
    actions = ['publish_stories', 'reject_stories']

    def publish_stories(self, request, queryset):
        queryset.update(status='PUBLISHED')
    publish_stories.short_description = "Approve and publish selected fan stories"

    def reject_stories(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_stories.short_description = "Reject selected fan stories"
