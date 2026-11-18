"""
Core views and system health check endpoints.
"""

import time
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.db import connection
from core.response import api_success, api_error

class HealthCheckView(APIView):
    """
    System status, database connectivity, and operational readiness endpoint.
    GET /api/v1/health/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        db_status = 'disconnected'
        db_latency_ms = None
        status_code = status.HTTP_200_OK

        start_time = time.monotonic()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1;')
                row = cursor.fetchone()
                if row and row[0] == 1:
                    db_status = 'connected'
                    db_latency_ms = round((time.monotonic() - start_time) * 1000, 2)
        except Exception as exc:
            db_status = f'error: {str(exc)}'
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        is_healthy = (db_status == 'connected')
        payload = {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'service': 'justbaddo-backend',
            'version': '1.0.0-phase6',
            'environment': 'development' if settings.DEBUG else 'production',
            'checks': {
                'database': {
                    'engine': settings.DATABASES['default']['ENGINE'].split('.')[-1],
                    'status': db_status,
                    'latency_ms': db_latency_ms,
                },
                'storage': {
                    'static_root_configured': bool(settings.STATIC_ROOT),
                    'media_root_configured': bool(settings.MEDIA_ROOT),
                }
            }
        }

        if is_healthy:
            return api_success(data=payload, message='JustBaddo backend operational.')
        return api_error(message='Service dependency failure.', errors=payload, status_code=status_code)

class PlatformMetadataView(APIView):
    """
    Public platform metadata, artist focus, and legal affiliation notice.
    GET /api/v1/platform/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return api_success(
            data={
                'name': getattr(settings, 'JUSTBADDO_PLATFORM_NAME', 'JustBaddo'),
                'artist': 'Olamide Baddo',
                'tagline': 'Voice of the Street — Discography & Fan Community',
                'disclaimer': getattr(settings, 'JUSTBADDO_AFFILIATION_DISCLAIMER', ''),
                'active_phase': 'Phase 6: Authorised Music Streaming & Player Activation',
                'modules': [
                    'accounts', 'music', 'playback', 'playlists',
                    'community', 'arena', 'stories', 'notifications',
                    'licensing', 'moderation'
                ]
            },
            message='Platform metadata retrieved.'
        )
