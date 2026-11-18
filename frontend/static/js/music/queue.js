/**
 * JUSTBADDO — Queue Controller
 * Renders and manages the active playback queue list, track removal, and queue clearing.
 */

window.JustBaddoQueue = {
  init() {
    this.renderQueue();

    JustBaddoState.on('queue-updated', () => {
      this.renderQueue();
    });

    JustBaddoState.on('player-updated', () => {
      this.updateActiveTrackHighlight();
    });

    this.bindEvents();
  },

  renderQueue() {
    const container = document.getElementById('jb-queue-list');
    if (!container) return;

    const queue = JustBaddoState.state.queue;
    const currentTrack = JustBaddoState.state.player.currentTrack;

    if (!queue || queue.length === 0) {
      container.innerHTML = `
        <div class="py-12 text-center text-zinc-500">
          <i data-lucide="music" class="w-10 h-10 mx-auto mb-3 opacity-40"></i>
          <p class="text-sm font-medium">Your queue is empty</p>
          <p class="text-xs text-zinc-600 mt-1">Add tracks from albums or discography to keep listening</p>
        </div>
      `;
      JustBaddoUI.refreshIcons();
      return;
    }

    container.innerHTML = queue.map((track, idx) => {
      const isCurrent = currentTrack && currentTrack.id === track.id;
      return `
        <div class="group flex items-center justify-between p-3 rounded-xl transition-all duration-200 ${isCurrent ? 'bg-amber-500/10 border border-amber-500/30' : 'hover:bg-zinc-800/50 border border-transparent'}">
          <div class="flex items-center gap-3 min-w-0 flex-1 cursor-pointer" data-queue-play-index="${idx}">
            <div class="relative w-10 h-10 rounded-lg overflow-hidden shrink-0 bg-zinc-800">
              <img src="${track.coverArt || track.albumCover || 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=150&q=80'}" alt="${track.title}" class="w-full h-full object-cover">
              ${isCurrent ? `
                <div class="absolute inset-0 bg-black/60 flex items-center justify-center">
                  <div class="flex items-end gap-0.5 h-3">
                    <span class="w-1 bg-amber-400 h-full animate-pulse"></span>
                    <span class="w-1 bg-amber-400 h-2/3 animate-pulse delay-75"></span>
                    <span class="w-1 bg-amber-400 h-1/2 animate-pulse delay-150"></span>
                  </div>
                </div>
              ` : ''}
            </div>
            <div class="min-w-0 flex-1">
              <h4 class="text-sm font-semibold truncate ${isCurrent ? 'text-amber-400' : 'text-zinc-200 group-hover:text-white'}">${track.title}</h4>
              <p class="text-xs text-zinc-400 truncate">${track.featured ? `ft. ${track.featured}` : (track.albumTitle || 'Olamide')}</p>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <span class="text-xs text-zinc-500 font-mono">${track.duration || '3:00'}</span>
            <button class="text-zinc-500 hover:text-rose-400 p-1.5 transition-colors opacity-0 group-hover:opacity-100" data-queue-remove-id="${track.id}" title="Remove from queue">
              <i data-lucide="trash-2" class="w-4 h-4"></i>
            </button>
          </div>
        </div>
      `;
    }).join('');

    // Update queue count badge
    document.querySelectorAll('.jb-queue-count').forEach(el => el.textContent = queue.length);

    JustBaddoUI.refreshIcons();
  },

  updateActiveTrackHighlight() {
    this.renderQueue();
  },

  bindEvents() {
    document.addEventListener('click', (e) => {
      // Play item from queue
      const playItem = e.target.closest('[data-queue-play-index]');
      if (playItem && !e.target.closest('[data-queue-remove-id]')) {
        const idx = parseInt(playItem.getAttribute('data-queue-play-index'), 10);
        const track = JustBaddoState.state.queue[idx];
        if (track) {
          JustBaddoPlayer.playTrack(track);
        }
        return;
      }

      // Remove item from queue
      const removeBtn = e.target.closest('[data-queue-remove-id]');
      if (removeBtn) {
        e.stopPropagation();
        const trackId = removeBtn.getAttribute('data-queue-remove-id');
        JustBaddoState.removeFromQueue(trackId);
        JustBaddoUI.toast('Track removed from queue', 'info');
        return;
      }

      // Clear entire queue
      if (e.target.closest('#jb-clear-queue-btn')) {
        JustBaddoState.clearQueue();
        JustBaddoUI.toast('Queue cleared', 'info');
        return;
      }
    });
  }
};
