"""
Community service layer for JustBaddo.
Manages discussion topics, threaded comments, reactions, and category feeds.
"""

import uuid
import datetime

class CommunityService:
    """
    In-memory community repository for Phase 2.
    """

    _posts = [
        {
            'id': 'post-01',
            'title': "Why 'Carpe Diem' Remains the Most Cohesive Afrobeats Album of 2020",
            'category': 'Discography',
            'content': (
                "Four years later, Carpe Diem still plays from track 1 to 12 with zero skips. "
                "The sonic pivot engineered by P.Priime, Pheelz, and Vstix marked a complete evolution in Olamide vocal style. "
                "Instead of loud aggression, he leaned into subtle melodies and acoustic warmth without losing street credibility. "
                "What track on this album do you return to most often?"
            ),
            'author': 'Kehinde Balogun',
            'author_username': 'kehinde_b',
            'avatar': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=150&q=80',
            'timestamp': '2 hours ago',
            'likes': 142,
            'liked_by': set(),
            'comments': [
                {
                    'id': 'comm-01',
                    'author': 'Tunde Baddo',
                    'author_username': 'baddofan99',
                    'avatar': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
                    'content': 'Loading with Bad Boy Timz is still played at every wedding reception in Lagos. Phenomenal album.',
                    'timestamp': '1 hour ago',
                    'likes': 18
                },
                {
                    'id': 'comm-02',
                    'author': 'Folake Adeleke',
                    'author_username': 'folake_a',
                    'avatar': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80',
                    'content': 'Infinity changed Omah Lay trajectory completely. The synergy was pure magic.',
                    'timestamp': '45 minutes ago',
                    'likes': 12
                }
            ]
        },
        {
            'id': 'post-02',
            'title': "Deciphering the Bariga Metaphors in 'Voice of the Street' (2012)",
            'category': 'Lyrics & Meaning',
            'content': (
                "Let's break down the lyrical depth in Voice of the Street. "
                "When Baddo raps 'Ta l’on so pe a o ni se aseyori...', it wasn't just a rap hook — "
                "it was an unyielding manifesto for disenfranchised youths navigating mainland Lagos hustles. "
                "The sheer hunger in that vocal take remains unmatched in indigenous rap history."
            ),
            'author': 'Dr. Biodun Ogundipe',
            'author_username': 'biodun_og',
            'avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=150&q=80',
            'timestamp': '5 hours ago',
            'likes': 289,
            'liked_by': set(),
            'comments': [
                {
                    'id': 'comm-03',
                    'author': 'Segun Alabi',
                    'author_username': 'segun_a',
                    'avatar': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80',
                    'content': 'Produced by Tyrone. That beat had that raw brass sample that shook every speaker on the mainland.',
                    'timestamp': '3 hours ago',
                    'likes': 34
                }
            ]
        },
        {
            'id': 'post-03',
            'title': "OLIC 1 (2014) vs OLIC 4 (2017 at Teslim Balogun): Which Was More Iconic?",
            'category': 'Concerts & OLIC',
            'content': (
                "Moving OLIC from the luxury indoor halls of Eko Hotel to the open-air Teslim Balogun Stadium in Surulere "
                "was one of the boldest moves in African live music history. Over 25,000 fans packed the stadium from afternoon till dawn. "
                "Which edition was your favorite live memory?"
            ),
            'author': 'Zainab Bello',
            'author_username': 'zainab_b',
            'avatar': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80',
            'timestamp': '1 day ago',
            'likes': 378,
            'liked_by': set(),
            'comments': []
        }
    ]

    @classmethod
    def list_posts(cls, category=None, search=None, username='baddofan99'):
        results = cls._posts
        if category and category.lower() != 'all':
            results = [p for p in results if p['category'].lower() == category.lower()]
        if search:
            q = search.lower()
            results = [p for p in results if q in p['title'].lower() or q in p['content'].lower()]

        return [
            {
                'id': p['id'],
                'title': p['title'],
                'content': p['content'],
                'author': p['author'],
                'author_username': p['author_username'],
                'avatar': p['avatar'],
                'category': p['category'],
                'timestamp': p['timestamp'],
                'likes': p['likes'],
                'comments_count': len(p['comments']),
                'has_liked': username in p.get('liked_by', set())
            }
            for p in results
        ]

    @classmethod
    def get_post_detail(cls, post_id, username='baddofan99'):
        p = next((post for post in cls._posts if post['id'] == post_id), None)
        if not p:
            return None
        return {
            'id': p['id'],
            'title': p['title'],
            'content': p['content'],
            'author': p['author'],
            'author_username': p['author_username'],
            'avatar': p['avatar'],
            'category': p['category'],
            'timestamp': p['timestamp'],
            'likes': p['likes'],
            'comments_count': len(p['comments']),
            'has_liked': username in p.get('liked_by', set()),
            'comments': p['comments']
        }

    @classmethod
    def create_post(cls, title, category, content, author_name, author_username, avatar):
        post_id = f"post-{uuid.uuid4().hex[:6]}"
        new_post = {
            'id': post_id,
            'title': title,
            'category': category,
            'content': content,
            'author': author_name,
            'author_username': author_username,
            'avatar': avatar or 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
            'timestamp': 'Just now',
            'likes': 0,
            'liked_by': set(),
            'comments': []
        }
        cls._posts.insert(0, new_post)
        return cls.get_post_detail(post_id, username=author_username)

    @classmethod
    def add_comment(cls, post_id, content, author_name, author_username, avatar):
        p = next((post for post in cls._posts if post['id'] == post_id), None)
        if not p:
            return None
        comment_id = f"comm-{uuid.uuid4().hex[:6]}"
        comment = {
            'id': comment_id,
            'author': author_name,
            'author_username': author_username,
            'avatar': avatar or 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
            'content': content,
            'timestamp': 'Just now',
            'likes': 0
        }
        p['comments'].append(comment)
        return comment

    @classmethod
    def toggle_like(cls, post_id, username):
        p = next((post for post in cls._posts if post['id'] == post_id), None)
        if not p:
            return None
        if 'liked_by' not in p:
            p['liked_by'] = set()

        if username in p['liked_by']:
            p['liked_by'].remove(username)
            p['likes'] = max(0, p['likes'] - 1)
            has_liked = False
        else:
            p['liked_by'].add(username)
            p['likes'] += 1
            has_liked = True

        return {'likes': p['likes'], 'has_liked': has_liked}
