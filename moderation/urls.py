"""
URL routing for moderation endpoints.
"""

from django.urls import path
from moderation.views import (
    ReportSubmitView,
    ModerationQueueView,
    ModerationActionApplyView,
    UserModerationStatusView
)

app_name = 'moderation'

urlpatterns = [
    path('report/', ReportSubmitView.as_view(), name='report-submit'),
    path('reports/', ModerationQueueView.as_view(), name='moderation-queue'),
    path('action/', ModerationActionApplyView.as_view(), name='moderation-action'),
    path('users/<str:username>/status/', UserModerationStatusView.as_view(), name='user-status'),
]
