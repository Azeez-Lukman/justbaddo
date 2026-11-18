"""
URL routing for licensing endpoints.
"""

from django.urls import path
from licensing.views import (
    RightsRecordListView,
    RightsRecordDetailView,
    RightsInquiryView
)

app_name = 'licensing'

urlpatterns = [
    path('rights/', RightsRecordListView.as_view(), name='rights-list'),
    path('rights/<str:track_id>/', RightsRecordDetailView.as_view(), name='rights-detail'),
    path('inquiry/', RightsInquiryView.as_view(), name='rights-inquiry'),
]
