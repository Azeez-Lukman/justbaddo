"""
Fan Arena service layer for JustBaddo.
Manages polls, song battles, trivia challenge runner, and leaderboards using PostgreSQL models.
"""

from arena.models import Poll, PollOption, PollVote, SongBattle, BattleVote, TriviaQuestion, TriviaSubmission
from accounts.models import UserProfile
from django.contrib.auth.models import User

class ArenaService:
    @classmethod
    def list_polls(cls):
        polls = Poll.objects.filter(is_active=True).prefetch_related('options')
        formatted = []
        for p in polls:
            total_votes = sum(o.votes for o in p.options.all())
            options = []
            for o in p.options.all():
                pct = round((o.votes / total_votes * 100)) if total_votes > 0 else 0
                options.append({'id': o.option_id, 'text': o.text, 'votes': o.votes, 'percentage': pct})
            formatted.append({
                'id': p.poll_id,
                'question': p.question,
                'category': p.category,
                'total_votes': total_votes,
                'options': options
            })
        return formatted

    @classmethod
    def vote_poll(cls, poll_id, option_id, user=None):
        p = Poll.objects.filter(poll_id=poll_id).first()
        if not p:
            return None, "Poll not found."

        opt = p.options.filter(option_id=option_id).first()
        if not opt:
            return None, "Option not found in this poll."

        if user and user.is_authenticated:
            if PollVote.objects.filter(poll=p, user=user).exists():
                return None, "You have already voted in this poll."
            PollVote.objects.create(poll=p, option=opt, user=user)
        else:
            PollVote.objects.create(poll=p, option=opt)

        opt.votes += 1
        opt.save()
        return cls.list_polls(), "Vote recorded successfully."

    @classmethod
    def list_battles(cls):
        battles = SongBattle.objects.filter(is_active=True).select_related('song_a', 'song_b')
        formatted = []
        for b in battles:
            total = b.song_a_votes + b.song_b_votes
            pct_a = round((b.song_a_votes / total * 100)) if total > 0 else 50
            pct_b = 100 - pct_a
            formatted.append({
                'id': b.battle_id,
                'title': b.title,
                'category': b.category,
                'total_votes': total,
                'song_a': {
                    'id': b.song_a.track_id,
                    'title': b.song_a.title,
                    'year': b.song_a.release_year,
                    'album': b.song_a.album.title if b.song_a.album else 'Single',
                    'votes': b.song_a_votes,
                    'coverArt': b.song_a.cover_art,
                    'percentage': pct_a
                },
                'song_b': {
                    'id': b.song_b.track_id,
                    'title': b.song_b.title,
                    'year': b.song_b.release_year,
                    'album': b.song_b.album.title if b.song_b.album else 'Single',
                    'votes': b.song_b_votes,
                    'coverArt': b.song_b.cover_art,
                    'percentage': pct_b
                }
            })
        return formatted

    @classmethod
    def vote_battle(cls, battle_id, selected_song, user=None):
        b = SongBattle.objects.filter(battle_id=battle_id).first()
        if not b:
            return None, "Battle not found."

        if user and user.is_authenticated:
            if BattleVote.objects.filter(battle=b, user=user).exists():
                return None, "You have already voted in this song battle."
            BattleVote.objects.create(battle=b, user=user, selected_song=selected_song)
        else:
            BattleVote.objects.create(battle=b, selected_song=selected_song)

        if selected_song == 'song_a':
            b.song_a_votes += 1
            b.save()
        elif selected_song == 'song_b':
            b.song_b_votes += 1
            b.save()
        else:
            return None, "Invalid song choice."

        return cls.list_battles(), "Battle vote recorded."

    @classmethod
    def get_trivia_questions(cls):
        qs = TriviaQuestion.objects.all().order_by('order')
        return [
            {'id': q.question_id, 'question': q.question, 'options': q.options}
            for q in qs
        ]

    @classmethod
    def evaluate_trivia(cls, user_answers, user=None):
        questions = TriviaQuestion.objects.all().order_by('order')
        score = 0
        feedback = []

        for q in questions:
            qid = q.question_id
            ans = user_answers.get(qid)
            is_correct = (ans == q.correct_index)
            if is_correct:
                score += 1
            feedback.append({
                'id': qid,
                'is_correct': is_correct,
                'correct_index': q.correct_index,
                'correct_answer': q.options[q.correct_index] if q.options and len(q.options) > q.correct_index else '',
                'explanation': q.explanation
            })

        points_awarded = score * 50
        if user and user.is_authenticated:
            TriviaSubmission.objects.create(
                user=user,
                score=score,
                total_questions=questions.count(),
                points_awarded=points_awarded
            )
            profile = getattr(user, 'profile', None)
            if profile:
                profile.points += points_awarded
                profile.save()

        total_count = questions.count() or 5
        return {
            'score': score,
            'total_questions': total_count,
            'percentage': round((score / total_count) * 100),
            'points_awarded': points_awarded,
            'feedback': feedback
        }

    @classmethod
    def get_leaderboard(cls):
        profiles = UserProfile.objects.all().select_related('user').order_by('-points')[:10]
        results = []
        for rank, p in enumerate(profiles, start=1):
            results.append({
                'rank': rank,
                'username': p.user.username,
                'name': p.display_name,
                'points': p.points,
                'tier': p.fan_tier,
                'avatar': p.avatar_url or 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'
            })
        return results
