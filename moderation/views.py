"""
API views for content reports, review queue, and moderation enforcement.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.response import api_success, api_error
from core.permissions import IsAdminOrModerator
from moderation.services import ModerationService
from moderation.serializers import ContentReportSerializer, ModerationActionSerializer

class ReportSubmitView(APIView):
    """
    Submit a community safety report for offensive content or copyright abuse.
    POST /api/v1/moderation/report/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContentReportSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid report submission.", code="VALIDATION_ERROR", errors=serializer.errors)

        reporter = request.user.username if request.user.is_authenticated else 'baddofan99'
        report = ModerationService.submit_report(
            reporter_username=reporter,
            target_type=serializer.validated_data['target_type'],
            target_id=serializer.validated_data['target_id'],
            reason=serializer.validated_data['reason'],
            details=serializer.validated_data.get('details', '')
        )

        return api_success(
            data=report,
            message="Content report submitted to moderation queue.",
            status_code=status.HTTP_201_CREATED
        )

class ModerationQueueView(APIView):
    """
    List reports awaiting staff inspection.
    GET /api/v1/moderation/reports/
    """
    permission_classes = [AllowAny]  # In Phase 2 allow dev testing; Phase 3 locks to IsAdminOrModerator

    def get(self, request):
        status_filter = request.query_params.get('status')
        reports = ModerationService.list_reports(status_filter=status_filter)
        return api_success(data=reports, meta={'count': len(reports)})

class ModerationActionApplyView(APIView):
    """
    Execute a moderation resolution (dismiss, warn, remove, suspend, ban).
    POST /api/v1/moderation/action/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        if not request.user.is_authenticated:
            return api_error(message="Administrative authentication required.", code="UNAUTHORIZED", status_code=status.HTTP_401_UNAUTHORIZED)
        serializer = ModerationActionSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid moderation action.", code="VALIDATION_ERROR", errors=serializer.errors)

        moderator = request.user.username if request.user.is_authenticated else 'staff_admin'
        success, msg = ModerationService.apply_action(
            report_id=serializer.validated_data['report_id'],
            action=serializer.validated_data['action'],
            moderator_username=moderator,
            notes=serializer.validated_data.get('notes', '')
        )

        if not success:
            return api_error(message=msg, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST)

        return api_success(message=msg)

class UserModerationStatusView(APIView):
    """
    Check if a specific user account is restricted or flagged.
    GET /api/v1/moderation/users/<username>/status/
    """
    permission_classes = [AllowAny]

    def get(self, request, username):
        user_status = ModerationService.get_user_status(username)
        return api_success(data=user_status)
