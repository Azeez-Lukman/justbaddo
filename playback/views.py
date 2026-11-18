"""
API views for playback verification, session creation, and listening history.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.response import api_success, api_error
from playback.services import PlaybackService
from playback.serializers import (
    PlaybackCheckSerializer,
    PlaybackSessionInitSerializer,
    PlaybackLogSerializer
)

class PlaybackCheckView(APIView):
    """
    Query whether a track is legally playable and determine the appropriate provider.
    GET /api/v1/playback/check/<track_id>/?territory=NG
    """
    permission_classes = [AllowAny]

    def get(self, request, track_id):
        territory = request.query_params.get('territory', 'NG')
        result = PlaybackService.check_track_availability(track_id, territory=territory)

        if not result['exists']:
            return api_error(message=result['message'], code="TRACK_NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        return api_success(data=result, message=result['message'])

class PlaybackSessionInitView(APIView):
    """
    Initialize a licensed playback session.
    POST /api/v1/playback/session/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PlaybackSessionInitSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid session parameters.", code="VALIDATION_ERROR", errors=serializer.errors)

        track_id = serializer.validated_data['track_id']
        client_provider = serializer.validated_data['client_provider']
        device = serializer.validated_data.get('device_type', 'web_browser')

        session, message = PlaybackService.create_session(
            track_id=track_id,
            client_provider=client_provider,
            device=device
        )

        if not session:
            return api_error(message=message, code="PLAYBACK_RESTRICTED", status_code=status.HTTP_403_FORBIDDEN)

        return api_success(data=session, message=message, status_code=status.HTTP_201_CREATED)

class PlaybackLogView(APIView):
    """
    Log listening telemetry for dashboard stats.
    POST /api/v1/playback/log/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PlaybackLogSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid telemetry payload.", code="VALIDATION_ERROR", errors=serializer.errors)

        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        record = PlaybackService.log_playback(
            track_id=serializer.validated_data['track_id'],
            username=username,
            duration_seconds=serializer.validated_data['duration_seconds'],
            completed=serializer.validated_data.get('completed_listen', False)
        )
        return api_success(data=record, message="Listening progress recorded.")

class UserListeningHistoryView(APIView):
    """
    Retrieve user recent listening history.
    GET /api/v1/playback/history/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        history = PlaybackService.get_user_history(username)
        return api_success(data=history, meta={'count': len(history)})
