"""
API views for fan discussions, replies, and reactions.
Integrates community guidelines enforcement, badges, and reputation event tracking.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from core.response import api_success, api_error
from community.services import CommunityService
from community.models import Post
from accounts.services import ReputationService, BadgeService
from community.serializers import (
    PostSummarySerializer,
    PostDetailSerializer,
    PostCreateSerializer,
    CommentCreateSerializer
)

class PostListCreateView(APIView):
    """
    List discussion posts or submit a new fan thread.
    GET /api/v1/community/posts/?category=Discography&q=carpe
    POST /api/v1/community/posts/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        category = request.query_params.get('category')
        search = request.query_params.get('q')
        username = request.user.username if request.user.is_authenticated else None

        posts = CommunityService.list_posts(category=category, search=search, username=username)
        serializer = PostSummarySerializer(posts, many=True)
        return api_success(data=serializer.data, meta={'count': len(posts)})

    def post(self, request):
        if not request.user.is_authenticated:
            return api_error(
                message="Authentication required to publish a discussion.",
                code="UNAUTHORIZED",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        profile = getattr(request.user, 'profile', None)
        if profile and not profile.accepted_community_guidelines:
            return api_error(
                message="You must review and accept the JustBaddo Community Guidelines before creating your first discussion.",
                code="GUIDELINES_REQUIRED",
                status_code=status.HTTP_403_FORBIDDEN
            )

        serializer = PostCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid post data.", code="VALIDATION_ERROR", errors=serializer.errors)

        author_name = request.user.profile.display_name if hasattr(request.user, 'profile') and request.user.profile.display_name else request.user.username.capitalize()
        author_username = request.user.username
        avatar = request.user.profile.avatar_url if hasattr(request.user, 'profile') and request.user.profile.avatar_url else 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'

        created = CommunityService.create_post(
            title=serializer.validated_data['title'],
            category=serializer.validated_data['category'],
            content=serializer.validated_data['content'],
            author_name=author_name,
            author_username=author_username,
            avatar=avatar
        )

        # Record reputation event for publishing valuable discussion
        ReputationService.record_event(
            user=request.user,
            event_type='POST_PUBLISHED',
            source_type='post',
            source_id=created['id'],
            reason='Published community discussion'
        )
        # Award Conversation Starter badge if not yet earned
        BadgeService.award_badge(request.user, 'conversation-starter', reason='Started a community discussion thread')

        return api_success(data=created, message="Discussion topic created.", status_code=status.HTTP_201_CREATED)

class PostDetailView(APIView):
    """
    Retrieve full post discussion with threaded replies.
    GET /api/v1/community/posts/<id>/
    """
    permission_classes = [AllowAny]

    def get(self, request, post_id):
        username = request.user.username if request.user.is_authenticated else None
        post = CommunityService.get_post_detail(post_id, username=username)
        if not post:
            return api_error(message=f"Post '{post_id}' not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        serializer = PostDetailSerializer(post)
        return api_success(data=serializer.data)

class PostCommentCreateView(APIView):
    """
    Post a reply to an ongoing discussion.
    POST /api/v1/community/posts/<id>/comments/
    """
    permission_classes = [AllowAny]

    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return api_error(
                message="Authentication required to reply.",
                code="UNAUTHORIZED",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        profile = getattr(request.user, 'profile', None)
        if profile and not profile.accepted_community_guidelines:
            return api_error(
                message="You must review and accept the JustBaddo Community Guidelines before posting comments.",
                code="GUIDELINES_REQUIRED",
                status_code=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid comment payload.", code="VALIDATION_ERROR", errors=serializer.errors)

        author_name = request.user.profile.display_name if hasattr(request.user, 'profile') and request.user.profile.display_name else request.user.username.capitalize()
        author_username = request.user.username
        avatar = request.user.profile.avatar_url if hasattr(request.user, 'profile') and request.user.profile.avatar_url else 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'

        comment = CommunityService.add_comment(
            post_id=post_id,
            content=serializer.validated_data['content'],
            author_name=author_name,
            author_username=author_username,
            avatar=avatar
        )

        if not comment:
            return api_error(message="Post not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        # Record reputation event for positive contribution
        ReputationService.record_event(
            user=request.user,
            event_type='HELPFUL_CONTRIBUTION',
            source_type='comment',
            source_id=comment['id'],
            reason='Contributed reply to community discussion'
        )

        return api_success(data=comment, message="Comment posted successfully.", status_code=status.HTTP_201_CREATED)

class PostLikeToggleView(APIView):
    """
    Toggle like reaction on a post.
    POST /api/v1/community/posts/<id>/like/
    """
    permission_classes = [AllowAny]

    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return api_error(
                message="Authentication required to react to discussions.",
                code="UNAUTHORIZED",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        username = request.user.username
        result = CommunityService.toggle_like(post_id, username)
        if not result:
            return api_error(message="Post not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        # If post was liked, reward the author of the post with reputation points
        if result.get('liked'):
            post_obj = Post.objects.filter(post_id=post_id).first()
            if post_obj and post_obj.author and post_obj.author != request.user:
                ReputationService.record_event(
                    user=post_obj.author,
                    event_type='REACTION_RECEIVED',
                    source_type='post_like',
                    source_id=f"{post_id}_{request.user.id}",
                    reason='Received positive reaction on discussion'
                )

        return api_success(data=result, message="Reaction updated.")
