from django.contrib import admin
from moderation.models import Report, ModerationAction, UserRestriction

class ModerationActionInline(admin.TabularInline):
    model = ModerationAction
    extra = 1

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'target_type', 'target_id', 'reason', 'reporter', 'status', 'created_at')
    list_filter = ('target_type', 'reason', 'status', 'created_at')
    search_fields = ('report_id', 'target_id', 'details', 'reporter__username')
    inlines = [ModerationActionInline]

@admin.register(ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    list_display = ('report', 'action', 'moderator', 'created_at')
    list_filter = ('action',)

@admin.register(UserRestriction)
class UserRestrictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_suspended', 'is_banned', 'warnings_count', 'updated_at')
    list_filter = ('is_suspended', 'is_banned')
