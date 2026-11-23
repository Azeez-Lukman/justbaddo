"""
API views for fan editorial stories, submissions, and reader modal data.
Allows public browsing and reading while requiring authentication for submissions.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.response import api_success, api_error
from core.permissions import IsAdminOrModerator
from stories.services import StoriesService
from stories.serializers import (
    StorySummarySerializer,
    StoryDetailSerializer,
    StorySubmissionSerializer
)

class StoryListView(APIView):
    """
    List published fan essays and concert reflections.
    GET /api/v1/stories/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        stories = StoriesService.list_stories(status_filter='PUBLISHED')
        serializer = StorySummarySerializer(stories, many=True)
        return api_success(data=serializer.data, meta={'count': len(stories)})

class StoryDetailView(APIView):
    """
    Retrieve full article body and author credentials for the story reader.
    GET /api/v1/stories/<id>/
    """
    permission_classes = [AllowAny]

    def get(self, request, story_id):
        story = StoriesService.get_story_by_id(story_id)
        if not story:
            return api_error(message=f"Story '{story_id}' not found.", code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        serializer = StoryDetailSerializer(story)
        return api_success(data=serializer.data)

class StorySubmitView(APIView):
    """
    Submit a personal fan reflection or historical essay for editorial review.
    Requires authentication and community guidelines acceptance.
    POST /api/v1/stories/submit/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        if not request.user.is_authenticated:
            return api_error(
                message="Authentication required to submit fan stories.",
                code="UNAUTHORIZED",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        profile = getattr(request.user, 'profile', None)
        if profile and not profile.accepted_community_guidelines:
            return api_error(
                message="You must review and accept the JustBaddo Community Guidelines before submitting stories.",
                code="GUIDELINES_REQUIRED",
                status_code=status.HTTP_403_FORBIDDEN
            )

        serializer = StorySubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid submission payload.", code="VALIDATION_ERROR", errors=serializer.errors)

        author_name = request.user.profile.display_name if hasattr(request.user, 'profile') and request.user.profile.display_name else request.user.username.capitalize()
        author_role = 'Community Member'
        author_avatar = request.user.profile.avatar_url if hasattr(request.user, 'profile') and request.user.profile.avatar_url else 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'

        created = StoriesService.submit_story(
            title=serializer.validated_data['title'],
            excerpt=serializer.validated_data['excerpt'],
            content=serializer.validated_data['content'],
            author_name=author_name,
            author_role=author_role,
            author_avatar=author_avatar,
            tags=serializer.validated_data.get('tags', []),
            author_user=request.user
        )

        return api_success(
            data=created,
            message="Your fan story has been submitted for editorial review.",
            status_code=status.HTTP_201_CREATED
        )

class StoryPublishView(APIView):
    """
    Publish a submitted fan story (moderator/staff only).
    POST /api/v1/stories/<id>/publish/
    """
    permission_classes = [IsAdminOrModerator]

    def post(self, request, story_id):
        success, msg = StoriesService.publish_story(story_id)
        if not success:
            return api_error(message=msg, code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

        return api_success(message="Story published successfully.")

