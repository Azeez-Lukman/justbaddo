"""
Django management command to seed the PostgreSQL database with verified
Olamide discography, albums, tracks, timeline milestones, and initial community data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile, AccountSettings
from music.models import Artist, Genre, Album, Track, TimelineMilestone
from playlists.models import Playlist, PlaylistTrack
from community.models import Post, Comment
from arena.models import Poll, PollOption, SongBattle, TriviaQuestion
from stories.models import Story
from notifications.models import Notification
from licensing.models import RightsRecord
from moderation.models import Report

class Command(BaseCommand):
    help = 'Seeds verified Olamide discography archive and demo community data into PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # 1. Users & Accounts
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@justbaddo.local', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('AdminPassword123!')
        admin_user.save()

        user1, _ = User.objects.get_or_create(
            username='baddofan99',
            defaults={'email': 'baddofan99@justbaddo.local'}
        )
        user1.set_password('DemoPassword123!')
        user1.save()

        UserProfile.objects.update_or_create(
            user=user1,
            defaults={
                'display_name': 'Tunde Baddo',
                'bio': 'Bariga native, listening since Eni Duro 2010. YBNL for life.',
                'avatar_url': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80',
                'city': 'Bariga, Lagos',
                'favorite_era': 'Carpe Diem (2020)',
                'fan_tier': 'Voice of the Street Ambassador',
                'points': 4850,
                'is_verified': True
            }
        )
        AccountSettings.objects.get_or_create(user=user1)

        user2, _ = User.objects.get_or_create(
            username='kehinde_b',
            defaults={'email': 'kehinde@justbaddo.local'}
        )
        user2.set_password('DemoPassword123!')
        user2.save()
        UserProfile.objects.update_or_create(
            user=user2,
            defaults={
                'display_name': 'Kehinde Balogun',
                'bio': 'Live music enthusiast and concert archivist.',
                'avatar_url': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=150&q=80',
                'city': 'Lagos Island, Nigeria',
                'favorite_era': 'Street OT (2014)',
                'fan_tier': 'OLIC Veteran',
                'points': 6980,
                'is_verified': True
            }
        )

        user3, _ = User.objects.get_or_create(
            username='folake_a',
            defaults={'email': 'folake@justbaddo.local'}
        )
        user3.set_password('DemoPassword123!')
        user3.save()
        UserProfile.objects.update_or_create(
            user=user3,
            defaults={
                'display_name': 'Folake Adeleke',
                'bio': 'Music writer & cultural critic.',
                'avatar_url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80',
                'city': 'Ibadan, Nigeria',
                'favorite_era': 'UY Scuti (2021)',
                'fan_tier': 'Day One Disciple',
                'points': 4210,
                'is_verified': True
            }
        )

        # 2. Artist & Genres
        artist, _ = Artist.objects.update_or_create(
            slug='olamide',
            defaults={
                'name': 'Olamide Adedeji',
                'stage_name': 'Olamide (Baddo / Baddosneh)',
                'origin': 'Bariga, Lagos State, Nigeria',
                'bio': 'Legendary Nigerian rapper, singer, songwriter, and record executive. Founder of YBNL Nation.',
                'image_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=600&q=80'
            }
        )

        genre_names = ['Afrobeats', 'Indigenous Yoruba Hip-Hop', 'Street Rap', 'Afro-fusion', 'Amapiano', 'Dancehall']
        genres = {}
        for g in genre_names:
            slug = g.lower().replace(' ', '-').replace('&', 'and')
            obj, _ = Genre.objects.get_or_create(name=g, defaults={'slug': slug})
            genres[g] = obj

        # 3. Albums & Tracks
        albums_data = [
            {
                'id': 'ikigai-vol-1',
                'title': 'Ikigai / 生き甲斐, Vol. 1',
                'slug': 'ikigai-vol-1',
                'type': 'EP',
                'releaseYear': 2024,
                'releaseDate': 'June 26, 2024',
                'coverArt': 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=600&q=80',
                'label': 'YBNL Nation / EMPIRE',
                'distributor': 'EMPIRE',
                'description': 'A contemplative seven-track sonic journey blending introspective street consciousness with sophisticated Afro-fusion production.',
                'featured_artists_text': 'Fireboy DML, Asake, Pheelz, Young Jonn, Lil Kesh, SABRI',
                'producers_text': 'Semzi, Pheelz, Young Jonn',
                'tracks': [
                    {'id': 'iki-01', 'number': 1, 'title': 'Metaverse', 'duration': '2:47', 'duration_seconds': 167, 'featured': '', 'producer': 'Semzi', 'status': 'JUSTBADDO_STREAMING', 'bpm': 108, 'key': 'F#m'},
                    {'id': 'iki-02', 'number': 2, 'title': 'Uptown Disco', 'duration': '3:12', 'duration_seconds': 192, 'featured': 'Fireboy DML & Asake', 'producer': 'Pheelz', 'status': 'JUSTBADDO_STREAMING', 'bpm': 114, 'key': 'Am'},
                    {'id': 'iki-03', 'number': 3, 'title': 'Makaveli', 'duration': '2:56', 'duration_seconds': 176, 'featured': '', 'producer': 'Semzi', 'status': 'JUSTBADDO_STREAMING', 'bpm': 102, 'key': 'Gm'},
                    {'id': 'iki-04', 'number': 4, 'title': 'Knockout', 'duration': '3:05', 'duration_seconds': 185, 'featured': 'SABRI', 'producer': 'Semzi', 'status': 'AUTHORISED_PROVIDER', 'bpm': 110, 'key': 'Dm'},
                    {'id': 'iki-05', 'number': 5, 'title': 'Hello Habibi', 'duration': '2:38', 'duration_seconds': 158, 'featured': '', 'producer': 'Young Jonn', 'status': 'JUSTBADDO_STREAMING', 'bpm': 116, 'key': 'Em'},
                    {'id': 'iki-06', 'number': 6, 'title': 'Synchro System', 'duration': '3:15', 'duration_seconds': 195, 'featured': 'Pheelz, Young Jonn & Lil Kesh', 'producer': 'Pheelz', 'status': 'JUSTBADDO_STREAMING', 'bpm': 120, 'key': 'C'},
                    {'id': 'iki-07', 'number': 7, 'title': 'Morowore', 'duration': '3:21', 'duration_seconds': 201, 'featured': '', 'producer': 'Semzi', 'status': 'JUSTBADDO_STREAMING', 'bpm': 98, 'key': 'Bm'}
                ]
            },
            {
                'id': 'unruly',
                'title': 'Unruly',
                'slug': 'unruly',
                'type': 'Studio Album',
                'releaseYear': 2023,
                'releaseDate': 'August 4, 2023',
                'coverArt': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80',
                'label': 'YBNL Nation / EMPIRE',
                'distributor': 'EMPIRE',
                'description': 'Celebrated tenth studio album featuring global anthems, amapiano experiments, and heavyweight guest appearances.',
                'featured_artists_text': 'Rema, Asake, Fireboy DML, BNXN, CKay',
                'producers_text': 'Eskeez, Magicsticks, P.Priime',
                'tracks': [
                    {'id': 'unr-01', 'number': 1, 'title': 'Celebrate', 'duration': '2:50', 'duration_seconds': 170, 'featured': '', 'producer': 'Eskeez', 'status': 'JUSTBADDO_STREAMING', 'bpm': 112, 'key': 'C#m'},
                    {'id': 'unr-02', 'number': 2, 'title': 'Gaza', 'duration': '2:40', 'duration_seconds': 160, 'featured': '', 'producer': 'Eskeez', 'status': 'JUSTBADDO_STREAMING', 'bpm': 115, 'key': 'Em'},
                    {'id': 'unr-03', 'number': 3, 'title': 'Doom', 'duration': '3:05', 'duration_seconds': 185, 'featured': '', 'producer': 'Magicsticks', 'status': 'JUSTBADDO_STREAMING', 'bpm': 118, 'key': 'Fm'},
                    {'id': 'unr-04', 'number': 4, 'title': 'Trumpet', 'duration': '3:10', 'duration_seconds': 190, 'featured': 'CKay', 'producer': 'P.Priime', 'status': 'AUTHORISED_PROVIDER', 'bpm': 105, 'key': 'Am'},
                    {'id': 'unr-05', 'number': 5, 'title': 'New Religion', 'duration': '3:12', 'duration_seconds': 192, 'featured': 'Asake', 'producer': 'Magicsticks', 'status': 'JUSTBADDO_STREAMING', 'bpm': 116, 'key': 'Gm'}
                ]
            },
            {
                'id': 'uy-scuti',
                'title': 'UY Scuti',
                'slug': 'uy-scuti',
                'type': 'Studio Album',
                'releaseYear': 2021,
                'releaseDate': 'June 18, 2021',
                'coverArt': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80',
                'label': 'YBNL Nation / EMPIRE',
                'distributor': 'EMPIRE',
                'description': 'A relaxed, sonic departure exploring dancehall, reggae rhythms, and intimate acoustic melodies named after the hypergiant star.',
                'featured_artists_text': 'Fave, Phyno, Jaywillz, Layydoe',
                'producers_text': 'P.Priime, Eskeez',
                'tracks': [
                    {'id': 'uys-01', 'number': 1, 'title': 'Need for Speed', 'duration': '3:01', 'duration_seconds': 181, 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'bpm': 100, 'key': 'F#m'},
                    {'id': 'uys-02', 'number': 2, 'title': 'Jailer', 'duration': '3:04', 'duration_seconds': 184, 'featured': 'Jaywillz', 'producer': 'Eskeez', 'status': 'JUSTBADDO_STREAMING', 'bpm': 104, 'key': 'C'},
                    {'id': 'uys-03', 'number': 3, 'title': 'Rock', 'duration': '3:05', 'duration_seconds': 185, 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'bpm': 102, 'key': 'Am'},
                    {'id': 'uys-04', 'number': 4, 'title': 'Julie', 'duration': '3:10', 'duration_seconds': 190, 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'bpm': 98, 'key': 'Dm'},
                    {'id': 'uys-05', 'number': 5, 'title': 'Rough Up', 'duration': '2:45', 'duration_seconds': 165, 'featured': 'Layydoe', 'producer': 'Eskeez', 'status': 'AUTHORISED_PROVIDER', 'bpm': 106, 'key': 'Em'}
                ]
            },
            {
                'id': 'carpe-diem',
                'title': 'Carpe Diem',
                'slug': 'carpe-diem',
                'type': 'Studio Album',
                'releaseYear': 2020,
                'releaseDate': 'October 8, 2020',
                'coverArt': 'https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=600&q=80',
                'label': 'YBNL Nation / EMPIRE',
                'distributor': 'EMPIRE',
                'description': 'A watershed classic that re-energized modern Afrobeats with "Infinity", "Loading", and "Greenlight".',
                'featured_artists_text': 'Fireboy DML, Bella Shmurda, Bad Boy Timz, Omah Lay, Peruzzi, Phyno',
                'producers_text': 'P.Priime, Pheelz, Vstix, ID Cabasa',
                'tracks': [
                    {'id': 'cpd-01', 'number': 1, 'title': 'Another Level', 'duration': '2:55', 'duration_seconds': 175, 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'bpm': 104, 'key': 'G'},
                    {'id': 'cpd-02', 'number': 2, 'title': 'Green Light', 'duration': '3:15', 'duration_seconds': 195, 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'bpm': 105, 'key': 'Am'},
                    {'id': 'cpd-03', 'number': 3, 'title': 'Infinity', 'duration': '2:52', 'duration_seconds': 172, 'featured': 'Omah Lay', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'bpm': 103, 'key': 'C#m'},
                    {'id': 'cpd-04', 'number': 4, 'title': 'Eru', 'duration': '3:03', 'duration_seconds': 183, 'featured': '', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'bpm': 110, 'key': 'Fm'},
                    {'id': 'cpd-05', 'number': 5, 'title': 'Loading', 'duration': '3:15', 'duration_seconds': 195, 'featured': 'Bad Boy Timz', 'producer': 'P.Priime', 'status': 'JUSTBADDO_STREAMING', 'bpm': 116, 'key': 'Dm'}
                ]
            },
            {
                'id': 'rapsodi',
                'title': 'Rapsodi',
                'slug': 'rapsodi',
                'type': 'Studio Album',
                'releaseYear': 2011,
                'releaseDate': 'March 14, 2011',
                'coverArt': 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=600&q=80',
                'label': 'Coded Tunes / NotJustOk',
                'distributor': 'Coded Tunes',
                'description': 'The iconic debut album that introduced Olamide Adedeji from Bariga to the world. Anchored by the breakout single "Eni Duro".',
                'featured_artists_text': 'Wizkid, ID Cabasa, Reminisce, 9ice, D\'Banj, Lord of Ajasa',
                'producers_text': 'ID Cabasa',
                'tracks': [
                    {'id': 'rap-01', 'number': 1, 'title': 'Eni Duro', 'duration': '4:15', 'duration_seconds': 255, 'featured': '', 'producer': 'ID Cabasa', 'status': 'JUSTBADDO_STREAMING', 'bpm': 98, 'key': 'Am'},
                    {'id': 'rap-02', 'number': 2, 'title': 'Omo To Shan', 'duration': '3:40', 'duration_seconds': 220, 'featured': 'Wizkid', 'producer': 'ID Cabasa', 'status': 'JUSTBADDO_STREAMING', 'bpm': 104, 'key': 'F'},
                    {'id': 'rap-03', 'number': 3, 'title': 'Apa Ti Jona', 'duration': '3:52', 'duration_seconds': 232, 'featured': 'ID Cabasa', 'producer': 'ID Cabasa', 'status': 'AUTHORISED_PROVIDER', 'bpm': 100, 'key': 'Dm'},
                    {'id': 'rap-04', 'number': 4, 'title': 'Legendary Hustlers', 'duration': '4:02', 'duration_seconds': 242, 'featured': 'Reminisce & 9ice', 'producer': 'ID Cabasa', 'status': 'METADATA_ONLY', 'bpm': 94, 'key': 'Em'}
                ]
            }
        ]

        for a_data in albums_data:
            alb, _ = Album.objects.update_or_create(
                slug=a_data['slug'],
                defaults={
                    'title': a_data['title'],
                    'album_type': a_data['type'],
                    'release_year': a_data['releaseYear'],
                    'release_date': a_data['releaseDate'],
                    'cover_art': a_data['coverArt'],
                    'label': a_data['label'],
                    'distributor': a_data['distributor'],
                    'description': a_data['description'],
                    'featured_artists_text': a_data['featured_artists_text'],
                    'producers_text': a_data['producers_text']
                }
            )
            for t_data in a_data['tracks']:
                trk, _ = Track.objects.update_or_create(
                    track_id=t_data['id'],
                    defaults={
                        'album': alb,
                        'title': t_data['title'],
                        'track_number': t_data['number'],
                        'duration': t_data['duration'],
                        'duration_seconds': t_data.get('duration_seconds', 180),
                        'featured': t_data['featured'],
                        'producer': t_data['producer'],
                        'playback_status': t_data['status'],
                        'is_playable': (t_data['status'] in ('JUSTBADDO_STREAMING', 'AUTHORISED_PROVIDER')),
                        'bpm': t_data.get('bpm'),
                        'musical_key': t_data.get('key', ''),
                        'cover_art': a_data['coverArt'],
                        'release_year': a_data['releaseYear']
                    }
                )
                RightsRecord.objects.get_or_create(
                    track=trk,
                    defaults={
                        'rightsholder_label': a_data['label'],
                        'licensing_status': 'permission_requested' if t_data['status'] == 'JUSTBADDO_STREAMING' else 'contact_identified',
                        'territories_allowed': ['GLOBAL'],
                        'allowed_playback_modes': ['web_audio_synth', 'authorised_provider_embed']
                    }
                )

        # 4. Standalone Singles
        singles_data = [
            {'id': 's-01', 'title': 'Motigbana', 'releaseYear': 2018, 'duration': '3:15', 'duration_seconds': 195, 'producer': 'Killertunes', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'coverArt': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80'},
            {'id': 's-02', 'title': 'Pawon', 'releaseYear': 2019, 'duration': '3:20', 'duration_seconds': 200, 'producer': 'Cracker Mallo', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'coverArt': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=400&q=80'},
            {'id': 's-03', 'title': 'Wo!!', 'releaseYear': 2017, 'duration': '3:15', 'duration_seconds': 195, 'producer': 'Young Jonn', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'coverArt': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80'},
            {'id': 's-04', 'title': 'Science Student', 'releaseYear': 2018, 'duration': '3:12', 'duration_seconds': 192, 'producer': 'Young Jonn & BBanks', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'coverArt': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=400&q=80'}
        ]

        for s_data in singles_data:
            s_trk, _ = Track.objects.update_or_create(
                track_id=s_data['id'],
                defaults={
                    'album': None,
                    'title': s_data['title'],
                    'track_number': 1,
                    'duration': s_data['duration'],
                    'duration_seconds': s_data['duration_seconds'],
                    'featured': s_data['featured'],
                    'producer': s_data['producer'],
                    'playback_status': s_data['status'],
                    'is_playable': True,
                    'cover_art': s_data['coverArt'],
                    'release_year': s_data['releaseYear']
                }
            )
            RightsRecord.objects.get_or_create(
                track=s_trk,
                defaults={
                    'rightsholder_label': 'YBNL Nation',
                    'licensing_status': 'contact_identified',
                    'territories_allowed': ['GLOBAL'],
                    'allowed_playback_modes': ['web_audio_synth', 'authorised_provider_embed']
                }
            )

        # 5. Timeline Milestones
        milestones = [
            {'year': 2010, 'date': 'Late 2010', 'title': 'Breakout Anthem: "Eni Duro"', 'category': 'Breakthrough', 'description': 'Burst onto the scene with iconic tongue-twisting delivery recorded with ID Cabasa at Coded Tunes.', 'badge': 'Debut Single', 'citation': 'Coded Tunes Records', 'order': 1},
            {'year': 2011, 'date': 'March 14, 2011', 'title': 'Debut Studio Album: Rapsodi', 'category': 'Studio Album', 'description': 'Solidified his arrival with 16 tracks including "Omo To Shan" featuring Wizkid.', 'badge': 'Studio Album #1', 'citation': 'NotJustOk / Coded Tunes', 'order': 2},
            {'year': 2012, 'date': 'November 12, 2012', 'title': 'YBNL Nation Founded & Album Release', 'category': 'Label Milestone', 'description': 'Launched independent imprint YBNL (Yahoo Boy No Laptop) Nation and dropped sophomore classic YBNL.', 'badge': 'Label Inception', 'citation': 'YBNL Nation Press', 'order': 3},
            {'year': 2014, 'date': 'December 28, 2014', 'title': 'Olamide Live In Concert (OLIC) 1', 'category': 'Live Milestone', 'description': 'Inaugural edition of the historic stadium/arena concert series that reshaped live Nigerian concerts.', 'badge': 'Live Concert Series', 'citation': 'Eko Convention Centre Archive', 'order': 4},
            {'year': 2020, 'date': 'February 2020', 'title': 'Joint Venture Deal with EMPIRE', 'category': 'Global Partnership', 'description': 'Signed game-changing international distribution joint venture with EMPIRE, followed by Carpe Diem.', 'badge': 'Global Alliance', 'citation': 'EMPIRE Official Press Release', 'order': 5},
            {'year': 2024, 'date': 'June 26, 2024', 'title': 'Surprise Project: Ikigai, Vol. 1', 'category': 'EP Release', 'description': 'Dropped introspective seven-track EP featuring Fireboy DML, Asake, and Pheelz.', 'badge': 'Latest EP', 'citation': 'YBNL Nation / EMPIRE', 'order': 6}
        ]
        for m in milestones:
            TimelineMilestone.objects.update_or_create(
                year=m['year'],
                title=m['title'],
                defaults=m
            )

        # 6. Playlists
        pl1, _ = Playlist.objects.update_or_create(
            playlist_id='pl-editorial-01',
            defaults={
                'title': 'Baddo Street Anthems',
                'description': 'The definitive high-octane club & street anthems that rocked Lagos and global stages.',
                'creator': admin_user,
                'is_editorial': True,
                'is_private': False,
                'cover_image': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80'
            }
        )
        for idx, tid in enumerate(['s-03', 's-04', 's-01', 'rap-01']):
            trk = Track.objects.filter(track_id=tid).first()
            if trk:
                PlaylistTrack.objects.get_or_create(playlist=pl1, track=trk, defaults={'order': idx})

        pl2, _ = Playlist.objects.update_or_create(
            playlist_id='pl-user-01',
            defaults={
                'title': 'My Daily Baddo Rotation',
                'description': 'My personal daily commute favorites.',
                'creator': user1,
                'is_editorial': False,
                'is_private': False,
                'cover_image': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80'
            }
        )
        for idx, tid in enumerate(['iki-02', 'cpd-05']):
            trk = Track.objects.filter(track_id=tid).first()
            if trk:
                PlaylistTrack.objects.get_or_create(playlist=pl2, track=trk, defaults={'order': idx})

        # 7. Community Discussions
        post1, _ = Post.objects.update_or_create(
            post_id='post-01',
            defaults={
                'title': "Why 'Carpe Diem' Remains the Most Cohesive Afrobeats Album of 2020",
                'category': 'Discography',
                'content': "Four years later, Carpe Diem still plays from track 1 to 12 with zero skips. What track on this album do you return to most often?",
                'author': user2,
                'likes_count': 142
            }
        )
        Comment.objects.get_or_create(
            comment_id='comm-01',
            defaults={
                'post': post1,
                'author': user1,
                'content': 'Loading with Bad Boy Timz is still played at every wedding reception in Lagos. Phenomenal album.',
                'likes_count': 18
            }
        )
        Comment.objects.get_or_create(
            comment_id='comm-02',
            defaults={
                'post': post1,
                'author': user3,
                'content': 'Infinity changed Omah Lay trajectory completely. The synergy was pure magic.',
                'likes_count': 12
            }
        )

        # 8. Fan Arena: Polls, Battles, Trivia
        poll1, _ = Poll.objects.update_or_create(
            poll_id='poll-01',
            defaults={
                'question': 'Which opening track sets the highest bar across Olamide entire discography?',
                'category': 'Track Discography'
            }
        )
        options_data = [
            ('opt-01', 'Voice of the Street (YBNL, 2012)', 489),
            ('opt-02', 'Prayer for Client (Street OT, 2014)', 312),
            ('opt-03', 'Eyan Mayweather (Eyan Mayweather, 2015)', 560),
            ('opt-04', 'Need for Speed (UY Scuti, 2021)', 214)
        ]
        for opt_id, text, votes in options_data:
            PollOption.objects.update_or_create(
                poll=poll1,
                option_id=opt_id,
                defaults={'text': text, 'votes': votes}
            )

        trk_wo = Track.objects.filter(track_id='s-03').first()
        trk_sci = Track.objects.filter(track_id='s-04').first()
        if trk_wo and trk_sci:
            SongBattle.objects.update_or_create(
                battle_id='battle-01',
                defaults={
                    'title': 'The Supreme 2017–2018 Mainland Dance Anthem',
                    'category': 'High-Energy Dance Anthems',
                    'song_a': trk_wo,
                    'song_b': trk_sci,
                    'song_a_votes': 1420,
                    'song_b_votes': 1290
                }
            )

        trivia_qs = [
            ('q1', 'Which studio album served as Olamide debut release in 2011?', ['YBNL', 'Rapsodi', 'Baddest Guy Ever Liveth', 'Street OT'], 1, 'Rapsodi was released on March 14, 2011 via Coded Tunes/NotJustOk.', 1),
            ('q2', 'Which artist was featured on the iconic breakthrough single "Omo To Shan" (2011)?', ['Davido', 'Wizkid', 'Reminisce', '9ice'], 1, 'Wizkid laid the melodic chorus on Omo To Shan during the Coded Tunes era.', 2),
            ('q3', 'What was the venue for the historic first edition of Olamide Live In Concert (OLIC 1) in 2014?', ['Teslim Balogun Stadium', 'Eko Hotel Convention Centre', 'National Stadium Lagos', 'TBS Lagos'], 1, 'OLIC 1 took place on December 28, 2014 at Eko Convention Centre in Victoria Island.', 3),
            ('q4', 'In which year did Olamide announce the landmark YBNL Nation joint venture with EMPIRE?', ['2018', '2019', '2020', '2021'], 2, 'The historic EMPIRE joint venture was finalized in February 2020.', 4),
            ('q5', 'Which 2024 surprise EP features tracks like "Metaverse", "Uptown Disco", and "Morowore"?', ['999', 'Ikigai, Vol. 1', 'UY Scuti', 'Unruly'], 1, 'Ikigai / 生き甲斐, Vol. 1 was released unexpectedly on June 26, 2024.', 5)
        ]
        for qid, qtext, qopts, qcorrect, qexp, qord in trivia_qs:
            TriviaQuestion.objects.update_or_create(
                question_id=qid,
                defaults={
                    'question': qtext,
                    'options': qopts,
                    'correct_index': qcorrect,
                    'explanation': qexp,
                    'order': qord
                }
            )

        # 9. Stories
        stories_data = [
            {
                'id': 'story-01',
                'title': 'The Night OLIC 1 Shook Eko Hotel: December 2014',
                'author_user': user2,
                'author_name': 'Kehinde Balogun',
                'author_role': 'Live Music Enthusiast',
                'author_avatar': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=150&q=80',
                'read_time': '6 min read',
                'cover_image': 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80',
                'excerpt': 'Before OLIC, Nigerian hip-hop concerts at luxury venues like Eko Hotel were considered high-risk. What happened on December 28, 2014 changed live Nigerian concerts forever.',
                'content': '<p class="mb-4 text-zinc-300 leading-relaxed">In late 2014, the prevailing wisdom in the Nigerian live event circuit was clear: street-hop belonged in open community grounds, while Victoria Island luxury halls were reserved for corporate galas and acoustic showcases.</p>',
                'likes_count': 624,
                'tags': ['OLIC', 'Live Concerts', 'Lagos Culture']
            },
            {
                'id': 'story-02',
                'title': 'How "Eni Duro" Saved My Faith in Indigenous African Rap',
                'author_user': None,
                'author_name': 'Dr. Biodun Ogundipe',
                'author_role': 'Ethnomusicologist',
                'author_avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=150&q=80',
                'read_time': '4 min read',
                'cover_image': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80',
                'excerpt': 'Following the untimely passing of Dagrin in 2010, the future of Yoruba hip-hop hung in balance until a relentless young voice emerged from Bariga.',
                'content': '<p class="mb-4 text-zinc-300 leading-relaxed">The grief that gripped Nigerian youth after April 2010 was palpable. For months, radio airwaves searched for who would carry the baton of street poetry without mimicking western cadences.</p>',
                'likes_count': 418,
                'tags': ['Hip-Hop History', 'Rapsodi', 'Bariga Roots']
            }
        ]
        for s in stories_data:
            Story.objects.update_or_create(
                story_id=s['id'],
                defaults={
                    'title': s['title'],
                    'author_user': s['author_user'],
                    'author_name': s['author_name'],
                    'author_role': s['author_role'],
                    'author_avatar': s['author_avatar'],
                    'read_time': s['read_time'],
                    'cover_image': s['cover_image'],
                    'excerpt': s['excerpt'],
                    'content': s['content'],
                    'likes_count': s['likes_count'],
                    'tags': s['tags'],
                    'status': 'PUBLISHED',
                    'published_at': timezone.now()
                }
            )

        # 10. Notifications
        Notification.objects.get_or_create(
            notification_id='notif-01',
            defaults={
                'recipient': user1,
                'title': 'New Song Battle Live!',
                'message': '"Wo!!" and "Science Student" are locked in a dead heat battle in Fan Arena.',
                'category': 'Arena',
                'is_read': False,
                'action_url': '/pages/fan-arena.html',
                'icon': 'flame'
            }
        )

        # 11. Moderation Report
        Report.objects.get_or_create(
            report_id='rep-001',
            defaults={
                'reporter': user1,
                'target_type': 'POST',
                'target_id': 'post-spam-01',
                'reason': 'SPAM',
                'details': 'External gambling link posted in general fan chat.',
                'status': 'PENDING'
            }
        )

        self.stdout.write(self.style.SUCCESS("PostgreSQL database successfully seeded with verified catalogue & demo data!"))
