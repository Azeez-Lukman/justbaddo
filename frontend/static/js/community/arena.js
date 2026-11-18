/**
 * JUSTBADDO — Fan Arena Interactive Engine
 * Handles live polls, song battles, interactive quizzes with answer feedback, and leaderboard.
 */

window.JustBaddoArena = {
  activeQuizState: {
    quiz: null,
    currentQuestionIndex: 0,
    score: 0,
    selectedOption: null,
    isAnswered: false
  },

  init() {
    this.renderPolls();
    this.renderBattles();
    this.renderQuizOverview();
    this.renderLeaderboard();
    this.bindEvents();
  },

  renderPolls() {
    const container = document.getElementById('jb-arena-polls-list');
    if (!container) return;

    container.innerHTML = JUSTBADDO_ARENA.polls.map(poll => {
      return `
        <div class="p-6 rounded-2xl border border-zinc-800 bg-zinc-900/60" data-poll-id="${poll.id}">
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs uppercase tracking-wider font-bold text-amber-500">Live Community Poll</span>
            <span class="text-xs text-zinc-500 font-mono">${poll.totalVotes} total votes</span>
          </div>
          <h3 class="text-lg font-bold text-zinc-100 mb-1">${poll.question}</h3>
          <p class="text-xs text-zinc-400 mb-5">${poll.description}</p>

          <div class="space-y-3">
            ${poll.options.map(opt => {
              const isSelected = poll.userVotedOption === opt.id;
              return `
                <button class="w-full relative overflow-hidden rounded-xl border ${isSelected ? 'border-amber-500 bg-amber-500/10' : 'border-zinc-800 hover:border-zinc-700 bg-zinc-950/60'} p-3.5 text-left transition-all group" data-action-vote-poll="${poll.id}" data-option-id="${opt.id}">
                  <!-- Result Fill Bar -->
                  <div class="absolute inset-y-0 left-0 ${isSelected ? 'bg-amber-500/20' : 'bg-zinc-800/40'} transition-all duration-500" style="width: ${poll.hasVoted ? opt.percentage : 0}%"></div>
                  
                  <div class="relative flex items-center justify-between text-xs z-10">
                    <span class="font-medium ${isSelected ? 'text-amber-300 font-semibold' : 'text-zinc-200 group-hover:text-white'}">${opt.text}</span>
                    <span class="font-mono ${isSelected ? 'text-amber-400 font-bold' : 'text-zinc-400'}">${poll.hasVoted ? `${opt.percentage}%` : 'Vote'}</span>
                  </div>
                </button>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }).join('');

    JustBaddoUI.refreshIcons();
  },

  renderBattles() {
    const container = document.getElementById('jb-arena-battles-list');
    if (!container) return;

    container.innerHTML = JUSTBADDO_ARENA.battles.map(battle => {
      const hasVoted = battle.hasVoted;
      return `
        <div class="p-6 rounded-2xl border border-zinc-800 bg-zinc-900/60" data-battle-id="${battle.id}">
          <div class="flex items-center justify-between mb-4">
            <span class="text-xs uppercase tracking-wider font-bold text-amber-500">${battle.category} Battle</span>
            <span class="text-xs text-zinc-500 font-mono">${battle.totalVotes} fan votes</span>
          </div>
          <h3 class="text-lg font-bold text-zinc-100 mb-1">${battle.title}</h3>
          <p class="text-xs text-zinc-400 mb-6">${battle.description}</p>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 relative">
            <!-- VS Badge -->
            <div class="hidden sm:flex absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-20 w-8 h-8 rounded-full bg-amber-500 text-black font-black text-xs items-center justify-center shadow-lg">
              VS
            </div>

            <!-- Track A -->
            <div class="relative overflow-hidden rounded-xl border ${battle.userVotedSong === battle.trackA.id ? 'border-amber-500 bg-amber-500/10' : 'border-zinc-800 bg-zinc-950/80'} p-4 flex flex-col justify-between transition-all">
              <div class="flex items-center gap-3 mb-4">
                <img src="${battle.trackA.coverArt}" alt="${battle.trackA.title}" class="w-12 h-12 rounded-lg object-cover">
                <div>
                  <h4 class="text-sm font-bold text-zinc-100">${battle.trackA.title}</h4>
                  <p class="text-xs text-zinc-400">${battle.trackA.album}</p>
                </div>
              </div>

              ${hasVoted ? `
                <div class="mb-3">
                  <div class="flex justify-between text-xs mb-1 font-mono">
                    <span class="text-zinc-400">${battle.trackA.votes} votes</span>
                    <span class="text-amber-400 font-bold">${battle.trackA.percentage}%</span>
                  </div>
                  <div class="h-2 rounded-full bg-zinc-800 overflow-hidden">
                    <div class="h-full bg-amber-500" style="width: ${battle.trackA.percentage}%"></div>
                  </div>
                </div>
              ` : ''}

              <button class="w-full py-2.5 rounded-xl border ${battle.userVotedSong === battle.trackA.id ? 'bg-amber-500 text-black font-bold' : 'border-zinc-700 hover:border-amber-500 text-zinc-200'} text-xs transition-colors" data-action-vote-battle="${battle.id}" data-track-target="${battle.trackA.id}">
                ${battle.userVotedSong === battle.trackA.id ? 'Voted' : 'Vote for ' + battle.trackA.title}
              </button>
            </div>

            <!-- Track B -->
            <div class="relative overflow-hidden rounded-xl border ${battle.userVotedSong === battle.trackB.id ? 'border-amber-500 bg-amber-500/10' : 'border-zinc-800 bg-zinc-950/80'} p-4 flex flex-col justify-between transition-all">
              <div class="flex items-center gap-3 mb-4">
                <img src="${battle.trackB.coverArt}" alt="${battle.trackB.title}" class="w-12 h-12 rounded-lg object-cover">
                <div>
                  <h4 class="text-sm font-bold text-zinc-100">${battle.trackB.title}</h4>
                  <p class="text-xs text-zinc-400">${battle.trackB.album}</p>
                </div>
              </div>

              ${hasVoted ? `
                <div class="mb-3">
                  <div class="flex justify-between text-xs mb-1 font-mono">
                    <span class="text-zinc-400">${battle.trackB.votes} votes</span>
                    <span class="text-amber-400 font-bold">${battle.trackB.percentage}%</span>
                  </div>
                  <div class="h-2 rounded-full bg-zinc-800 overflow-hidden">
                    <div class="h-full bg-amber-500" style="width: ${battle.trackB.percentage}%"></div>
                  </div>
                </div>
              ` : ''}

              <button class="w-full py-2.5 rounded-xl border ${battle.userVotedSong === battle.trackB.id ? 'bg-amber-500 text-black font-bold' : 'border-zinc-700 hover:border-amber-500 text-zinc-200'} text-xs transition-colors" data-action-vote-battle="${battle.id}" data-track-target="${battle.trackB.id}">
                ${battle.userVotedSong === battle.trackB.id ? 'Voted' : 'Vote for ' + battle.trackB.title}
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');

    JustBaddoUI.refreshIcons();
  },

  renderQuizOverview() {
    const container = document.getElementById('jb-arena-quiz-card');
    if (!container) return;

    const quiz = JUSTBADDO_ARENA.quizzes[0];
    if (!quiz) return;

    container.innerHTML = `
      <div class="p-6 rounded-2xl border border-zinc-800 bg-zinc-900/60">
        <div class="flex items-center justify-between mb-4">
          <span class="text-xs uppercase tracking-wider font-bold text-amber-500">Verified Trivia Challenge</span>
          <span class="text-xs px-2.5 py-0.5 rounded-full bg-zinc-800 text-zinc-300 font-medium">+${quiz.pointsReward} Points</span>
        </div>
        <h3 class="text-xl font-bold text-zinc-100 mb-2">${quiz.title}</h3>
        <p class="text-sm text-zinc-400 mb-6">${quiz.subtitle}</p>

        <div class="flex items-center gap-6 text-xs text-zinc-400 mb-6">
          <div class="flex items-center gap-2">
            <i data-lucide="help-circle" class="w-4 h-4 text-amber-500"></i>
            <span>${quiz.questions.length} Questions</span>
          </div>
          <div class="flex items-center gap-2">
            <i data-lucide="award" class="w-4 h-4 text-amber-500"></i>
            <span>${quiz.difficulty} Level</span>
          </div>
          <div class="flex items-center gap-2">
            <i data-lucide="check-circle" class="w-4 h-4 text-amber-500"></i>
            <span>Verified Sources</span>
          </div>
        </div>

        <button class="px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-sm transition-colors flex items-center gap-2" id="jb-start-quiz-btn">
          <span>Start Challenge</span>
          <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </button>
      </div>
    `;

    JustBaddoUI.refreshIcons();
  },

  startQuiz(quizId = 'quiz-01') {
    const quiz = JUSTBADDO_ARENA.quizzes.find(q => q.id === quizId) || JUSTBADDO_ARENA.quizzes[0];
    this.activeQuizState = {
      quiz: quiz,
      currentQuestionIndex: 0,
      score: 0,
      selectedOption: null,
      isAnswered: false
    };

    JustBaddoUI.openModal('jb-quiz-runner-modal');
    this.renderCurrentQuestion();
  },

  renderCurrentQuestion() {
    const modalContent = document.getElementById('jb-quiz-runner-content');
    if (!modalContent) return;

    const { quiz, currentQuestionIndex, score, isAnswered, selectedOption } = this.activeQuizState;
    const question = quiz.questions[currentQuestionIndex];
    const totalQuestions = quiz.questions.length;

    // Check if completed
    if (currentQuestionIndex >= totalQuestions) {
      modalContent.innerHTML = `
        <div class="text-center py-6">
          <div class="w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center mx-auto mb-4">
            <i data-lucide="trophy" class="w-8 h-8"></i>
          </div>
          <h3 class="text-2xl font-bold text-zinc-100 mb-1">Challenge Completed!</h3>
          <p class="text-sm text-zinc-400 mb-6">You scored <span class="text-amber-400 font-bold">${score}</span> out of <span class="font-bold text-white">${totalQuestions}</span></p>

          <div class="p-4 rounded-xl bg-zinc-950 border border-zinc-800 text-xs text-zinc-300 mb-6 max-w-sm mx-auto">
            ${score === totalQuestions ? 'Flawless performance! You know your Baddo discography inside and out.' : 'Great effort! Review the catalogue and try again to climb the leaderboard.'}
          </div>

          <button class="px-6 py-2.5 rounded-xl bg-amber-500 text-black font-bold text-sm hover:bg-amber-400 transition-colors" data-modal-close>
            Close & Collect Points
          </button>
        </div>
      `;
      JustBaddoUI.refreshIcons();
      return;
    }

    modalContent.innerHTML = `
      <div class="mb-4">
        <div class="flex items-center justify-between text-xs text-zinc-400 mb-2">
          <span>Question ${currentQuestionIndex + 1} of ${totalQuestions}</span>
          <span class="font-mono text-amber-500 font-semibold">Score: ${score}</span>
        </div>
        <div class="h-1.5 rounded-full bg-zinc-800 overflow-hidden mb-6">
          <div class="h-full bg-amber-500 transition-all duration-300" style="width: ${((currentQuestionIndex) / totalQuestions) * 100}%"></div>
        </div>

        <h3 class="text-lg font-bold text-zinc-100 mb-6 leading-snug">${question.question}</h3>

        <div class="space-y-3 mb-6">
          ${question.options.map((opt, idx) => {
            let btnClass = 'border-zinc-800 hover:border-zinc-700 bg-zinc-950/70 text-zinc-200';
            if (isAnswered) {
              if (idx === question.correctIndex) {
                btnClass = 'border-emerald-500 bg-emerald-500/20 text-emerald-300 font-semibold';
              } else if (idx === selectedOption) {
                btnClass = 'border-rose-500 bg-rose-500/20 text-rose-300';
              } else {
                btnClass = 'border-zinc-900 bg-zinc-950/40 text-zinc-600 opacity-60';
              }
            }
            return `
              <button class="w-full text-left p-3.5 rounded-xl border text-xs transition-all ${btnClass}" data-action-quiz-answer="${idx}" ${isAnswered ? 'disabled' : ''}>
                <div class="flex items-center justify-between">
                  <span>${opt}</span>
                  ${isAnswered && idx === question.correctIndex ? '<i data-lucide="check" class="w-4 h-4 text-emerald-400"></i>' : ''}
                  ${isAnswered && idx === selectedOption && idx !== question.correctIndex ? '<i data-lucide="x" class="w-4 h-4 text-rose-400"></i>' : ''}
                </div>
              </button>
            `;
          }).join('')}
        </div>

        ${isAnswered ? `
          <div class="p-4 rounded-xl bg-zinc-950 border border-zinc-800 mb-6 text-xs leading-relaxed text-zinc-300 animate-fadeIn">
            <span class="font-semibold text-amber-400 block mb-1">Source Fact:</span>
            ${question.explanation}
          </div>

          <button class="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs transition-colors flex items-center justify-center gap-2" id="jb-quiz-next-btn">
            <span>Next Question</span>
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </button>
        ` : ''}
      </div>
    `;

    JustBaddoUI.refreshIcons();
  },

  renderLeaderboard() {
    const container = document.getElementById('jb-arena-leaderboard');
    if (!container) return;

    container.innerHTML = JUSTBADDO_ARENA.leaderboard.map(item => {
      return `
        <div class="flex items-center justify-between p-3.5 rounded-xl border border-zinc-800/60 bg-zinc-900/40 hover:bg-zinc-800/40 transition-colors">
          <div class="flex items-center gap-3">
            <div class="w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs ${item.rank === 1 ? 'bg-amber-500 text-black' : item.rank === 2 ? 'bg-zinc-400 text-black' : item.rank === 3 ? 'bg-amber-800 text-amber-200' : 'bg-zinc-800 text-zinc-400'}">
              ${item.rank}
            </div>
            <img src="${item.avatar}" alt="${item.name}" class="w-9 h-9 rounded-full object-cover border border-zinc-700">
            <div>
              <div class="flex items-center gap-2">
                <h4 class="text-xs font-semibold text-zinc-200">${item.name}</h4>
                <span class="text-[10px] text-amber-400/90 font-mono">${item.badge}</span>
              </div>
              <p class="text-[11px] text-zinc-500">${item.handle}</p>
            </div>
          </div>
          <div class="text-right">
            <span class="text-xs font-mono font-bold text-zinc-100">${item.points.toLocaleString()}</span>
            <span class="block text-[10px] text-zinc-500">pts</span>
          </div>
        </div>
      `;
    }).join('');

    JustBaddoUI.refreshIcons();
  },

  bindEvents() {
    document.addEventListener('click', (e) => {
      // Vote in Poll
      const pollVoteBtn = e.target.closest('[data-action-vote-poll]');
      if (pollVoteBtn) {
        const pollId = pollVoteBtn.getAttribute('data-action-vote-poll');
        const optId = pollVoteBtn.getAttribute('data-option-id');
        const poll = JUSTBADDO_ARENA.polls.find(p => p.id === pollId);
        if (poll) {
          poll.hasVoted = true;
          poll.userVotedOption = optId;
          poll.totalVotes += 1;
          const opt = poll.options.find(o => o.id === optId);
          if (opt) opt.votes += 1;
          poll.options.forEach(o => {
            o.percentage = Math.round((o.votes / poll.totalVotes) * 100);
          });
          this.renderPolls();
          JustBaddoUI.toast('Vote recorded!', 'success');
        }
        return;
      }

      // Vote in Song Battle
      const battleVoteBtn = e.target.closest('[data-action-vote-battle]');
      if (battleVoteBtn) {
        const battleId = battleVoteBtn.getAttribute('data-action-vote-battle');
        const trackTarget = battleVoteBtn.getAttribute('data-track-target');
        const battle = JUSTBADDO_ARENA.battles.find(b => b.id === battleId);
        if (battle) {
          battle.hasVoted = true;
          battle.userVotedSong = trackTarget;
          battle.totalVotes += 1;
          if (battle.trackA.id === trackTarget) {
            battle.trackA.votes += 1;
          } else {
            battle.trackB.votes += 1;
          }
          battle.trackA.percentage = Math.round((battle.trackA.votes / battle.totalVotes) * 100);
          battle.trackB.percentage = 100 - battle.trackA.percentage;
          this.renderBattles();
          JustBaddoUI.toast('Battle vote recorded!', 'success');
        }
        return;
      }

      // Start Quiz button
      if (e.target.closest('#jb-start-quiz-btn')) {
        this.startQuiz();
        return;
      }

      // Select quiz answer
      const quizAnswerBtn = e.target.closest('[data-action-quiz-answer]');
      if (quizAnswerBtn && !this.activeQuizState.isAnswered) {
        const selectedIdx = parseInt(quizAnswerBtn.getAttribute('data-action-quiz-answer'), 10);
        const { quiz, currentQuestionIndex } = this.activeQuizState;
        const currentQ = quiz.questions[currentQuestionIndex];

        this.activeQuizState.isAnswered = true;
        this.activeQuizState.selectedOption = selectedIdx;

        if (selectedIdx === currentQ.correctIndex) {
          this.activeQuizState.score += 1;
          JustBaddoUI.toast('Correct answer! +30 Points', 'success');
        } else {
          JustBaddoUI.toast('Incorrect. Read the verified fact below.', 'info');
        }

        this.renderCurrentQuestion();
        return;
      }

      // Next quiz question
      if (e.target.closest('#jb-quiz-next-btn')) {
        this.activeQuizState.currentQuestionIndex += 1;
        this.activeQuizState.isAnswered = false;
        this.activeQuizState.selectedOption = null;
        this.renderCurrentQuestion();
        return;
      }
    });
  }
};
