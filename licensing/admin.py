from django.contrib import admin
from licensing.models import RightsRecord, RightsInquiry

@admin.register(RightsRecord)
class RightsRecordAdmin(admin.ModelAdmin):
    list_display = ('track', 'rightsholder_label', 'licensing_status', 'updated_at')
    list_filter = ('licensing_status', 'rightsholder_label')
    search_fields = ('track__title', 'rightsholder_label', 'disclaimer')

@admin.register(RightsInquiry)
class RightsInquiryAdmin(admin.ModelAdmin):
    list_display = ('inquiry_id', 'claimant_name', 'organization', 'inquiry_type', 'status', 'created_at')
    list_filter = ('inquiry_type', 'status')
    search_fields = ('claimant_name', 'organization', 'email', 'track_or_album', 'message')
