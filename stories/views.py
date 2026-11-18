"""
API views for fan editorial stories, submissions, and reader modal data.
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
    POST /api/v1/stories/submit/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StorySubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid submission payload.", code="VALIDATION_ERROR", errors=serializer.errors)

        author_name = 'Tunde Baddo' if not request.user.is_authenticated else request.user.username.capitalize()
        author_role = 'Community Member'
        author_avatar = 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'

        new_story = StoriesService.submit_story(
            title=serializer.validated_data['title'],
            content=serializer.validated_data['content'],
            author_name=author_name,
            author_role=author_role,
            author_avatar=author_avatar,
            read_time=serializer.validated_data.get('read_time', '5 min read'),
            cover_image=serializer.validated_data.get('cover_image'),
            tags=serializer.validated_data.get('tags', '')
        )

        return api_success(
            data=new_story,
            message="Story submitted for editorial review. Thank you for contributing to the archive!",
            status_code=status.HTTP_201_CREATED
        )

class StoryPublishView(APIView):
    """
    Approve and publish a pending story (moderator action).
    POST /api/v1/stories/<id>/publish/
    """
    permission_classes = [AllowAny]  # In Phase 2 allow dev testing; Phase 3 locks to IsAdminOrModerator

    def post(self, request, story_id):
        success, msg = StoriesService.publish_story(story_id)
        if not success:
            return api_error(message=msg, code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)
        return api_success(message=msg)
