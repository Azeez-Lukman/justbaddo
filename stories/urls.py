"""
URL routing for fan stories endpoints.
"""

from django.urls import path
from stories.views import (
    StoryListView,
    StoryDetailView,
    StorySubmitView,
    StoryPublishView
)

app_name = 'stories'

urlpatterns = [
    path('', StoryListView.as_view(), name='story-list'),
    path('submit/', StorySubmitView.as_view(), name='story-submit'),
    path('<str:story_id>/', StoryDetailView.as_view(), name='story-detail'),
    path('<str:story_id>/publish/', StoryPublishView.as_view(), name='story-publish'),
]
