"""
Serializers for licensing tracking, rights clearance records, and takedown inquiries.
"""

from rest_framework import serializers

class RightsRecordSerializer(serializers.Serializer):
    track_id = serializers.CharField()
    title = serializers.CharField()
    release_year = serializers.IntegerField()
    rightsholder_label = serializers.CharField()
    licensing_status = serializers.CharField()
    territories_allowed = serializers.ListField(child=serializers.CharField())
    allowed_playback_modes = serializers.ListField(child=serializers.CharField())
    disclaimer = serializers.CharField()

class RightsInquirySerializer(serializers.Serializer):
    claimant_name = serializers.CharField(min_length=2, max_length=100)
    organization = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    track_or_album = serializers.CharField(max_length=150)
    inquiry_type = serializers.ChoiceField(choices=[
        ('LICENSING_OFFER', 'Direct Licensing Agreement'),
        ('TAKEDOWN_REQUEST', 'Notice & Takedown Request'),
        ('METADATA_CORRECTION', 'Correction of Rights / Producer Credits'),
        ('GENERAL_INQUIRY', 'General Legal / Rights Question')
    ])
    message = serializers.CharField(min_length=15, max_length=3000)
