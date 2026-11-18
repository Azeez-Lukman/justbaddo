"""
API views for the music catalogue, albums, tracks, search, and career timeline.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.response import api_success, api_error
from music.services import MusicService
from music.serializers import (
    AlbumSummarySerializer,
    AlbumDetailSerializer,
    TrackDetailSerializer,
    SingleReleaseSerializer,
    TimelineMilestoneSerializer
)

class ArtistInfoView(APIView):
    """
    Get artist biographical profile and discography statistics.
    GET /api/v1/music/artist/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        info = MusicService.get_artist_info()
        return api_success(data=info)

class AlbumListView(APIView):
    """
    List albums and EPs with optional filtering and sorting.
    GET /api/v1/music/albums/?type=EP&sort=year_desc&q=ikigai
    """
    permission_classes = [AllowAny]

    def get(self, request):
        album_type = request.query_params.get('type')
        search = request.query_params.get('q')
        sort = request.query_params.get('sort', 'year_desc')

        albums = MusicService.list_albums(album_type=album_type, search=search, sort=sort)
        serializer = AlbumSummarySerializer(albums, many=True)
        return api_success(data=serializer.data, meta={'count': len(albums)})

class AlbumDetailView(APIView):
    """
    Get full album details, tracklist, and verified production credits.
    GET /api/v1/music/albums/<slug>/
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        album = MusicService.get_album_by_slug(slug)
        if not album:
            return api_error(message=f"Album '{slug}' not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        serializer = AlbumDetailSerializer(album)
        return api_success(data=serializer.data)

class SinglesListView(APIView):
    """
    List standalone singles and major collaborations.
    GET /api/v1/music/singles/?q=wo
    """
    permission_classes = [AllowAny]

    def get(self, request):
        search = request.query_params.get('q')
        singles = MusicService.list_singles(search=search)
        serializer = SingleReleaseSerializer(singles, many=True)
        return api_success(data=serializer.data, meta={'count': len(singles)})

class TrackDetailView(APIView):
    """
    Get detailed track metadata, key/BPM, credits, and playback status.
    GET /api/v1/music/tracks/<id>/
    """
    permission_classes = [AllowAny]

    def get(self, request, track_id):
        track = MusicService.get_track_by_id(track_id)
        if not track:
            return api_error(message=f"Track '{track_id}' not found in catalogue.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        serializer = TrackDetailSerializer(track)
        return api_success(data=serializer.data)

class GlobalCatalogueSearchView(APIView):
    """
    Unified search across albums, tracks, and singles.
    GET /api/v1/music/search/?q=baddo
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        results = MusicService.search_catalogue(query)
        return api_success(data=results, meta={'query': query})

class CareerTimelineView(APIView):
    """
    List verified chronological milestones from 2010 to present.
    GET /api/v1/music/timeline/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        timeline = MusicService.get_timeline()
        serializer = TimelineMilestoneSerializer(timeline, many=True)
        return api_success(data=serializer.data, meta={'count': len(timeline)})
