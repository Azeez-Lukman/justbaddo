"""
URL routing for playback endpoints.
"""

from django.urls import path
from playback.views import (
    PlaybackCheckView,
    PlaybackSessionInitView,
    PlaybackLogView,
    UserListeningHistoryView
)

app_name = 'playback'

urlpatterns = [
    path('check/<str:track_id>/', PlaybackCheckView.as_view(), name='playback-check'),
    path('session/', PlaybackSessionInitView.as_view(), name='session-init'),
    path('log/', PlaybackLogView.as_view(), name='playback-log'),
    path('history/', UserListeningHistoryView.as_view(), name='listening-history'),
]
