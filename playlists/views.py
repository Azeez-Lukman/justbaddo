"""
API views for user playlists and editorial collections.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from core.response import api_success, api_error
from playlists.services import PlaylistService
from playlists.serializers import (
    PlaylistSummarySerializer,
    PlaylistDetailSerializer,
    PlaylistCreateSerializer,
    PlaylistAddTrackSerializer
)

class PlaylistListCreateView(APIView):
    """
    List playlists or create a new user playlist.
    GET /api/v1/playlists/
    POST /api/v1/playlists/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        playlists = PlaylistService.list_playlists(username=username)
        serializer = PlaylistSummarySerializer(playlists, many=True)
        return api_success(data=serializer.data, meta={'count': len(playlists)})

    def post(self, request):
        serializer = PlaylistCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid playlist payload.", code="VALIDATION_ERROR", errors=serializer.errors)

        creator = request.user.username if request.user.is_authenticated else 'baddofan99'
        created_pl = PlaylistService.create_playlist(
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', ''),
            creator=creator,
            is_private=serializer.validated_data.get('is_private', False),
            cover_image=serializer.validated_data.get('cover_image')
        )
        return api_success(data=created_pl, message="Playlist created successfully.", status_code=status.HTTP_201_CREATED)

class PlaylistDetailView(APIView):
    """
    Retrieve, edit, or delete a playlist.
    GET /api/v1/playlists/<id>/
    PATCH /api/v1/playlists/<id>/
    DELETE /api/v1/playlists/<id>/
    """
    permission_classes = [AllowAny]

    def get(self, request, playlist_id):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        pl = PlaylistService.get_playlist_by_id(playlist_id, username=username)
        if not pl:
            return api_error(message=f"Playlist '{playlist_id}' not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistDetailSerializer(pl)
        return api_success(data=serializer.data)

    def patch(self, request, playlist_id):
        creator = request.user.username if request.user.is_authenticated else 'baddofan99'
        updated = PlaylistService.update_playlist(playlist_id, creator=creator, data=request.data)
        if not updated:
            return api_error(message="Playlist not found or permission denied.", code="FORBIDDEN", status_code=status.HTTP_403_FORBIDDEN)
        return api_success(data=updated, message="Playlist updated.")

    def delete(self, request, playlist_id):
        creator = request.user.username if request.user.is_authenticated else 'baddofan99'
        success, message = PlaylistService.delete_playlist(playlist_id, creator=creator)
        if not success:
            return api_error(message=message, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST)
        return api_success(message=message)

class PlaylistTrackActionView(APIView):
    """
    Add track to playlist or remove track from playlist.
    POST /api/v1/playlists/<id>/tracks/
    DELETE /api/v1/playlists/<id>/tracks/<track_id>/
    """
    permission_classes = [AllowAny]

    def post(self, request, playlist_id):
        serializer = PlaylistAddTrackSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid track payload.", code="VALIDATION_ERROR", errors=serializer.errors)

        creator = request.user.username if request.user.is_authenticated else 'baddofan99'
        success, msg = PlaylistService.add_track_to_playlist(
            playlist_id=playlist_id,
            track_id=serializer.validated_data['track_id'],
            creator=creator
        )
        if not success:
            return api_error(message=msg, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST)
        return api_success(message=msg, status_code=status.HTTP_201_CREATED)

    def delete(self, request, playlist_id, track_id):
        creator = request.user.username if request.user.is_authenticated else 'baddofan99'
        success, msg = PlaylistService.remove_track_from_playlist(
            playlist_id=playlist_id,
            track_id=track_id,
            creator=creator
        )
        if not success:
            return api_error(message=msg, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST)
        return api_success(message=msg)
