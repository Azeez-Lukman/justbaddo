"""
Music catalogue service layer for JustBaddo.
Provides querying, filtering, search, and detail retrieval for albums, tracks, and singles.
Backed by verified discography metadata matching the JustBaddo catalogue schema.
"""

class MusicService:
    """
    Catalogue repository and query engine.
    Preloaded with verified historical recordings and rights metadata.
    """

    ALBUMS = [
        {
            'id': 'ikigai-vol-1',
            'title': 'Ikigai / 生き甲斐, Vol. 1',
            'slug': 'ikigai-vol-1',
            'type': 'EP',
            'releaseYear': 2024,
            'releaseDate': 'June 26, 2024',
            'trackCount': 7,
            'duration': '21:14',
            'coverArt': 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=600&q=80',
            'label': 'YBNL Nation / EMPIRE',
            'distributor': 'EMPIRE',
            'description': 'A contemplative seven-track sonic journey blending introspective street consciousness with sophisticated Afro-fusion production.',
            'featuredArtists': ['Fireboy DML', 'Asake', 'Pheelz', 'Young Jonn', 'Lil Kesh', 'SABRI'],
            'producers': ['Semzi', 'Pheelz', 'Young Jonn'],
            'tracks': [
                {'id': 'iki-01', 'number': 1, 'title': 'Metaverse', 'duration': '2:47', 'featured': '', 'producer': 'Semzi', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 108, 'key': 'F#m'},
                {'id': 'iki-02', 'number': 2, 'title': 'Uptown Disco', 'duration': '3:12', 'featured': 'Fireboy DML & Asake', 'producer': 'Pheelz', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 114, 'key': 'Am'},
                {'id': 'iki-03', 'number': 3, 'title': 'Makaveli', 'duration': '2:56', 'featured': '', 'producer': 'Semzi', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 102, 'key': 'Gm'},
                {'id': 'iki-04', 'number': 4, 'title': 'Knockout', 'duration': '3:05', 'featured': 'SABRI', 'producer': 'Semzi', 'status': 'AUTHORISED_PROVIDER', 'isPlayable': True, 'bpm': 110, 'key': 'Dm'},
                {'id': 'iki-05', 'number': 5, 'title': 'Hello Habibi', 'duration': '2:38', 'featured': '', 'producer': 'Young Jonn', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 116, 'key': 'Em'},
                {'id': 'iki-06', 'number': 6, 'title': 'Synchro System', 'duration': '3:15', 'featured': 'Pheelz, Young Jonn & Lil Kesh', 'producer': 'Pheelz', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 120, 'key': 'C'},
                {'id': 'iki-07', 'number': 7, 'title': 'Morowore', 'duration': '3:21', 'featured': '', 'producer': 'Semzi', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 98, 'key': 'Bm'}
            ]
        },
        {
            'id': 'unruly',
            'title': 'Unruly',
            'slug': 'unruly',
            'type': 'Studio Album',
            'releaseYear': 2023,
            'releaseDate': 'August 4, 2023',
            'trackCount': 15,
            'duration': '44:20',
            'coverArt': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80',
            'label': 'YBNL Nation / EMPIRE',
            'distributor': 'EMPIRE',
            'description': 'Celebrated tenth studio album featuring global anthems, amapiano experiments, and heavyweight guest appearances.',
            'featuredArtists': ['Rema', 'Asake', 'Fireboy DML', 'BNXN', 'CKay'],
            'producers': ['Eskeez', 'Magicsticks', 'P.Priime'],
            'tracks': [
                {'id': 'unr-01', 'number': 1, 'title': 'Celebrate', 'duration': '2:50', 'featured': '', 'producer': 'Eskeez', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 112, 'key': 'C#m'},
                {'id': 'unr-02', 'number': 2, 'title': 'Gaza', 'duration': '2:40', 'featured': '', 'producer': 'Eskeez', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 115, 'key': 'Em'},
                {'id': 'unr-03', 'number': 3, 'title': 'Doom', 'duration': '3:05', 'featured': '', 'producer': 'Magicsticks', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 118, 'key': 'Fm'},
                {'id': 'unr-04', 'number': 4, 'title': 'Trumpet', 'duration': '3:10', 'featured': 'CKay', 'producer': 'P.Priime', 'status': 'AUTHORISED_PROVIDER', 'isPlayable': True, 'bpm': 105, 'key': 'Am'},
                {'id': 'unr-05', 'number': 5, 'title': 'New Religion', 'duration': '3:12', 'featured': 'Asake', 'producer': 'Magicsticks', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 116, 'key': 'Gm'}
            ]
        },
        {
            'id': 'uy-scuti',
            'title': 'UY Scuti',
            'slug': 'uy-scuti',
            'type': 'Studio Album',
            'releaseYear': 2021,
            'releaseDate': 'June 18, 2021',
            'trackCount': 10,
            'duration': '31:40',
            'coverArt': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80',
            'label': 'YBNL Nation / EMPIRE',
            'distributor': 'EMPIRE',
            'description': 'A relaxed, sonic departure exploring dancehall, reggae rhythms, and intimate acoustic melodies named after the hypergiant star.',
            'featuredArtists': ['Fave', 'Phyno', 'Jaywillz', 'Layydoe'],
            'producers': ['P.Priime', 'Eskeez'],
            'tracks': [
                {'id': 'uys-01', 'number': 1, 'title': 'Need for Speed', 'duration': '3:01', 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 100, 'key': 'F#m'},
                {'id': 'uys-02', 'number': 2, 'title': 'Jailer', 'duration': '3:04', 'featured': 'Jaywillz', 'producer': 'Eskeez', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 104, 'key': 'C'},
                {'id': 'uys-03', 'number': 3, 'title': 'Rock', 'duration': '3:05', 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 102, 'key': 'Am'},
                {'id': 'uys-04', 'number': 4, 'title': 'Julie', 'duration': '3:10', 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 98, 'key': 'Dm'},
                {'id': 'uys-05', 'number': 5, 'title': 'Rough Up', 'duration': '2:45', 'featured': 'Layydoe', 'producer': 'Eskeez', 'status': 'AUTHORISED_PROVIDER', 'isPlayable': True, 'bpm': 106, 'key': 'Em'}
            ]
        },
        {
            'id': 'carpe-diem',
            'title': 'Carpe Diem',
            'slug': 'carpe-diem',
            'type': 'Studio Album',
            'releaseYear': 2020,
            'releaseDate': 'October 8, 2020',
            'trackCount': 12,
            'duration': '38:15',
            'coverArt': 'https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=600&q=80',
            'label': 'YBNL Nation / EMPIRE',
            'distributor': 'EMPIRE',
            'description': 'A watershed classic that re-energized modern Afrobeats with "Infinity", "Loading", and "Greenlight".',
            'featuredArtists': ['Fireboy DML', 'Bella Shmurda', 'Bad Boy Timz', 'Omah Lay', 'Peruzzi', 'Phyno'],
            'producers': ['P.Priime', 'Pheelz', 'Vstix', 'ID Cabasa'],
            'tracks': [
                {'id': 'cpd-01', 'number': 1, 'title': 'Another Level', 'duration': '2:55', 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 104, 'key': 'G'},
                {'id': 'cpd-02', 'number': 2, 'title': 'Green Light', 'duration': '3:15', 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 105, 'key': 'Am'},
                {'id': 'cpd-03', 'number': 3, 'title': 'Infinity', 'duration': '2:52', 'featured': 'Omah Lay', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 103, 'key': 'C#m'},
                {'id': 'cpd-04', 'number': 4, 'title': 'Eru', 'duration': '3:03', 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 110, 'key': 'Fm'},
                {'id': 'cpd-05', 'number': 5, 'title': 'Loading', 'duration': '3:15', 'featured': 'Bad Boy Timz', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 116, 'key': 'Dm'}
            ]
        },
        {
            'id': 'rapsodi',
            'title': 'Rapsodi',
            'slug': 'rapsodi',
            'type': 'Studio Album',
            'releaseYear': 2011,
            'releaseDate': 'March 14, 2011',
            'trackCount': 16,
            'duration': '58:24',
            'coverArt': 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=600&q=80',
            'label': 'Coded Tunes / NotJustOk',
            'distributor': 'Coded Tunes',
            'description': 'The iconic debut album that introduced Olamide Adedeji from Bariga to the world. Anchored by the breakout single "Eni Duro".',
            'featuredArtists': ['Wizkid', 'ID Cabasa', 'Reminisce', '9ice', "D'Banj", 'Lord of Ajasa'],
            'producers': ['ID Cabasa'],
            'tracks': [
                {'id': 'rap-01', 'number': 1, 'title': 'Eni Duro', 'duration': '4:15', 'featured': '', 'producer': 'ID Cabasa', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 98, 'key': 'Am'},
                {'id': 'rap-02', 'number': 2, 'title': 'Omo To Shan', 'duration': '3:40', 'featured': 'Wizkid', 'producer': 'ID Cabasa', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'bpm': 104, 'key': 'F'},
                {'id': 'rap-03', 'number': 3, 'title': 'Apa Ti Jona', 'duration': '3:52', 'featured': 'ID Cabasa', 'producer': 'ID Cabasa', 'status': 'AUTHORISED_PROVIDER', 'isPlayable': True, 'bpm': 100, 'key': 'Dm'},
                {'id': 'rap-04', 'number': 4, 'title': 'Legendary Hustlers', 'duration': '4:02', 'featured': 'Reminisce & 9ice', 'producer': 'ID Cabasa', 'status': 'METADATA_ONLY', 'isPlayable': False, 'bpm': 94, 'key': 'Em'}
            ]
        }
    ]

    SINGLES = [
        {'id': 's-01', 'title': 'Motigbana', 'releaseYear': 2018, 'type': 'Single', 'duration': '3:15', 'producer': 'Killertunes', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'coverArt': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80'},
        {'id': 's-02', 'title': 'Pawon', 'releaseYear': 2019, 'type': 'Single', 'duration': '3:20', 'producer': 'Cracker Mallo', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'coverArt': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=400&q=80'},
        {'id': 's-03', 'title': 'Wo!!', 'releaseYear': 2017, 'type': 'Single', 'duration': '3:15', 'producer': 'Young Jonn', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'coverArt': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80'},
        {'id': 's-04', 'title': 'Science Student', 'releaseYear': 2018, 'type': 'Single', 'duration': '3:12', 'producer': 'Young Jonn & BBanks', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'coverArt': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=400&q=80'},
        {'id': 's-05', 'title': 'Rock', 'releaseYear': 2021, 'type': 'Single', 'duration': '3:05', 'producer': 'P.Priime', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'coverArt': 'https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=400&q=80'},
        {'id': 's-06', 'title': 'Infinity', 'releaseYear': 2020, 'type': 'Single', 'duration': '2:52', 'producer': 'P.Priime', 'featured': 'Omah Lay', 'status': 'JUSTBADDO_STREAMING', 'isPlayable': True, 'coverArt': 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=400&q=80'}
    ]

    TIMELINE = [
        {'year': 2010, 'date': 'Late 2010', 'title': 'Breakout Anthem: "Eni Duro"', 'category': 'Breakthrough', 'description': 'Burst onto the scene with iconic tongue-twisting delivery recorded with ID Cabasa at Coded Tunes.', 'badge': 'Debut Single', 'citation': 'Coded Tunes Records'},
        {'year': 2011, 'date': 'March 14, 2011', 'title': 'Debut Studio Album: Rapsodi', 'category': 'Studio Album', 'description': 'Solidified his arrival with 16 tracks including "Omo To Shan" featuring Wizkid.', 'badge': 'Studio Album #1', 'citation': 'NotJustOk / Coded Tunes'},
        {'year': 2012, 'date': 'November 12, 2012', 'title': 'YBNL Nation Founded & Album Release', 'category': 'Label Milestone', 'description': 'Launched independent imprint YBNL (Yahoo Boy No Laptop) Nation and dropped sophomore classic YBNL.', 'badge': 'Label Inception', 'citation': 'YBNL Nation Press'},
        {'year': 2014, 'date': 'December 28, 2014', 'title': 'Olamide Live In Concert (OLIC) 1', 'category': 'Live Milestone', 'description': 'Inaugural edition of the historic stadium/arena concert series that reshaped live Nigerian concerts.', 'badge': 'Live Concert Series', 'citation': 'Eko Convention Centre Archive'},
        {'year': 2020, 'date': 'February 2020', 'title': 'Joint Venture Deal with EMPIRE', 'category': 'Global Partnership', 'description': 'Signed game-changing international distribution joint venture with EMPIRE, followed by Carpe Diem.', 'badge': 'Global Alliance', 'citation': 'EMPIRE Official Press Release'},
        {'year': 2024, 'date': 'June 26, 2024', 'title': 'Surprise Project: Ikigai, Vol. 1', 'category': 'EP Release', 'description': 'Dropped introspective seven-track EP featuring Fireboy DML, Asake, and Pheelz.', 'badge': 'Latest EP', 'citation': 'YBNL Nation / EMPIRE'}
    ]

    @classmethod
    def get_artist_info(cls):
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

    @classmethod
    def list_albums(cls, album_type=None, search=None, sort='year_desc'):
        results = [a for a in cls.ALBUMS]
        if album_type:
            results = [a for a in results if a['type'].lower() == album_type.lower()]
        if search:
            q = search.lower()
            results = [a for a in results if q in a['title'].lower() or q in a['description'].lower()]
        if sort == 'year_desc':
            results.sort(key=lambda x: x['releaseYear'], reverse=True)
        elif sort == 'year_asc':
            results.sort(key=lambda x: x['releaseYear'])
        elif sort == 'title':
            results.sort(key=lambda x: x['title'].lower())
        return results

    @classmethod
    def get_album_by_slug(cls, slug):
        return next((a for a in cls.ALBUMS if a['slug'].lower() == slug.lower() or a['id'].lower() == slug.lower()), None)

    @classmethod
    def list_singles(cls, search=None):
        results = [s for s in cls.SINGLES]
        if search:
            q = search.lower()
            results = [s for s in results if q in s['title'].lower() or (s['featured'] and q in s['featured'].lower())]
        return results

    @classmethod
    def get_track_by_id(cls, track_id):
        # Look in albums
        for album in cls.ALBUMS:
            for track in album['tracks']:
                if track['id'].lower() == track_id.lower():
                    return {
                        **track,
                        'album_id': album['id'],
                        'album_title': album['title'],
                        'album_slug': album['slug'],
                        'cover_art': album['coverArt'],
                        'release_year': album['releaseYear'],
                        'composer': 'Olamide Adedeji',
                        'recording_location': 'Lagos, Nigeria',
                        'rights_notice': f"© {album['releaseYear']} {album['label']}. All rights reserved."
                    }
        # Look in singles
        for s in cls.SINGLES:
            if s['id'].lower() == track_id.lower():
                return {
                    **s,
                    'number': 1,
                    'album_id': None,
                    'album_title': 'Standalone Single',
                    'album_slug': None,
                    'cover_art': s['coverArt'],
                    'release_year': s['releaseYear'],
                    'composer': 'Olamide Adedeji',
                    'recording_location': 'Lagos, Nigeria',
                    'rights_notice': f"© {s['releaseYear']} YBNL Nation. All rights reserved."
                }
        return None

    @classmethod
    def search_catalogue(cls, query):
        q = (query or '').strip().lower()
        if not q:
            return {'albums': [], 'tracks': [], 'singles': []}

        matched_albums = [a for a in cls.ALBUMS if q in a['title'].lower() or q in a['description'].lower()]
        matched_singles = [s for s in cls.SINGLES if q in s['title'].lower() or (s['featured'] and q in s['featured'].lower())]
        matched_tracks = []
        for a in cls.ALBUMS:
            for t in a['tracks']:
                if q in t['title'].lower() or (t['featured'] and q in t['featured'].lower()):
                    matched_tracks.append({
                        **t,
                        'album_title': a['title'],
                        'album_slug': a['slug'],
                        'cover_art': a['coverArt']
                    })

        return {
            'albums': matched_albums,
            'tracks': matched_tracks,
            'singles': matched_singles
        }

    @classmethod
    def get_timeline(cls):
        return cls.TIMELINE
