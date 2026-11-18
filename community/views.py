"""
API views for community feed, threaded replies, and reactions.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.response import api_success, api_error
from community.services import CommunityService
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
        username = request.user.username if request.user.is_authenticated else 'baddofan99'

        posts = CommunityService.list_posts(category=category, search=search, username=username)
        serializer = PostSummarySerializer(posts, many=True)
        return api_success(data=serializer.data, meta={'count': len(posts)})

    def post(self, request):
        if not request.user.is_authenticated:
            return api_error(message="Authentication required to publish a discussion.", code="UNAUTHORIZED", status_code=status.HTTP_401_UNAUTHORIZED)
        serializer = PostCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid post data.", code="VALIDATION_ERROR", errors=serializer.errors)

        author_name = 'Tunde Baddo' if not request.user.is_authenticated else request.user.username.capitalize()
        author_username = request.user.username if request.user.is_authenticated else 'baddofan99'
        avatar = 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'

        created = CommunityService.create_post(
            title=serializer.validated_data['title'],
            category=serializer.validated_data['category'],
            content=serializer.validated_data['content'],
            author_name=author_name,
            author_username=author_username,
            avatar=avatar
        )
        return api_success(data=created, message="Discussion topic created.", status_code=status.HTTP_201_CREATED)

class PostDetailView(APIView):
    """
    Retrieve full post discussion with threaded replies.
    GET /api/v1/community/posts/<id>/
    """
    permission_classes = [AllowAny]

    def get(self, request, post_id):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
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
        serializer = CommentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid comment payload.", code="VALIDATION_ERROR", errors=serializer.errors)

        author_name = 'Tunde Baddo' if not request.user.is_authenticated else request.user.username.capitalize()
        author_username = request.user.username if request.user.is_authenticated else 'baddofan99'
        avatar = 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'

        comment = CommunityService.add_comment(
            post_id=post_id,
            content=serializer.validated_data['content'],
            author_name=author_name,
            author_username=author_username,
            avatar=avatar
        )

        if not comment:
            return api_error(message="Post not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        return api_success(data=comment, message="Comment posted successfully.", status_code=status.HTTP_201_CREATED)

class PostLikeToggleView(APIView):
    """
    Toggle like reaction on a post.
    POST /api/v1/community/posts/<id>/like/
    """
    permission_classes = [AllowAny]

    def post(self, request, post_id):
        username = request.user.username if request.user.is_authenticated else 'baddofan99'
        result = CommunityService.toggle_like(post_id, username)
        if not result:
            return api_error(message="Post not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        return api_success(data=result, message="Reaction updated.")
