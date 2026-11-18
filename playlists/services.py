"""
Playlist service layer for JustBaddo.
Manages user playlists and editorial collections in PostgreSQL.
"""

from playlists.models import Playlist, PlaylistTrack
from music.models import Track
from django.contrib.auth.models import User
import uuid

class PlaylistService:
    @classmethod
    def list_playlists(cls, username=None, include_private=False):
        qs = Playlist.objects.all().prefetch_related('playlist_tracks__track')
        results = []
        for pl in qs:
            if pl.is_editorial:
                results.append(cls._format_summary(pl))
            elif pl.creator.username == username:
                results.append(cls._format_summary(pl))
            elif not pl.is_private:
                results.append(cls._format_summary(pl))
        return results

    @classmethod
    def get_playlist_by_id(cls, playlist_id, username=None):
        pl = Playlist.objects.filter(playlist_id=playlist_id).prefetch_related('playlist_tracks__track__album').first()
        if not pl:
            return None
        if pl.is_private and pl.creator.username != username:
            return None

        tracks = []
        for pt in pl.playlist_tracks.all().order_by('order', 'added_at'):
            t = pt.track
            tracks.append({
                'id': t.track_id,
                'title': t.title,
                'duration': t.duration,
                'albumTitle': t.album.title if t.album else 'Single',
                'coverArt': t.cover_art or (t.album.cover_art if t.album else ''),
                'status': t.playback_status
            })

        return {
            'id': pl.playlist_id,
            'title': pl.title,
            'description': pl.description,
            'creator': pl.creator.username,
            'is_editorial': pl.is_editorial,
            'is_private': pl.is_private,
            'track_count': len(tracks),
            'cover_image': pl.cover_image or 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80',
            'updated_at': pl.updated_at.strftime('%Y-%m-%d') if pl.updated_at else '2024-07-01',
            'tracks': tracks
        }

    @classmethod
    def create_playlist(cls, title, description, creator, is_private=False, cover_image=None):
        user, _ = User.objects.get_or_create(username=creator, defaults={'email': f"{creator}@justbaddo.local"})
        playlist_id = f"pl-user-{uuid.uuid4().hex[:6]}"

        pl = Playlist.objects.create(
            playlist_id=playlist_id,
            title=title,
            description=description or '',
            creator=user,
            is_editorial=False,
            is_private=is_private,
            cover_image=cover_image or 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80'
        )
        return cls.get_playlist_by_id(playlist_id, username=creator)

    @classmethod
    def update_playlist(cls, playlist_id, creator, data):
        pl = Playlist.objects.filter(playlist_id=playlist_id, creator__username=creator).first()
        if not pl:
            return None
        if 'title' in data:
            pl.title = data['title']
        if 'description' in data:
            pl.description = data['description']
        if 'is_private' in data:
            pl.is_private = data['is_private']
        if 'cover_image' in data and data['cover_image']:
            pl.cover_image = data['cover_image']
        pl.save()
        return cls.get_playlist_by_id(playlist_id, username=creator)

    @classmethod
    def delete_playlist(cls, playlist_id, creator):
        pl = Playlist.objects.filter(playlist_id=playlist_id).first()
        if not pl:
            return False, "Playlist not found."
        if pl.creator.username != creator:
            return False, "You do not have permission to delete this playlist."
        pl.delete()
        return True, "Playlist deleted successfully."

    @classmethod
    def add_track_to_playlist(cls, playlist_id, track_id, creator):
        pl = Playlist.objects.filter(playlist_id=playlist_id).first()
        if not pl:
            return False, "Playlist not found."
        if pl.creator.username != creator:
            return False, "You do not own this playlist."

        track = Track.objects.filter(track_id__iexact=str(track_id)).first()
        if not track and str(track_id).isdigit():
            track = Track.objects.filter(id=int(track_id)).first()
        if not track:
            return False, "Track not found in catalogue."

        if PlaylistTrack.objects.filter(playlist=pl, track=track).exists():
            return False, "Track already exists in this playlist."

        next_order = pl.playlist_tracks.count()
        PlaylistTrack.objects.create(playlist=pl, track=track, order=next_order)
        return True, "Track added to playlist."

    @classmethod
    def remove_track_from_playlist(cls, playlist_id, track_id, creator):
        pl = Playlist.objects.filter(playlist_id=playlist_id).first()
        if not pl:
            return False, "Playlist not found."
        if pl.creator.username != creator:
            return False, "You do not own this playlist."

        pt = PlaylistTrack.objects.filter(playlist=pl, track__track_id__iexact=str(track_id)).first()
        if not pt and str(track_id).isdigit():
            pt = PlaylistTrack.objects.filter(playlist=pl, track__id=int(track_id)).first()
        if not pt:
            return False, "Track was not in this playlist."

        pt.delete()
        return True, "Track removed from playlist."

    @staticmethod
    def _format_summary(pl):
        return {
            'id': pl.playlist_id,
            'title': pl.title,
            'description': pl.description,
            'creator': pl.creator.username,
            'is_editorial': pl.is_editorial,
            'is_private': pl.is_private,
            'track_count': pl.playlist_tracks.count(),
            'cover_image': pl.cover_image or 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80',
            'updated_at': pl.updated_at.strftime('%Y-%m-%d') if pl.updated_at else '2024-07-01'
        }
