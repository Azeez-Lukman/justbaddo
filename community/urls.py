"""
URL routing for community discussion endpoints.
"""

from django.urls import path
from community.views import (
    PostListCreateView,
    PostDetailView,
    PostCommentCreateView,
    PostLikeToggleView
)

app_name = 'community'

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<str:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<str:post_id>/comments/', PostCommentCreateView.as_view(), name='post-comment-create'),
    path('posts/<str:post_id>/like/', PostLikeToggleView.as_view(), name='post-like-toggle'),
]
