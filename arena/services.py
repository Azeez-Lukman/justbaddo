"""
Fan Arena service layer for JustBaddo.
Manages real-time voting on polls, song battles, trivia scoring, and fan leaderboard rankings.
"""

class ArenaService:
    """
    In-memory arena repository for Phase 2.
    """

    _polls = [
        {
            'id': 'poll-01',
            'question': 'Which opening track sets the highest bar across Olamide entire discography?',
            'category': 'Track Discography',
            'options': [
                {'id': 'opt-01', 'text': 'Voice of the Street (YBNL, 2012)', 'votes': 489},
                {'id': 'opt-02', 'text': 'Prayer for Client (Street OT, 2014)', 'votes': 312},
                {'id': 'opt-03', 'text': 'Eyan Mayweather (Eyan Mayweather, 2015)', 'votes': 560},
                {'id': 'opt-04', 'text': 'Need for Speed (UY Scuti, 2021)', 'votes': 214}
            ]
        },
        {
            'id': 'poll-02',
            'question': 'Which producer achieved the deepest sonic chemistry with Baddo?',
            'category': 'Production Chemistry',
            'options': [
                {'id': 'opt-p1', 'text': 'Pheelz (Mr. Producer)', 'votes': 840},
                {'id': 'opt-p2', 'text': 'Young Jonn (The Wicked Producer)', 'votes': 792},
                {'id': 'opt-p3', 'text': 'ID Cabasa (The Architect)', 'votes': 510},
                {'id': 'opt-p4', 'text': 'P.Priime (The Renaissance)', 'votes': 390}
            ]
        }
    ]

    _battles = [
        {
            'id': 'battle-01',
            'title': 'The Supreme 2017–2018 Mainland Dance Anthem',
            'category': 'High-Energy Dance Anthems',
            'song_a': {
                'id': 's-03',
                'title': 'Wo!!',
                'year': 2017,
                'album': 'Lagos Nawa / Single',
                'votes': 1420,
                'coverArt': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80'
            },
            'song_b': {
                'id': 's-04',
                'title': 'Science Student',
                'year': 2018,
                'album': 'Single',
                'votes': 1290,
                'coverArt': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=400&q=80'
            }
        }
    ]

    _trivia = [
        {
            'id': 'q1',
            'question': 'Which studio album served as Olamide debut release in 2011?',
            'options': ['YBNL', 'Rapsodi', 'Baddest Guy Ever Liveth', 'Street OT'],
            'correct_index': 1,
            'explanation': 'Rapsodi was released on March 14, 2011 via Coded Tunes/NotJustOk.'
        },
        {
            'id': 'q2',
            'question': 'Which artist was featured on the iconic breakthrough single "Omo To Shan" (2011)?',
            'options': ['Davido', 'Wizkid', 'Reminisce', '9ice'],
            'correct_index': 1,
            'explanation': 'Wizkid laid the melodic chorus on Omo To Shan during the Coded Tunes era.'
        },
        {
            'id': 'q3',
            'question': 'What was the venue for the historic first edition of Olamide Live In Concert (OLIC 1) in 2014?',
            'options': ['Teslim Balogun Stadium', 'Eko Hotel Convention Centre', 'National Stadium Lagos', 'TBS Lagos'],
            'correct_index': 1,
            'explanation': 'OLIC 1 took place on December 28, 2014 at Eko Convention Centre in Victoria Island.'
        },
        {
            'id': 'q4',
            'question': 'In which year did Olamide announce the landmark YBNL Nation joint venture with EMPIRE?',
            'options': ['2018', '2019', '2020', '2021'],
            'correct_index': 2,
            'explanation': 'The historic EMPIRE joint venture was finalized in February 2020.'
        },
        {
            'id': 'q5',
            'question': 'Which 2024 surprise EP features tracks like "Metaverse", "Uptown Disco", and "Morowore"?',
            'options': ['999', 'Ikigai, Vol. 1', 'UY Scuti', 'Unruly'],
            'correct_index': 1,
            'explanation': 'Ikigai / 生き甲斐, Vol. 1 was released unexpectedly on June 26, 2024.'
        }
    ]

    _leaderboard = [
        {'rank': 1, 'username': 'bariga_general', 'name': 'Adewale Johnson', 'points': 8920, 'tier': 'Voice of the Street Legend', 'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80'},
        {'rank': 2, 'username': 'ybnl_princess', 'name': 'Simisola Cole', 'points': 7640, 'tier': 'YBNL Vanguard', 'avatar': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80'},
        {'rank': 3, 'username': 'olic_veteran', 'name': 'Emeka Obi', 'points': 6980, 'tier': 'OLIC Veteran', 'avatar': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80'},
        {'rank': 4, 'username': 'baddofan99', 'name': 'Tunde Baddo', 'points': 4850, 'tier': 'Voice of the Street Ambassador', 'avatar': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80'},
        {'rank': 5, 'username': 'folake_a', 'name': 'Folake Adeleke', 'points': 4210, 'tier': 'Day One Disciple', 'avatar': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80'}
    ]

    @classmethod
    def list_polls(cls):
        formatted = []
        for p in cls._polls:
            total_votes = sum(o['votes'] for o in p['options'])
            options = []
            for o in p['options']:
                pct = round((o['votes'] / total_votes * 100)) if total_votes > 0 else 0
                options.append({**o, 'percentage': pct})
            formatted.append({
                'id': p['id'],
                'question': p['question'],
                'category': p['category'],
                'total_votes': total_votes,
                'options': options
            })
        return formatted

    @classmethod
    def vote_poll(cls, poll_id, option_id):
        p = next((poll for poll in cls._polls if poll['id'] == poll_id), None)
        if not p:
            return None, "Poll not found."
        opt = next((o for o in p['options'] if o['id'] == option_id), None)
        if not opt:
            return None, "Option not found in this poll."
        opt['votes'] += 1
        return cls.list_polls(), "Vote recorded successfully."

    @classmethod
    def list_battles(cls):
        formatted = []
        for b in cls._battles:
            total = b['song_a']['votes'] + b['song_b']['votes']
            pct_a = round((b['song_a']['votes'] / total * 100)) if total > 0 else 50
            pct_b = 100 - pct_a
            formatted.append({
                'id': b['id'],
                'title': b['title'],
                'category': b['category'],
                'total_votes': total,
                'song_a': {**b['song_a'], 'percentage': pct_a},
                'song_b': {**b['song_b'], 'percentage': pct_b}
            })
        return formatted

    @classmethod
    def vote_battle(cls, battle_id, selected_song):
        b = next((bat for bat in cls._battles if bat['id'] == battle_id), None)
        if not b:
            return None, "Battle not found."
        if selected_song == 'song_a':
            b['song_a']['votes'] += 1
        elif selected_song == 'song_b':
            b['song_b']['votes'] += 1
        else:
            return None, "Invalid song choice."
        return cls.list_battles(), "Battle vote recorded."

    @classmethod
    def get_trivia_questions(cls):
        # Strip correct_index for client security
        return [
            {'id': q['id'], 'question': q['question'], 'options': q['options']}
            for q in cls._trivia
        ]

    @classmethod
    def evaluate_trivia(cls, user_answers):
        score = 0
        feedback = []
        for q in cls._trivia:
            qid = q['id']
            ans = user_answers.get(qid)
            is_correct = (ans == q['correct_index'])
            if is_correct:
                score += 1
            feedback.append({
                'id': qid,
                'is_correct': is_correct,
                'correct_index': q['correct_index'],
                'correct_answer': q['options'][q['correct_index']],
                'explanation': q['explanation']
            })
        points_awarded = score * 50
        return {
            'score': score,
            'total_questions': len(cls._trivia),
            'percentage': round((score / len(cls._trivia)) * 100),
            'points_awarded': points_awarded,
            'feedback': feedback
        }

    @classmethod
    def get_leaderboard(cls):
        return cls._leaderboard
