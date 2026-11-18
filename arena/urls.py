"""
URL routing for Fan Arena endpoints.
"""

from django.urls import path
from arena.views import (
    PollListView,
    PollVoteView,
    SongBattleListView,
    SongBattleVoteView,
    TriviaQuestionsView,
    TriviaSubmitView,
    LeaderboardView
)

app_name = 'arena'

urlpatterns = [
    path('polls/', PollListView.as_view(), name='poll-list'),
    path('polls/<str:poll_id>/vote/', PollVoteView.as_view(), name='poll-vote'),
    path('battles/', SongBattleListView.as_view(), name='battle-list'),
    path('battles/<str:battle_id>/vote/', SongBattleVoteView.as_view(), name='battle-vote'),
    path('trivia/', TriviaQuestionsView.as_view(), name='trivia-questions'),
    path('trivia/submit/', TriviaSubmitView.as_view(), name='trivia-submit'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
