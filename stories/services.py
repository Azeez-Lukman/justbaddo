"""
Fan Stories service layer for JustBaddo.
Manages published editorial fan essays and community submissions awaiting review.
"""

import uuid
import datetime

class StoriesService:
    """
    In-memory stories repository for Phase 2.
    """

    _stories = [
        {
            'id': 'story-01',
            'title': 'The Night OLIC 1 Shook Eko Hotel: December 2014',
            'author': 'Kehinde Balogun',
            'author_role': 'Live Music Enthusiast',
            'author_avatar': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=150&q=80',
            'date': 'August 14, 2023',
            'read_time': '6 min read',
            'cover_image': 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80',
            'excerpt': 'Before OLIC, Nigerian hip-hop concerts at luxury venues like Eko Hotel were considered high-risk. What happened on December 28, 2014 changed live Nigerian concerts forever.',
            'content': (
                '<p class="mb-4 text-zinc-300 leading-relaxed">In late 2014, the prevailing wisdom in the Nigerian live event circuit was clear: street-hop belonged in open community grounds, while Victoria Island luxury halls were reserved for corporate galas and acoustic showcases.</p>'
                '<p class="mb-4 text-zinc-300 leading-relaxed">Olamide and YBNL shattered that consensus into pieces. By 9 PM on December 28, the traffic on Ozumba Mbadiwe stretched back into Victoria Island. Thousands of mainland youths dressed in signature black and snapbacks stood shoulder-to-shoulder with corporate executives.</p>'
                '<p class="mb-4 text-zinc-300 leading-relaxed">When the horns of "Story For The Gods" dropped, the vibration was so intense that the hall security barricades gave way. It wasn’t a riot; it was an ecstatic coronation.</p>'
            ),
            'likes': 624,
            'tags': ['OLIC', 'Live Concerts', 'Lagos Culture'],
            'status': 'PUBLISHED'
        },
        {
            'id': 'story-02',
            'title': 'How "Eni Duro" Saved My Faith in Indigenous African Rap',
            'author': 'Dr. Biodun Ogundipe',
            'author_role': 'Ethnomusicologist',
            'author_avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=150&q=80',
            'date': 'November 2, 2023',
            'read_time': '4 min read',
            'cover_image': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80',
            'excerpt': 'Following the untimely passing of Dagrin in 2010, the future of Yoruba hip-hop hung in balance until a relentless young voice emerged from Bariga.',
            'content': (
                '<p class="mb-4 text-zinc-300 leading-relaxed">The grief that gripped Nigerian youth after April 2010 was palpable. For months, radio airwaves searched for who would carry the baton of street poetry without mimicking western cadences.</p>'
                '<p class="mb-4 text-zinc-300 leading-relaxed">When "Eni Duro" hit terrestrial television with its gritty one-take video, something shifted. Olamide brought a distinct, aggressive rhythm that wasn\'t an imitation; it was an authentic translation of Lagos street survival.</p>'
            ),
            'likes': 418,
            'tags': ['Hip-Hop History', 'Rapsodi', 'Bariga Roots'],
            'status': 'PUBLISHED'
        },
        {
            'id': 'story-03',
            'title': 'The YBNL A&R Golden Touch: Mentorship as a Movement',
            'author': 'Zainab Bello',
            'author_role': 'Music Industry A&R',
            'author_avatar': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80',
            'date': 'January 18, 2024',
            'read_time': '5 min read',
            'cover_image': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80',
            'excerpt': 'Beyond his own discography, Olamide will go down in African music history as one of the most generous and prolific talent discoverers of modern times.',
            'content': (
                '<p class="mb-4 text-zinc-300 leading-relaxed">Consider the roster that has passed through or blossomed directly under the YBNL umbrella: Adekunle Gold, Lil Kesh, Viktoh, Chinko Ekun, Pheelz, Young Jonn, Fireboy DML, and Asake.</p>'
                '<p class="mb-4 text-zinc-300 leading-relaxed">Unlike traditional record executives who bind artists in restrictive multi-album deals, Olamide pioneered an incubation approach: give artists creative freedom, provide production infrastructure, let them flourish, and celebrate their independent flight.</p>'
            ),
            'likes': 529,
            'tags': ['YBNL Nation', 'Mentorship', 'Industry Impact'],
            'status': 'PUBLISHED'
        }
    ]

    @classmethod
    def list_stories(cls, status_filter='PUBLISHED'):
        if status_filter:
            return [s for s in cls._stories if s['status'] == status_filter]
        return cls._stories

    @classmethod
    def get_story_by_id(cls, story_id):
        return next((s for s in cls._stories if s['id'] == story_id), None)

    @classmethod
    def submit_story(cls, title, content, author_name, author_role, author_avatar, read_time='5 min read', cover_image=None, tags=''):
        tag_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else ['Fan Reflection']
        story_id = f"story-{uuid.uuid4().hex[:6]}"
        excerpt = content[:200] + ('...' if len(content) > 200 else '')

        new_story = {
            'id': story_id,
            'title': title,
            'author': author_name,
            'author_role': author_role or 'Community Fan',
            'author_avatar': author_avatar or 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
            'date': datetime.date.today().strftime('%B %d, %Y'),
            'read_time': read_time,
            'cover_image': cover_image or 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80',
            'excerpt': excerpt,
            'content': f"<p class='text-zinc-300 leading-relaxed'>{content}</p>",
            'likes': 0,
            'tags': tag_list,
            'status': 'PENDING_REVIEW'
        }
        cls._stories.append(new_story)
        return new_story

    @classmethod
    def publish_story(cls, story_id):
        story = cls.get_story_by_id(story_id)
        if story:
            story['status'] = 'PUBLISHED'
            return True, "Story published."
        return False, "Story not found."
