"""
Django management command to seed the PostgreSQL database with verified
Olamide discography, albums, tracks, timeline milestones, and initial community data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile, AccountSettings, Badge, BadgeAward, ReputationEvent
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
                'country': 'Nigeria',
                'favorite_era': 'Carpe Diem (2020)',
                'favorite_album': 'Time and Space (2026)',
                'favorite_track': 'Jaiye (feat. FOLA)',
                'fan_tier': 'Voice of the Street Ambassador',
                'points': 4850,
                'reputation_score': 1850,
                'is_profile_public': True,
                'accepted_community_guidelines': True,
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
                'country': 'Nigeria',
                'favorite_era': 'Street OT (2014)',
                'favorite_album': 'Time and Space (2026)',
                'favorite_track': 'Say Less',
                'fan_tier': 'OLIC Veteran',
                'points': 6980,
                'reputation_score': 2400,
                'is_profile_public': True,
                'accepted_community_guidelines': True,
                'is_verified': True
            }
        )
        AccountSettings.objects.get_or_create(user=user2)

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
                'country': 'Nigeria',
                'favorite_era': 'UY Scuti (2021)',
                'favorite_album': 'Time and Space (2026)',
                'favorite_track': 'Elohim',
                'fan_tier': 'Day One Disciple',
                'points': 4210,
                'reputation_score': 1620,
                'is_profile_public': True,
                'accepted_community_guidelines': True,
                'is_verified': True
            }
        )
        AccountSettings.objects.get_or_create(user=user3)

        # 1.1 Badges & Reputation
        badges_definitions = [
            {
                'badge_id': 'badge-first-steps',
                'name': 'First Steps',
                'slug': 'first-steps',
                'description': 'Joined the JustBaddo fan community and completed registration.',
                'icon': 'compass',
                'category': 'community',
                'points_required': 100,
                'criteria_description': 'Successfully create and verify a JustBaddo member account.'
            },
            {
                'badge_id': 'badge-conversation-starter',
                'name': 'Conversation Starter',
                'slug': 'conversation-starter',
                'description': 'Sparked dialogue by creating your first community discussion topic.',
                'icon': 'message-square',
                'category': 'community',
                'points_required': 250,
                'criteria_description': 'Publish an original discussion topic in the community forum.'
            },
            {
                'badge_id': 'badge-good-contributor',
                'name': 'Good Contributor',
                'slug': 'good-contributor',
                'description': 'Recognised by fellow fans for helpful and insightful contributions.',
                'icon': 'thumbs-up',
                'category': 'community',
                'points_required': 500,
                'criteria_description': 'Receive 10 or more helpful reactions across community posts and comments.'
            },
            {
                'badge_id': 'badge-album-explorer',
                'name': 'Album Explorer',
                'slug': 'album-explorer',
                'description': 'Listened to complete discography projects including Time and Space.',
                'icon': 'disc',
                'category': 'music',
                'points_required': 750,
                'criteria_description': 'Explore tracks across 3 or more full album eras.'
            },
            {
                'badge_id': 'badge-community-regular',
                'name': 'Community Regular',
                'slug': 'community-regular',
                'description': 'Maintained a strong reputation for active, respectful participation.',
                'icon': 'flame',
                'category': 'reputation',
                'points_required': 1000,
                'criteria_description': 'Accumulate 1,000+ reputation points through positive participation.'
            }
        ]

        badges_dict = {}
        for b_data in badges_definitions:
            b_obj, _ = Badge.objects.update_or_create(
                slug=b_data['slug'],
                defaults=b_data
            )
            badges_dict[b_data['slug']] = b_obj

        # Assign awards idempotently
        BadgeAward.objects.get_or_create(badge=badges_dict['first-steps'], user=user1, defaults={'reason': 'Initial account verification'})
        BadgeAward.objects.get_or_create(badge=badges_dict['conversation-starter'], user=user1, defaults={'reason': 'Created first discography discussion'})
        BadgeAward.objects.get_or_create(badge=badges_dict['good-contributor'], user=user1, defaults={'reason': 'Earned 10+ helpful community replies'})
        BadgeAward.objects.get_or_create(badge=badges_dict['album-explorer'], user=user1, defaults={'reason': 'Explored Time and Space'})
        BadgeAward.objects.get_or_create(badge=badges_dict['community-regular'], user=user1, defaults={'reason': 'Active daily participation streak'})

        BadgeAward.objects.get_or_create(badge=badges_dict['first-steps'], user=user2, defaults={'reason': 'Account created'})
        BadgeAward.objects.get_or_create(badge=badges_dict['album-explorer'], user=user2, defaults={'reason': 'Archived OLIC live sets'})
        BadgeAward.objects.get_or_create(badge=badges_dict['community-regular'], user=user2, defaults={'reason': 'Consistent community moderation compliance'})

        BadgeAward.objects.get_or_create(badge=badges_dict['first-steps'], user=user3, defaults={'reason': 'Account created'})
        BadgeAward.objects.get_or_create(badge=badges_dict['good-contributor'], user=user3, defaults={'reason': 'Published insightful cultural review'})

        # Record Initial Reputation Events
        ReputationEvent.objects.get_or_create(
            user=user1,
            event_type='POST_PUBLISHED',
            source_type='post',
            source_id='post-01',
            defaults={'points_delta': 25, 'reason': 'Published initial high-value discussion'}
        )
        ReputationEvent.objects.get_or_create(
            user=user1,
            event_type='REACTION_RECEIVED',
            source_type='post',
            source_id='post-01',
            defaults={'points_delta': 10, 'reason': 'Received positive reactions from community members'}
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
                'id': 'time-and-space',
                'title': 'Time and Space',
                'slug': 'time-and-space',
                'type': 'Studio Album',
                'releaseYear': 2026,
                'releaseDate': 'November 16, 2026',
                'coverArt': '/static/images/albums/time-and-space.svg',
                'label': 'YBNL Nation / EMPIRE',
                'distributor': 'EMPIRE',
                'description': 'Eleventh studio album by Olamide. A cohesive ten-track sonic masterpiece traversing legacy, freedom, and Afrobeats evolution, featuring rising talent FOLA on the standout moment "Jaiye".',
                'featured_artists_text': 'FOLA',
                'producers_text': 'P.Priime, Eskeez, Magicsticks, Pheelz, Semzi',
                'tracks': [
                    {'id': 'ts-01', 'number': 1, 'title': 'Elohim', 'duration': '2:45', 'duration_seconds': 165, 'featured': '', 'producer': 'P.Priime', 'status': 'AUTHORISED_PROVIDER', 'bpm': 106, 'key': 'C#m'},
                    {'id': 'ts-02', 'number': 2, 'title': 'Skoskola', 'duration': '2:52', 'duration_seconds': 172, 'featured': '', 'producer': 'Eskeez', 'status': 'AUTHORISED_PROVIDER', 'bpm': 114, 'key': 'F#m'},
                    {'id': 'ts-03', 'number': 3, 'title': 'Say Less', 'duration': '3:08', 'duration_seconds': 188, 'featured': '', 'producer': 'Magicsticks', 'status': 'AUTHORISED_PROVIDER', 'bpm': 112, 'key': 'Am'},
                    {'id': 'ts-04', 'number': 4, 'title': 'Burukutu', 'duration': '2:39', 'duration_seconds': 159, 'featured': '', 'producer': 'Semzi', 'status': 'AUTHORISED_PROVIDER', 'bpm': 118, 'key': 'Gm'},
                    {'id': 'ts-05', 'number': 5, 'title': 'Alujon', 'duration': '3:14', 'duration_seconds': 194, 'featured': '', 'producer': 'P.Priime', 'status': 'AUTHORISED_PROVIDER', 'bpm': 108, 'key': 'Dm'},
                    {'id': 'ts-06', 'number': 6, 'title': 'Mbiri', 'duration': '2:48', 'duration_seconds': 168, 'featured': '', 'producer': 'Eskeez', 'status': 'AUTHORISED_PROVIDER', 'bpm': 110, 'key': 'Em'},
                    {'id': 'ts-07', 'number': 7, 'title': 'Jaiye', 'duration': '3:22', 'duration_seconds': 202, 'featured': 'FOLA', 'producer': 'Pheelz', 'status': 'AUTHORISED_PROVIDER', 'bpm': 115, 'key': 'Bm'},
                    {'id': 'ts-08', 'number': 8, 'title': 'Oshey', 'duration': '2:55', 'duration_seconds': 175, 'featured': '', 'producer': 'Magicsticks', 'status': 'AUTHORISED_PROVIDER', 'bpm': 112, 'key': 'C'},
                    {'id': 'ts-09', 'number': 9, 'title': 'Ring', 'duration': '3:02', 'duration_seconds': 182, 'featured': '', 'producer': 'Semzi', 'status': 'AUTHORISED_PROVIDER', 'bpm': 104, 'key': 'F'},
                    {'id': 'ts-10', 'number': 10, 'title': 'Jogor', 'duration': '2:40', 'duration_seconds': 160, 'featured': '', 'producer': 'Eskeez', 'status': 'AUTHORISED_PROVIDER', 'bpm': 120, 'key': 'Am'}
                ]
            },
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
                'coverArt': '/static/images/albums/rapsodi.svg',
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
                prov_name = 'soundcloud' if t_data['status'] == 'AUTHORISED_PROVIDER' else 'web_audio_synth'
                prov_id = f"sc-{t_data['id']}" if prov_name == 'soundcloud' else t_data['id']
                trk, _ = Track.objects.update_or_create(
                    track_id=t_data['id'],
                    defaults={
                        'album': alb,
                        'artist': artist,
                        'title': t_data['title'],
                        'track_number': t_data['number'],
                        'duration': t_data['duration'],
                        'duration_seconds': t_data.get('duration_seconds', 180),
                        'featured': t_data['featured'],
                        'producer': t_data['producer'],
                        'playback_status': t_data['status'],
                        'provider_name': prov_name,
                        'provider_track_id': prov_id,
                        'availability_territories': ['NG', 'GH', 'GB', 'US', 'WORLD'],
                        'is_playable': (t_data['status'] in ('JUSTBADDO_STREAMING', 'AUTHORISED_PROVIDER')),
                        'bpm': t_data.get('bpm'),
                        'musical_key': t_data.get('key', ''),
                        'cover_art': a_data['coverArt'],
                        'release_year': a_data['releaseYear']
                    }
                )
                RightsRecord.objects.update_or_create(
                    track=trk,
                    defaults={
                        'rightsholder_label': a_data['label'],
                        'licensing_status': 'licensed' if t_data['status'] == 'JUSTBADDO_STREAMING' else 'contact_identified',
                        'master_rights_cleared': (t_data['status'] == 'JUSTBADDO_STREAMING'),
                        'composition_rights_cleared': (t_data['status'] == 'JUSTBADDO_STREAMING'),
                        'playback_authorized': (t_data['status'] in ('JUSTBADDO_STREAMING', 'AUTHORISED_PROVIDER')),
                        'territories_allowed': ['WORLD', 'NG', 'GH', 'GB', 'US'],
                        'allowed_playback_modes': ['web_audio_synth', 'authorised_provider_embed', 'soundcloud']
                    }
                )

        # 4. Standalone Singles
        singles_data = [
            {'id': 's-01', 'title': 'Motigbana', 'releaseYear': 2018, 'duration': '3:15', 'duration_seconds': 195, 'producer': 'Killertunes', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'provider': 'youtube', 'provider_id': 'm7_J3P5k9ZQ', 'coverArt': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80'},
            {'id': 's-02', 'title': 'Pawon', 'releaseYear': 2019, 'duration': '3:20', 'duration_seconds': 200, 'producer': 'Cracker Mallo', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'provider': 'soundcloud', 'provider_id': 'sc-pawon-olamide', 'coverArt': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=400&q=80'},
            {'id': 's-03', 'title': 'Wo!!', 'releaseYear': 2017, 'duration': '3:15', 'duration_seconds': 195, 'producer': 'Young Jonn', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'provider': 'web_audio_synth', 'provider_id': 's-03', 'coverArt': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80'},
            {'id': 's-04', 'title': 'Science Student', 'releaseYear': 2018, 'duration': '3:12', 'duration_seconds': 192, 'producer': 'Young Jonn & BBanks', 'featured': '', 'status': 'JUSTBADDO_STREAMING', 'provider': 'youtube', 'provider_id': 'dQw4w9WgXcQ', 'coverArt': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=400&q=80'}
        ]

        for s_data in singles_data:
            s_trk, _ = Track.objects.update_or_create(
                track_id=s_data['id'],
                defaults={
                    'album': None,
                    'artist': artist,
                    'title': s_data['title'],
                    'track_number': 1,
                    'duration': s_data['duration'],
                    'duration_seconds': s_data['duration_seconds'],
                    'featured': s_data['featured'],
                    'producer': s_data['producer'],
                    'playback_status': s_data['status'],
                    'provider_name': s_data.get('provider', 'web_audio_synth'),
                    'provider_track_id': s_data.get('provider_id', s_data['id']),
                    'availability_territories': ['NG', 'GH', 'GB', 'US', 'WORLD'],
                    'is_playable': True,
                    'cover_art': s_data['coverArt'],
                    'release_year': s_data['releaseYear']
                }
            )
            RightsRecord.objects.update_or_create(
                track=s_trk,
                defaults={
                    'rightsholder_label': 'YBNL Nation',
                    'licensing_status': 'licensed',
                    'master_rights_cleared': True,
                    'composition_rights_cleared': True,
                    'playback_authorized': True,
                    'territories_allowed': ['WORLD', 'NG', 'GH', 'GB', 'US'],
                    'allowed_playback_modes': ['web_audio_synth', 'authorised_provider_embed', 'youtube', 'soundcloud']
                }
            )

        # 5. Timeline Milestones (Complete 16-Year Chronology from 2010 to 2026)
        milestones = [
            {'year': 2010, 'date': 'Late 2010', 'title': 'Breakout Anthem: "Eni Duro"', 'category': 'Breakthrough', 'description': 'Signed to ID Cabasa\'s Coded Tunes imprint, Olamide Adedeji released "Eni Duro", accompanied by a high-energy video directed by DJ Tee. The song became an immediate street phenomenon.', 'badge': 'Debut Single', 'citation': 'Coded Tunes Records / Hip Hop World Magazine', 'order': 1},
            {'year': 2011, 'date': 'March 14, 2011', 'title': 'Debut Studio Album: "Rapsodi"', 'category': 'Studio Album', 'description': 'Released debut LP featuring 16 tracks including "Omo To Shan" featuring Wizkid, "Apa Ti Jona", and "Legendary Hustlers", earning a Next Rated nomination at The Headies 2011.', 'badge': 'Studio Album #1', 'citation': 'The Headies / NotJustOk Archives', 'order': 2},
            {'year': 2012, 'date': 'November 12, 2012', 'title': 'YBNL Nation Founded & Sophomore Album', 'category': 'Label Milestone', 'description': 'Launched independent imprint YBNL (Yahoo Boy No Laptop) Nation and dropped sophomore classic YBNL, spawning party records like "First of All", "Stupid Love", and "Voice of the Street".', 'badge': 'Label Inception', 'citation': 'YBNL Nation / Vanguard Nigeria', 'order': 3},
            {'year': 2013, 'date': 'November 7, 2013', 'title': 'Third Studio Album: "Baddest Guy Ever Liveth" (BGEL)', 'category': 'Studio Album', 'description': 'Solidified his hip-hop supremacy with BGEL, containing "Durosoke", "Turn Up", and "Yemi My Lover". The album swept major accolades at The Headies 2014 including Album of the Year.', 'badge': 'Studio Album #3', 'citation': 'The Headies 2014 Awards Record', 'order': 4},
            {'year': 2014, 'date': 'November 14, 2014', 'title': '"Street OT" & The Launch of OLIC', 'category': 'Concert & Album', 'description': 'Released Street OT featuring "Story For The Gods" and "Goons Mi". In December 2014, launched Olamide Live In Concert (OLIC) at Eko Convention Centre, pioneering annual arena shows for Nigerian rappers.', 'badge': 'Live Concert Series', 'citation': 'Eko Hotels / Premium Times', 'order': 5},
            {'year': 2015, 'date': 'November 23, 2015', 'title': '"2 Kings" Collaboration & "Eyan Mayweather"', 'category': 'Studio Album', 'description': 'Joined forces with Phyno for collaborative LP 2 Kings in April, then dropped Eyan Mayweather in November, a 21-track solo masterpiece featuring zero guest artists and the national dance craze "Bobo".', 'badge': 'Studio Album #5', 'citation': 'YBNL / Penthauze / Pulse Nigeria', 'order': 6},
            {'year': 2016, 'date': 'December 26, 2016', 'title': 'Return to Hardcore Rap: "The Glory"', 'category': 'Studio Album', 'description': 'Released on Boxing Day alongside OLIC 3, The Glory showcased pure hip-hop lyricism with records like "The Glory Intro", "Letter to Milli" and "Pepper Dem Gang", reaffirming his technical rapping roots.', 'badge': 'Studio Album #6', 'citation': 'The Guardian Life / YBNL', 'order': 7},
            {'year': 2017, 'date': 'November 17, 2017', 'title': '"Lagos Nawa" & The Viral "Wo!!" Phenomenon', 'category': 'Studio Album', 'description': 'Recorded Lagos Nawa in a reported 48-hour studio session with Young Jonn. Lead street single "Wo!!" spurred a global viral dance challenge and became the most searched Nigerian song of 2017 on Google.', 'badge': 'Studio Album #7', 'citation': 'Google Year in Search 2017 / Channels TV', 'order': 8},
            {'year': 2018, 'date': 'August 2018', 'title': 'Incubation Era: Mentorship & "Motigbana"', 'category': 'YBNL Expansion', 'description': 'Announced the signing of Fireboy DML. Meanwhile, Olamide continued his run with standalone smash singles including "Science Student", "Motigbana", "Poverty Die", and the YBNL Mafia Family compilation.', 'badge': 'Label Roster', 'citation': 'Native Mag / YBNL Nation', 'order': 9},
            {'year': 2020, 'date': 'February 2020', 'title': 'Global Joint Venture with EMPIRE & "Carpe Diem"', 'category': 'Global Partnership', 'description': 'Signed a landmark international joint venture distribution deal with EMPIRE for YBNL Nation. In October 2020, released Carpe Diem, producing global hits "Infinity" (feat. Omah Lay) and "Loading".', 'badge': 'Global Alliance', 'citation': 'Billboard / EMPIRE Press Release', 'order': 10},
            {'year': 2021, 'date': 'June 18, 2021', 'title': 'Sonic Evolution: "UY Scuti"', 'category': 'Studio Album', 'description': 'Named after the celestial supergiant star, UY Scuti explored acoustic, dancehall and mellow Afrobeats tempos, led by the beloved international single "Rock", charting in over 30 countries.', 'badge': 'Studio Album #9', 'citation': 'Pitchfork / Rolling Stone', 'order': 11},
            {'year': 2022, 'date': 'February 2022', 'title': 'The Breakthrough of Asake', 'category': 'Label Milestone', 'description': 'Signed Asake to YBNL Nation and co-executive produced his debut EP and record-breaking studio album "Mr. Money With The Vibe", cementing YBNL\'s status as Africa\'s preeminent star-building factory.', 'badge': 'Label Executive', 'citation': 'The New York Times / Billboard', 'order': 12},
            {'year': 2023, 'date': 'August 9, 2023', 'title': 'Tenth Studio Album: "Unruly"', 'category': 'Studio Album', 'description': 'Unveiled Unruly, his tenth solo studio project, featuring collaborations with CKay, Asake, Fireboy DML, BNXN, and Rema, garnering critical acclaim across global platforms.', 'badge': 'Studio Album #10', 'citation': 'OkayAfrica / EMPIRE', 'order': 13},
            {'year': 2024, 'date': 'June 26, 2024', 'title': 'Cultural Stewardship: "Ikigai / 生き甲斐, Vol. 1"', 'category': 'EP Release', 'description': 'Released the acclaimed 7-track EP Ikigai, featuring "Metaverse", "Uptown Disco" with Fireboy DML & Asake, and "Hello Habibi", reaffirming his creative longevity and cultural stewardship.', 'badge': 'Latest EP', 'citation': 'The Native / YBNL / EMPIRE', 'order': 14},
            {'year': 2026, 'date': 'November 16, 2026', 'title': 'Eleventh Studio Album: "Time and Space"', 'category': 'Studio Album', 'description': 'Released his landmark eleventh studio album, Time and Space, via YBNL Nation and EMPIRE. Featuring 10 tracks including "Elohim", "Skoskola", "Say Less", "Burukutu", "Alujon", and "Jaiye" (featuring FOLA), inaugurating a transcendent new era in Afrobeats history.', 'badge': 'Studio Album #11', 'citation': 'YBNL Nation / EMPIRE Official Release', 'order': 15}
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
        post_ts, _ = Post.objects.update_or_create(
            post_id='post-time-and-space',
            defaults={
                'title': "Ten Tracks, One Guest: Inside Olamide's 'Time and Space' Masterpiece",
                'category': 'Discography',
                'content': "Released on November 16, 2026, 'Time and Space' marks Olamide's eleventh studio project. Featuring rising artist FOLA on the spellbinding track 'Jaiye', the album strips back excess to deliver ten immaculate tracks. What are your first impressions?",
                'author': user3,
                'likes_count': 215
            }
        )
        Comment.objects.get_or_create(
            comment_id='comm-ts-01',
            defaults={
                'post': post_ts,
                'author': user1,
                'content': 'Jaiye with FOLA is an instant modern classic. Pheelz production on that track is out of this world.',
                'likes_count': 42
            }
        )
        Comment.objects.get_or_create(
            comment_id='comm-ts-02',
            defaults={
                'post': post_ts,
                'author': user2,
                'content': 'Elohim opening the album sets the spiritual tone right away, and Jogor closes it on high energy.',
                'likes_count': 29
            }
        )

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
        poll_ts, _ = Poll.objects.update_or_create(
            poll_id='poll-time-and-space',
            defaults={
                'question': 'Which track defines Olamide\'s eleventh studio album "Time and Space"?',
                'category': 'Album Highlights'
            }
        )
        ts_poll_options = [
            ('opt-ts-01', 'Elohim', 620),
            ('opt-ts-02', 'Jaiye (feat. FOLA)', 1240),
            ('opt-ts-03', 'Say Less', 415),
            ('opt-ts-04', 'Jogor', 530)
        ]
        for opt_id, text, votes in ts_poll_options:
            PollOption.objects.update_or_create(
                poll=poll_ts,
                option_id=opt_id,
                defaults={'text': text, 'votes': votes}
            )

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
            ('q5', 'Which 2024 surprise EP features tracks like "Metaverse", "Uptown Disco", and "Morowore"?', ['999', 'Ikigai, Vol. 1', 'UY Scuti', 'Unruly'], 1, 'Ikigai / 生き甲斐, Vol. 1 was released unexpectedly on June 26, 2024.', 5),
            ('q6', 'On Olamide\'s 2026 album "Time and Space", which rising artist is the sole featured guest on "Jaiye"?', ['Asake', 'FOLA', 'Fireboy DML', 'CKay'], 1, 'FOLA is the sole featured guest artist on Time and Space, appearing on track 7 "Jaiye".', 6)
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
                'id': 'story-time-and-space',
                'title': 'Time and Space: Olamide Opens a New Chapter',
                'author_user': user3,
                'author_name': 'Folake Adeleke',
                'author_role': 'Music Critic & Essayist',
                'author_avatar': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80',
                'read_time': '5 min read',
                'cover_image': '/static/images/albums/time-and-space.svg',
                'excerpt': 'With ten tracks and only one featured artist (FOLA on "Jaiye"), Time and Space represents Olamide at his most confident, self-contained, and forward-looking.',
                'content': '<p class="mb-4 text-zinc-300 leading-relaxed">Released in November 2026 through YBNL Nation and EMPIRE, Time and Space is a testament to longevity in African popular music. Rejecting bloated tracklists and chasing ephemeral algorithm trends, Olamide crafted a concise, cohesive body of work with ten immaculate tracks.</p><p class="mb-4 text-zinc-300 leading-relaxed">The sole collaboration on the album — "Jaiye" featuring breakout talent FOLA — stands as a brilliant moment of sonic chemistry, proving once again Baddo instinct for lifting authentic voices.</p>',
                'likes_count': 512,
                'tags': ['Time and Space', 'Album Review', 'YBNL', 'New Music']
            },
            {
                'id': 'story-01',
                'title': 'The Night OLIC 1 Shook Eko Hotel: December 2014',
                'author_user': user2,
                'author_name': 'Kehinde Balogun',
                'author_role': 'Live Music Enthusiast',
                'author_avatar': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=150&q=80',
                'read_time': '6 min read',
                'cover_image': '/static/images/stories/olic-story.svg',
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
                'cover_image': '/static/images/stories/eni-duro-story.svg',
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
