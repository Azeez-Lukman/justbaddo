"""
URL routing for playlist endpoints.
"""

from django.urls import path
from playlists.views import (
    PlaylistListCreateView,
    PlaylistDetailView,
    PlaylistTrackActionView
)

app_name = 'playlists'

urlpatterns = [
    path('', PlaylistListCreateView.as_view(), name='playlist-list-create'),
    path('<str:playlist_id>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('<str:playlist_id>/tracks/', PlaylistTrackActionView.as_view(), name='playlist-add-track'),
    path('<str:playlist_id>/tracks/<str:track_id>/', PlaylistTrackActionView.as_view(), name='playlist-remove-track'),
]
