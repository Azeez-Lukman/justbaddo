"""
Community service layer for JustBaddo.
Manages discussion posts, threaded comments, and likes in PostgreSQL.
"""

from community.models import Post, Comment, PostLike
from django.contrib.auth.models import User
from django.db.models import Q
import uuid

class CommunityService:
    @classmethod
    def list_posts(cls, category=None, search=None, username='baddofan99'):
        qs = Post.objects.all().select_related('author__profile').prefetch_related('comments', 'likes')
        if category and category.lower() != 'all':
            qs = qs.filter(category__iexact=category)
        if search:
            q = search.strip()
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))

        results = []
        for p in qs:
            author_profile = getattr(p.author, 'profile', None)
            has_liked = p.likes.filter(user__username=username).exists() if username else False
            results.append({
                'id': p.post_id,
                'title': p.title,
                'content': p.content,
                'author': author_profile.display_name if author_profile else p.author.username,
                'author_username': p.author.username,
                'avatar': author_profile.avatar_url if author_profile and author_profile.avatar_url else 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
                'category': p.category,
                'timestamp': p.created_at.strftime('%B %d, %Y') if p.created_at else 'Recent',
                'likes': p.likes_count,
                'comments_count': p.comments.count(),
                'has_liked': has_liked
            })
        return results

    @classmethod
    def get_post_detail(cls, post_id, username='baddofan99'):
        p = Post.objects.filter(post_id=post_id).select_related('author__profile').prefetch_related('comments__author__profile', 'likes').first()
        if not p:
            return None

        author_profile = getattr(p.author, 'profile', None)
        has_liked = p.likes.filter(user__username=username).exists() if username else False

        comments = []
        for c in p.comments.all().order_by('created_at'):
            c_profile = getattr(c.author, 'profile', None)
            comments.append({
                'id': c.comment_id,
                'author': c_profile.display_name if c_profile else c.author.username,
                'author_username': c.author.username,
                'avatar': c_profile.avatar_url if c_profile and c_profile.avatar_url else 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
                'content': c.content,
                'timestamp': c.created_at.strftime('%B %d, %Y') if c.created_at else 'Recent',
                'likes': c.likes_count
            })

        return {
            'id': p.post_id,
            'title': p.title,
            'content': p.content,
            'author': author_profile.display_name if author_profile else p.author.username,
            'author_username': p.author.username,
            'avatar': author_profile.avatar_url if author_profile and author_profile.avatar_url else 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
            'category': p.category,
            'timestamp': p.created_at.strftime('%B %d, %Y') if p.created_at else 'Recent',
            'likes': p.likes_count,
            'comments_count': len(comments),
            'has_liked': has_liked,
            'comments': comments
        }

    @classmethod
    def create_post(cls, title, category, content, author_name, author_username, avatar):
        user, _ = User.objects.get_or_create(username=author_username, defaults={'email': f"{author_username}@justbaddo.local"})
        post_id = f"post-{uuid.uuid4().hex[:6]}"

        p = Post.objects.create(
            post_id=post_id,
            title=title,
            category=category,
            content=content,
            author=user,
            likes_count=0
        )
        return cls.get_post_detail(post_id, username=author_username)

    @classmethod
    def add_comment(cls, post_id, content, author_name, author_username, avatar):
        p = Post.objects.filter(post_id=post_id).first()
        if not p:
            return None

        user, _ = User.objects.get_or_create(username=author_username, defaults={'email': f"{author_username}@justbaddo.local"})
        comment_id = f"comm-{uuid.uuid4().hex[:6]}"

        c = Comment.objects.create(
            comment_id=comment_id,
            post=p,
            author=user,
            content=content,
            likes_count=0
        )

        return {
            'id': c.comment_id,
            'author': author_name,
            'author_username': author_username,
            'avatar': avatar or 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
            'content': c.content,
            'timestamp': 'Just now',
            'likes': 0
        }

    @classmethod
    def toggle_like(cls, post_id, username):
        p = Post.objects.filter(post_id=post_id).first()
        if not p:
            return None

        user, _ = User.objects.get_or_create(username=username, defaults={'email': f"{username}@justbaddo.local"})
        existing_like = PostLike.objects.filter(post=p, user=user).first()

        if existing_like:
            existing_like.delete()
            p.likes_count = max(0, p.likes_count - 1)
            p.save()
            return {'likes': p.likes_count, 'has_liked': False}
        else:
            PostLike.objects.create(post=p, user=user)
            p.likes_count += 1
            p.save()
            return {'likes': p.likes_count, 'has_liked': True}
