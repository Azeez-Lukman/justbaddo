from django.contrib import admin
from arena.models import Poll, PollOption, PollVote, SongBattle, BattleVote, TriviaQuestion, TriviaSubmission

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 2

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'poll_id', 'category', 'total_votes', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('question',)
    inlines = [PollOptionInline]

@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'poll', 'votes')

@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'option', 'user', 'created_at')

@admin.register(SongBattle)
class SongBattleAdmin(admin.ModelAdmin):
    list_display = ('title', 'battle_id', 'category', 'song_a', 'song_a_votes', 'song_b', 'song_b_votes', 'total_votes', 'is_active')
    list_filter = ('is_active',)

@admin.register(BattleVote)
class BattleVoteAdmin(admin.ModelAdmin):
    list_display = ('battle', 'user', 'selected_song', 'created_at')

@admin.register(TriviaQuestion)
class TriviaQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'question', 'correct_index', 'points', 'order')

@admin.register(TriviaSubmission)
class TriviaSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'total_questions', 'points_awarded', 'submitted_at')
