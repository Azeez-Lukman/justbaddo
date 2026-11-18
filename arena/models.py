"""
Database models for Fan Arena interactive modules (polls, battles, trivia, votes).
"""

from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    poll_id = models.CharField(max_length=50, unique=True)
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'arena_polls'
        ordering = ['-created_at']

    def __str__(self):
        return self.question

    @property
    def total_votes(self):
        return sum(option.votes for option in self.options.all())

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_id = models.CharField(max_length=50)
    text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'arena_poll_options'

    def __str__(self):
        return f"{self.text} ({self.votes} votes)"

class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='ballots')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='ballots')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='poll_votes')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'arena_poll_votes'
        unique_together = ('poll', 'user')

    def __str__(self):
        return f"Vote on {self.poll.question} by {self.user.username if self.user else 'Anon'}"

class SongBattle(models.Model):
    battle_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    song_a = models.ForeignKey('music.Track', on_delete=models.CASCADE, related_name='battles_as_song_a')
    song_b = models.ForeignKey('music.Track', on_delete=models.CASCADE, related_name='battles_as_song_b')
    song_a_votes = models.PositiveIntegerField(default=0)
    song_b_votes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'arena_song_battles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.song_a.title} vs {self.song_b.title}"

    @property
    def total_votes(self):
        return self.song_a_votes + self.song_b_votes

class BattleVote(models.Model):
    battle = models.ForeignKey(SongBattle, on_delete=models.CASCADE, related_name='ballots')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='battle_votes')
    selected_song = models.CharField(max_length=10, choices=[('song_a', 'Song A'), ('song_b', 'Song B')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'arena_battle_votes'
        unique_together = ('battle', 'user')

    def __str__(self):
        return f"Vote on {self.battle.title} for {self.selected_song}"

class TriviaQuestion(models.Model):
    question_id = models.CharField(max_length=50, unique=True)
    question = models.CharField(max_length=300)
    options = models.JSONField(default=list)
    correct_index = models.PositiveIntegerField()
    explanation = models.TextField()
    points = models.PositiveIntegerField(default=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'arena_trivia_questions'
        ordering = ['order']

    def __str__(self):
        return self.question

class TriviaSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trivia_submissions')
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    points_awarded = models.PositiveIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'arena_trivia_submissions'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} scored {self.score}/{self.total_questions}"
