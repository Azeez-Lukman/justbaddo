"""
Core application URL routing.
"""

from django.urls import path
from core.views import HealthCheckView, PlatformMetadataView

app_name = 'core'

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('platform/', PlatformMetadataView.as_view(), name='platform-metadata'),
]
