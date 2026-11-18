"""
URL routing for music catalogue endpoints.
"""

from django.urls import path
from music.views import (
    ArtistInfoView,
    AlbumListView,
    AlbumDetailView,
    SinglesListView,
    TrackDetailView,
    GlobalCatalogueSearchView,
    CareerTimelineView
)

app_name = 'music'

urlpatterns = [
    path('artist/', ArtistInfoView.as_view(), name='artist-info'),
    path('albums/', AlbumListView.as_view(), name='album-list'),
    path('albums/<slug:slug>/', AlbumDetailView.as_view(), name='album-detail'),
    path('singles/', SinglesListView.as_view(), name='singles-list'),
    path('tracks/<str:track_id>/', TrackDetailView.as_view(), name='track-detail'),
    path('search/', GlobalCatalogueSearchView.as_view(), name='catalogue-search'),
    path('timeline/', CareerTimelineView.as_view(), name='career-timeline'),
]
