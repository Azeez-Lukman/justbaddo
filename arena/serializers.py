"""
Serializers for Fan Arena interactive modules (polls, battles, trivia, leaderboard).
"""

from rest_framework import serializers

class PollOptionSerializer(serializers.Serializer):
    id = serializers.CharField()
    text = serializers.CharField()
    votes = serializers.IntegerField()
    percentage = serializers.IntegerField(required=False)

class PollSerializer(serializers.Serializer):
    id = serializers.CharField()
    question = serializers.CharField()
    category = serializers.CharField()
    total_votes = serializers.IntegerField()
    options = PollOptionSerializer(many=True)

class VoteRequestSerializer(serializers.Serializer):
    option_id = serializers.CharField()

class SongBattleSongSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    year = serializers.IntegerField()
    album = serializers.CharField()
    votes = serializers.IntegerField()
    coverArt = serializers.URLField()
    percentage = serializers.IntegerField(required=False)

class SongBattleSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    category = serializers.CharField()
    total_votes = serializers.IntegerField()
    song_a = SongBattleSongSerializer()
    song_b = SongBattleSongSerializer()

class BattleVoteSerializer(serializers.Serializer):
    selected_song = serializers.ChoiceField(choices=['song_a', 'song_b'])

class TriviaQuestionSerializer(serializers.Serializer):
    id = serializers.CharField()
    question = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField())
    # Note: correct_answer is omitted in client delivery to prevent client cheating!

class TriviaSubmissionSerializer(serializers.Serializer):
    answers = serializers.DictField(child=serializers.IntegerField())

class LeaderboardEntrySerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    username = serializers.CharField()
    name = serializers.CharField()
    points = serializers.IntegerField()
    tier = serializers.CharField()
    avatar = serializers.URLField()
