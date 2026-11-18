"""
API views for music licensing records, clearance tracking, and legal inquiries.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.response import api_success, api_error
from licensing.services import LicensingService
from licensing.serializers import RightsRecordSerializer, RightsInquirySerializer

class RightsRecordListView(APIView):
    """
    List track licensing clearance records and rights parameters.
    GET /api/v1/licensing/rights/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        records = LicensingService.list_rights_records()
        serializer = RightsRecordSerializer(records, many=True)
        return api_success(data=serializer.data, meta={'count': len(records)})

class RightsRecordDetailView(APIView):
    """
    Get rights record for a specific track.
    GET /api/v1/licensing/rights/<track_id>/
    """
    permission_classes = [AllowAny]

    def get(self, request, track_id):
        record = LicensingService.get_rights_record(track_id)
        if not record:
            return api_error(message=f"No rights clearance record found for '{track_id}'.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        serializer = RightsRecordSerializer(record)
        return api_success(data=serializer.data)

class RightsInquiryView(APIView):
    """
    Submit a rightsholder contact, direct licensing proposal, or takedown notice.
    POST /api/v1/licensing/inquiry/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RightsInquirySerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid inquiry form submission.", code="VALIDATION_ERROR", errors=serializer.errors)

        inquiry = LicensingService.submit_inquiry(
            claimant_name=serializer.validated_data['claimant_name'],
            organization=serializer.validated_data['organization'],
            email=serializer.validated_data['email'],
            track_or_album=serializer.validated_data['track_or_album'],
            inquiry_type=serializer.validated_data['inquiry_type'],
            message=serializer.validated_data['message']
        )

        return api_success(
            data=inquiry,
            message="Your rights communication has been logged. Our licensing team responds within 48 hours.",
            status_code=status.HTTP_201_CREATED
        )
