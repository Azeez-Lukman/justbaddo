"""
Fan Stories service layer for JustBaddo.
Manages published editorial fan essays and submissions in PostgreSQL.
"""

from stories.models import Story
from django.contrib.auth.models import User
import uuid

class StoriesService:
    @classmethod
    def list_stories(cls, status_filter='PUBLISHED'):
        qs = Story.objects.all()
        if status_filter:
            qs = qs.filter(status=status_filter)

        results = []
        for s in qs:
            results.append({
                'id': s.story_id,
                'title': s.title,
                'author': s.author_name,
                'author_role': s.author_role,
                'author_avatar': s.author_avatar or 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=150&q=80',
                'date': s.created_at.strftime('%B %d, %Y') if s.created_at else 'Recent',
                'read_time': s.read_time,
                'cover_image': s.cover_image or 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80',
                'excerpt': s.excerpt,
                'likes': s.likes_count,
                'tags': s.tags,
                'status': s.status
            })
        return results

    @classmethod
    def get_story_by_id(cls, story_id):
        s = Story.objects.filter(story_id=story_id).first()
        if not s:
            return None

        return {
            'id': s.story_id,
            'title': s.title,
            'author': s.author_name,
            'author_role': s.author_role,
            'author_avatar': s.author_avatar or 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=150&q=80',
            'date': s.created_at.strftime('%B %d, %Y') if s.created_at else 'Recent',
            'read_time': s.read_time,
            'cover_image': s.cover_image or 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80',
            'excerpt': s.excerpt,
            'content': s.content,
            'likes': s.likes_count,
            'tags': s.tags,
            'status': s.status
        }

    @classmethod
    def submit_story(cls, title, content, author_name, author_role, author_avatar, read_time='5 min read', cover_image=None, tags='', user=None, excerpt=None, author_user=None, **kwargs):
        if not user and author_user:
            user = author_user
        if isinstance(tags, list):
            tag_list = tags if tags else ['Fan Reflection']
        elif isinstance(tags, str) and tags:
            tag_list = [t.strip() for t in tags.split(',') if t.strip()]
        else:
            tag_list = ['Fan Reflection']
        story_id = f"story-{uuid.uuid4().hex[:6]}"
        if not excerpt:
            excerpt = content[:200] + ('...' if len(content) > 200 else '')

        s = Story.objects.create(
            story_id=story_id,
            author_user=user if user and user.is_authenticated else None,
            author_name=author_name,
            author_role=author_role or 'Community Fan',
            author_avatar=author_avatar or 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80',
            read_time=read_time,
            cover_image=cover_image or 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80',
            excerpt=excerpt,
            content=f"<p class='text-zinc-300 leading-relaxed'>{content}</p>",
            tags=tag_list,
            status='PENDING_REVIEW'
        )
        return cls.get_story_by_id(story_id)

    @classmethod
    def publish_story(cls, story_id):
        s = Story.objects.filter(story_id=story_id).first()
        if not s:
            return False, "Story not found."
        s.status = 'PUBLISHED'
        s.save()
        return True, "Story published."
