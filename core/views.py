"""
Core views and system health check endpoints.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from core.response import api_success

class HealthCheckView(APIView):
    """
    System status and operational readiness endpoint.
    GET /api/v1/health/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return api_success(
            data={
                'status': 'healthy',
                'service': 'justbaddo-backend',
                'version': '1.0.0-phase2',
                'environment': 'development' if settings.DEBUG else 'production',
                'database_engine': settings.DATABASES['default']['ENGINE'].split('.')[-1],
            },
            message='JustBaddo backend operational.'
        )

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
                'active_phase': 'Phase 2: Backend Development',
                'modules': [
                    'accounts', 'music', 'playback', 'playlists',
                    'community', 'arena', 'stories', 'notifications',
                    'licensing', 'moderation'
                ]
            },
            message='Platform metadata retrieved.'
        )
