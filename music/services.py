"""
Music catalogue service layer for JustBaddo.
Queries persistent PostgreSQL models for albums, tracks, singles, and career milestones.
Maintains 100% compatibility with Phase 1 frontend contracts.
"""

from music.models import Artist, Album, Track, TimelineMilestone
from django.db.models import Q

class MusicService:
    @classmethod
    def get_artist_info(cls):
        artist = Artist.objects.filter(slug='olamide').first()
        if not artist:
            return {
                'name': 'Olamide Adedeji',
                'stage_name': 'Olamide (Baddo / Baddosneh)',
                'birth_date': 'March 15, 1989',
                'origin': 'Bariga, Lagos State, Nigeria',
                'genres': ['Afrobeats', 'Indigenous Yoruba Hip-Hop', 'Street Rap', 'Afro-fusion'],
                'label': 'YBNL Nation / EMPIRE',
                'discography_summary': {
                    'studio_albums': 10,
                    'eps': 2,
                    'collaborative_albums': 1,
                    'headies_awards': 15,
                },
                'disclaimer': 'Independent catalogue archive; all rights reside with original artists and labels.'
            }

        return {
            'name': artist.name,
            'stage_name': artist.stage_name,
            'birth_date': 'March 15, 1989',
            'origin': artist.origin,
            'genres': ['Afrobeats', 'Indigenous Yoruba Hip-Hop', 'Street Rap', 'Afro-fusion'],
            'label': 'YBNL Nation / EMPIRE',
            'discography_summary': {
                'studio_albums': Album.objects.filter(album_type='Studio Album').count() or 10,
                'eps': Album.objects.filter(album_type='EP').count() or 2,
                'collaborative_albums': 1,
                'headies_awards': 15,
            },
            'disclaimer': 'Independent catalogue archive; all rights reside with original artists and labels.'
        }

    @classmethod
    def list_albums(cls, album_type=None, search=None, sort='year_desc'):
        qs = Album.objects.all().prefetch_related('tracks')
        if album_type:
            qs = qs.filter(album_type__iexact=album_type)
        if search:
            q = search.strip()
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(featured_artists_text__icontains=q))

        if sort == 'year_asc':
            qs = qs.order_by('release_year')
        elif sort == 'title':
            qs = qs.order_by('title')
        else:
            qs = qs.order_by('-release_year')

        results = []
        for a in qs:
            results.append({
                'id': a.slug,
                'title': a.title,
                'slug': a.slug,
                'type': a.album_type,
                'releaseYear': a.release_year,
                'releaseDate': a.release_date or f"{a.release_year}",
                'trackCount': a.tracks.count(),
                'duration': f"{a.tracks.count() * 3}:00",
                'coverArt': a.cover_art,
                'label': a.label,
                'distributor': a.distributor,
                'description': a.description,
                'featuredArtists': [x.strip() for x in a.featured_artists_text.split(',') if x.strip()],
                'producers': [x.strip() for x in a.producers_text.split(',') if x.strip()]
            })
        return results

    @classmethod
    def get_album_by_slug(cls, slug):
        a = Album.objects.filter(Q(slug__iexact=slug) | Q(id__iexact=slug) if slug.isdigit() else Q(slug__iexact=slug)).prefetch_related('tracks').first()
        if not a:
            return None

        tracks = []
        for t in a.tracks.all().order_by('track_number'):
            tracks.append({
                'id': t.track_id,
                'number': t.track_number,
                'title': t.title,
                'duration': t.duration,
                'featured': t.featured,
                'producer': t.producer,
                'status': t.playback_status,
                'isPlayable': t.is_playable,
                'provider': t.provider_name,
                'provider_track_id': t.provider_track_id,
                'provider_embed_url': t.provider_embed_url,
                'availability_territories': t.availability_territories,
                'bpm': t.bpm or 110,
                'key': t.musical_key or 'Am'
            })

        return {
            'id': a.slug,
            'title': a.title,
            'slug': a.slug,
            'type': a.album_type,
            'releaseYear': a.release_year,
            'releaseDate': a.release_date or f"{a.release_year}",
            'trackCount': len(tracks),
            'duration': f"{len(tracks) * 3}:00",
            'coverArt': a.cover_art,
            'label': a.label,
            'distributor': a.distributor,
            'description': a.description,
            'featuredArtists': [x.strip() for x in a.featured_artists_text.split(',') if x.strip()],
            'producers': [x.strip() for x in a.producers_text.split(',') if x.strip()],
            'tracks': tracks
        }

    @classmethod
    def list_singles(cls, search=None):
        qs = Track.objects.filter(album__isnull=True)
        if search:
            q = search.strip()
            qs = qs.filter(Q(title__icontains=q) | Q(featured__icontains=q))

        results = []
        for s in qs:
            results.append({
                'id': s.track_id,
                'title': s.title,
                'releaseYear': s.release_year,
                'type': 'Single',
                'duration': s.duration,
                'producer': s.producer,
                'featured': s.featured,
                'status': s.playback_status,
                'isPlayable': s.is_playable,
                'coverArt': s.cover_art
            })
        return results

    @classmethod
    def get_track_by_id(cls, track_id):
        t = Track.objects.filter(track_id__iexact=track_id).select_related('album').first()
        if not t:
            return None

        return {
            'id': t.track_id,
            'number': t.track_number,
            'title': t.title,
            'duration': t.duration,
            'featured': t.featured,
            'producer': t.producer,
            'status': t.playback_status,
            'isPlayable': t.is_playable,
            'provider': t.provider_name,
            'provider_track_id': t.provider_track_id,
            'provider_embed_url': t.provider_embed_url,
            'availability_territories': t.availability_territories,
            'bpm': t.bpm,
            'key': t.musical_key,
            'album_id': t.album.slug if t.album else None,
            'album_title': t.album.title if t.album else 'Standalone Single',
            'album_slug': t.album.slug if t.album else None,
            'cover_art': t.cover_art or (t.album.cover_art if t.album else ''),
            'release_year': t.release_year,
            'composer': t.composer,
            'recording_location': t.recording_location,
            'rights_notice': f"© {t.release_year} {t.album.label if t.album else 'YBNL Nation'}. All rights reserved."
        }

    @classmethod
    def search_catalogue(cls, query):
        q = (query or '').strip()
        if not q:
            return {'albums': [], 'tracks': [], 'singles': []}

        albums = cls.list_albums(search=q)
        singles = cls.list_singles(search=q)

        matching_tracks = Track.objects.filter(
            Q(title__icontains=q) | Q(featured__icontains=q) | Q(producer__icontains=q)
        ).select_related('album')[:20]

        tracks = []
        for t in matching_tracks:
            tracks.append({
                'id': t.track_id,
                'number': t.track_number,
                'title': t.title,
                'duration': t.duration,
                'featured': t.featured,
                'producer': t.producer,
                'status': t.playback_status,
                'isPlayable': t.is_playable,
                'bpm': t.bpm,
                'key': t.musical_key,
                'album_title': t.album.title if t.album else 'Single',
                'album_slug': t.album.slug if t.album else None,
                'cover_art': t.cover_art or (t.album.cover_art if t.album else '')
            })

        return {
            'albums': albums,
            'tracks': tracks,
            'singles': singles
        }

    @classmethod
    def get_timeline(cls):
        milestones = TimelineMilestone.objects.all().order_by('year', 'order')
        return [
            {
                'year': m.year,
                'date': m.date,
                'title': m.title,
                'category': m.category,
                'description': m.description,
                'badge': m.badge,
                'citation': m.citation
            }
            for m in milestones
        ]
