"""
Database models for rights clearance records, territory restrictions, and legal inquiries.
"""

from django.db import models

class RightsRecord(models.Model):
    STATUS_CHOICES = [
        ('unverified', 'Unverified'),
        ('contact_identified', 'Contact Identified'),
        ('permission_requested', 'Permission Requested'),
        ('negotiation', 'In Negotiation'),
        ('licensed', 'Licensed'),
        ('restricted', 'Restricted'),
        ('expired', 'Expired'),
        ('withdrawn', 'Withdrawn')
    ]

    track = models.OneToOneField('music.Track', on_delete=models.CASCADE, related_name='rights_record')
    rightsholder_label = models.CharField(max_length=150, default='YBNL Nation / EMPIRE')
    licensing_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='contact_identified')
    master_rights_cleared = models.BooleanField(default=False)
    composition_rights_cleared = models.BooleanField(default=False)
    playback_authorized = models.BooleanField(default=False)
    commercial_use_permitted = models.BooleanField(default=False)
    free_tier_permitted = models.BooleanField(default=True)
    premium_tier_permitted = models.BooleanField(default=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    territories_allowed = models.JSONField(default=list, blank=True)
    allowed_playback_modes = models.JSONField(default=list, blank=True)
    provider_restrictions = models.JSONField(default=list, blank=True)
    disclaimer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'licensing_rights_records'

    def __str__(self):
        return f"Rights for {self.track.title} [{self.licensing_status}]"

class RightsInquiry(models.Model):
    INQUIRY_TYPE_CHOICES = [
        ('LICENSING_OFFER', 'Direct Licensing Agreement'),
        ('TAKEDOWN_REQUEST', 'Notice & Takedown Request'),
        ('METADATA_CORRECTION', 'Correction of Rights / Producer Credits'),
        ('GENERAL_INQUIRY', 'General Legal / Rights Question')
    ]

    inquiry_id = models.CharField(max_length=50, unique=True)
    claimant_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=150)
    email = models.EmailField()
    track_or_album = models.CharField(max_length=200)
    inquiry_type = models.CharField(max_length=50, choices=INQUIRY_TYPE_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=30, default='PENDING_LEGAL_REVIEW')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'licensing_rights_inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.inquiry_type} by {self.claimant_name} ({self.organization})"
