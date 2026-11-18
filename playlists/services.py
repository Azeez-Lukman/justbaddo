"""
Playlist service layer for JustBaddo.
Manages user playlists, editorial collections, track insertions, and access rules.
"""

from music.services import MusicService
import uuid
import datetime

class PlaylistService:
    """
    In-memory playlist repository for Phase 2.
    """

    _playlists = [
        {
            'id': 'pl-editorial-01',
            'title': 'Baddo Street Anthems',
            'description': 'The definitive high-octane club & street anthems that rocked Lagos and global stages.',
            'creator': 'JustBaddo Editorial',
            'is_editorial': True,
            'is_private': False,
            'cover_image': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80',
            'updated_at': '2024-06-28',
            'tracks': [
                {'id': 's-03', 'title': 'Wo!!', 'duration': '3:15', 'albumTitle': 'Single', 'coverArt': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80', 'status': 'JUSTBADDO_STREAMING'},
                {'id': 's-04', 'title': 'Science Student', 'duration': '3:12', 'albumTitle': 'Single', 'coverArt': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=400&q=80', 'status': 'JUSTBADDO_STREAMING'},
                {'id': 's-01', 'title': 'Motigbana', 'duration': '3:15', 'albumTitle': 'Single', 'coverArt': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80', 'status': 'JUSTBADDO_STREAMING'},
                {'id': 'rap-01', 'title': 'Eni Duro', 'duration': '4:15', 'albumTitle': 'Rapsodi', 'coverArt': 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=400&q=80', 'status': 'JUSTBADDO_STREAMING'}
            ]
        },
        {
            'id': 'pl-editorial-02',
            'title': 'Melodic & Introspective Baddo',
            'description': 'Soulful, relaxed Afro-fusion cuts showcasing Olamide poetic depth and vocal maturity.',
            'creator': 'JustBaddo Editorial',
            'is_editorial': True,
            'is_private': False,
            'cover_image': 'https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=400&q=80',
            'updated_at': '2024-06-28',
            'tracks': [
                {'id': 'cpd-03', 'title': 'Infinity', 'duration': '2:52', 'albumTitle': 'Carpe Diem', 'coverArt': 'https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=400&q=80', 'status': 'JUSTBADDO_STREAMING'},
                {'id': 'uys-03', 'title': 'Rock', 'duration': '3:05', 'albumTitle': 'UY Scuti', 'coverArt': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=400&q=80', 'status': 'JUSTBADDO_STREAMING'},
                {'id': 'iki-07', 'title': 'Morowore', 'duration': '3:21', 'albumTitle': 'Ikigai, Vol. 1', 'coverArt': 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=400&q=80', 'status': 'JUSTBADDO_STREAMING'}
            ]
        },
        {
            'id': 'pl-user-01',
            'title': 'My Daily Baddo Rotation',
            'description': 'My personal daily commute favorites.',
            'creator': 'baddofan99',
            'is_editorial': False,
            'is_private': False,
            'cover_image': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80',
            'updated_at': '2024-07-01',
            'tracks': [
                {'id': 'iki-02', 'title': 'Uptown Disco', 'duration': '3:12', 'albumTitle': 'Ikigai, Vol. 1', 'coverArt': 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=400&q=80', 'status': 'JUSTBADDO_STREAMING'},
                {'id': 'cpd-05', 'title': 'Loading', 'duration': '3:15', 'albumTitle': 'Carpe Diem', 'coverArt': 'https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=400&q=80', 'status': 'JUSTBADDO_STREAMING'}
            ]
        }
    ]

    @classmethod
    def list_playlists(cls, username=None, include_private=False):
        results = []
        for pl in cls._playlists:
            # Editorial always visible
            if pl['is_editorial']:
                results.append(cls._format_summary(pl))
            # User playlists
            elif pl['creator'] == username:
                results.append(cls._format_summary(pl))
            elif not pl['is_private']:
                results.append(cls._format_summary(pl))
        return results

    @classmethod
    def get_playlist_by_id(cls, playlist_id, username=None):
        pl = next((p for p in cls._playlists if p['id'] == playlist_id), None)
        if not pl:
            return None
        if pl['is_private'] and pl['creator'] != username:
            return None
        return {
            **pl,
            'track_count': len(pl['tracks'])
        }

    @classmethod
    def create_playlist(cls, title, description, creator, is_private=False, cover_image=None):
        playlist_id = f"pl-user-{uuid.uuid4().hex[:6]}"
        new_pl = {
            'id': playlist_id,
            'title': title,
            'description': description or '',
            'creator': creator,
            'is_editorial': False,
            'is_private': is_private,
            'cover_image': cover_image or 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80',
            'updated_at': datetime.date.today().isoformat(),
            'tracks': []
        }
        cls._playlists.append(new_pl)
        return cls.get_playlist_by_id(playlist_id, username=creator)

    @classmethod
    def update_playlist(cls, playlist_id, creator, data):
        pl = next((p for p in cls._playlists if p['id'] == playlist_id and p['creator'] == creator), None)
        if not pl:
            return None
        if 'title' in data:
            pl['title'] = data['title']
        if 'description' in data:
            pl['description'] = data['description']
        if 'is_private' in data:
            pl['is_private'] = data['is_private']
        if 'cover_image' in data and data['cover_image']:
            pl['cover_image'] = data['cover_image']
        pl['updated_at'] = datetime.date.today().isoformat()
        return cls.get_playlist_by_id(playlist_id, username=creator)

    @classmethod
    def delete_playlist(cls, playlist_id, creator):
        for idx, pl in enumerate(cls._playlists):
            if pl['id'] == playlist_id:
                if pl['creator'] != creator:
                    return False, "You do not have permission to delete this playlist."
                cls._playlists.pop(idx)
                return True, "Playlist deleted successfully."
        return False, "Playlist not found."

    @classmethod
    def add_track_to_playlist(cls, playlist_id, track_id, creator):
        pl = next((p for p in cls._playlists if p['id'] == playlist_id), None)
        if not pl:
            return False, "Playlist not found."
        if pl['creator'] != creator:
            return False, "You do not own this playlist."

        # Verify track
        track = MusicService.get_track_by_id(track_id)
        if not track:
            return False, "Track not found in catalogue."

        if any(t['id'] == track_id for t in pl['tracks']):
            return False, "Track already exists in this playlist."

        pl['tracks'].append({
            'id': track['id'],
            'title': track['title'],
            'duration': track['duration'],
            'albumTitle': track.get('album_title', 'Single'),
            'coverArt': track.get('cover_art', ''),
            'status': track.get('status', 'JUSTBADDO_STREAMING')
        })
        pl['updated_at'] = datetime.date.today().isoformat()
        return True, "Track added to playlist."

    @classmethod
    def remove_track_from_playlist(cls, playlist_id, track_id, creator):
        pl = next((p for p in cls._playlists if p['id'] == playlist_id), None)
        if not pl:
            return False, "Playlist not found."
        if pl['creator'] != creator:
            return False, "You do not own this playlist."

        before_len = len(pl['tracks'])
        pl['tracks'] = [t for t in pl['tracks'] if t['id'] != track_id]
        if len(pl['tracks']) == before_len:
            return False, "Track was not in this playlist."

        pl['updated_at'] = datetime.date.today().isoformat()
        return True, "Track removed from playlist."

    @staticmethod
    def _format_summary(pl):
        return {
            'id': pl['id'],
            'title': pl['title'],
            'description': pl['description'],
            'creator': pl['creator'],
            'is_editorial': pl['is_editorial'],
            'is_private': pl['is_private'],
            'track_count': len(pl['tracks']),
            'cover_image': pl['cover_image'],
            'updated_at': pl['updated_at']
        }
