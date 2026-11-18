"""
API views for polls, song battles, trivia challenge runner, and fan leaderboard.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from core.response import api_success, api_error
from arena.services import ArenaService
from arena.serializers import (
    PollSerializer,
    VoteRequestSerializer,
    SongBattleSerializer,
    BattleVoteSerializer,
    TriviaQuestionSerializer,
    TriviaSubmissionSerializer,
    LeaderboardEntrySerializer
)

class PollListView(APIView):
    """
    List active fan community polls with current vote tallies.
    GET /api/v1/arena/polls/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        polls = ArenaService.list_polls()
        serializer = PollSerializer(polls, many=True)
        return api_success(data=serializer.data)

class PollVoteView(APIView):
    """
    Cast vote on a community poll option.
    POST /api/v1/arena/polls/<id>/vote/
    """
    permission_classes = [AllowAny]

    def post(self, request, poll_id):
        serializer = VoteRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid vote option.", code="VALIDATION_ERROR", errors=serializer.errors)

        updated_polls, msg = ArenaService.vote_poll(
            poll_id=poll_id,
            option_id=serializer.validated_data['option_id'],
            user=request.user if request.user.is_authenticated else None
        )
        if not updated_polls:
            return api_error(message=msg, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST)

        return api_success(data=updated_polls, message=msg)

class SongBattleListView(APIView):
    """
    List head-to-head song battles with live percentage splits.
    GET /api/v1/arena/battles/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        battles = ArenaService.list_battles()
        serializer = SongBattleSerializer(battles, many=True)
        return api_success(data=serializer.data)

class SongBattleVoteView(APIView):
    """
    Vote for song_a or song_b in a song clash.
    POST /api/v1/arena/battles/<id>/vote/
    """
    permission_classes = [AllowAny]

    def post(self, request, battle_id):
        serializer = BattleVoteSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid battle choice.", code="VALIDATION_ERROR", errors=serializer.errors)

        updated_battles, msg = ArenaService.vote_battle(
            battle_id=battle_id,
            selected_song=serializer.validated_data['selected_song'],
            user=request.user if request.user.is_authenticated else None
        )
        if not updated_battles:
            return api_error(message=msg, code="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST)

        return api_success(data=updated_battles, message=msg)

class TriviaQuestionsView(APIView):
    """
    Retrieve questions for the verified discography trivia challenge.
    GET /api/v1/arena/trivia/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        questions = ArenaService.get_trivia_questions()
        serializer = TriviaQuestionSerializer(questions, many=True)
        return api_success(data=serializer.data, meta={'count': len(questions)})

class TriviaSubmitView(APIView):
    """
    Submit trivia answer sheet, receive scoring, breakdown, and award fan points.
    POST /api/v1/arena/trivia/submit/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TriviaSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return api_error(message="Invalid answers map.", code="VALIDATION_ERROR", errors=serializer.errors)

        result = ArenaService.evaluate_trivia(serializer.validated_data['answers'])
        return api_success(data=result, message=f"Trivia challenge scored! You earned {result['points_awarded']} points.")

class LeaderboardView(APIView):
    """
    Retrieve top fan standings and prestige tier ranks.
    GET /api/v1/arena/leaderboard/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        leaderboard = ArenaService.get_leaderboard()
        serializer = LeaderboardEntrySerializer(leaderboard, many=True)
        return api_success(data=serializer.data, meta={'count': len(leaderboard)})
