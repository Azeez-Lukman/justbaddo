/**
 * JUSTBADDO — Playlists Controller
 * Manages user custom playlists, add-to-playlist modal, and playlist track management.
 */

window.JustBaddoPlaylists = {
  pendingTrackId: null,

  init() {
    this.bindEvents();
    this.renderAddPlaylistModalList();

    JustBaddoState.on('playlists-updated', () => {
      this.renderAddPlaylistModalList();
    });
  },

  openAddToPlaylistModal(trackId) {
    this.pendingTrackId = trackId;
    this.renderAddPlaylistModalList();
    JustBaddoUI.openModal('jb-add-to-playlist-modal');
  },

  renderAddPlaylistModalList() {
    const container = document.getElementById('jb-add-to-playlist-items');
    if (!container) return;

    const playlists = JustBaddoState.state.userPlaylists;
    if (!playlists || playlists.length === 0) {
      container.innerHTML = `
        <p class="text-sm text-zinc-500 py-4 text-center">No playlists created yet. Create your first one below.</p>
      `;
      return;
    }

    container.innerHTML = playlists.map(pl => {
      const alreadyIn = this.pendingTrackId && pl.trackIds.includes(this.pendingTrackId);
      return `
        <button class="w-full flex items-center justify-between p-3 rounded-xl border border-zinc-800 hover:border-amber-500/50 hover:bg-zinc-800/60 transition-all text-left group" data-add-target-playlist-id="${pl.id}">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-zinc-800 flex items-center justify-center text-amber-400 font-bold text-xs">
              ${pl.title.substring(0, 2).toUpperCase()}
            </div>
            <div>
              <h5 class="text-sm font-medium text-zinc-200 group-hover:text-white">${pl.title}</h5>
              <p class="text-xs text-zinc-500">${pl.trackIds.length} tracks</p>
            </div>
          </div>
          <div class="text-xs">
            ${alreadyIn ? '<span class="text-emerald-400 font-medium">Added</span>' : '<span class="text-zinc-500 group-hover:text-amber-400">+ Add</span>'}
          </div>
        </button>
      `;
    }).join('');

    JustBaddoUI.refreshIcons();
  },

  bindEvents() {
    document.addEventListener('click', (e) => {
      // Trigger "Add to playlist" button on any track
      const addToPlaylistBtn = e.target.closest('[data-action-add-to-playlist]');
      if (addToPlaylistBtn) {
        e.preventDefault();
        const trackId = addToPlaylistBtn.getAttribute('data-action-add-to-playlist');
        this.openAddToPlaylistModal(trackId);
        return;
      }

      // Select target playlist in modal
      const targetPlBtn = e.target.closest('[data-add-target-playlist-id]');
      if (targetPlBtn && this.pendingTrackId) {
        e.preventDefault();
        const playlistId = targetPlBtn.getAttribute('data-add-target-playlist-id');
        const success = JustBaddoState.addTrackToPlaylist(playlistId, this.pendingTrackId);
        const pl = JustBaddoState.state.userPlaylists.find(p => p.id === playlistId);
        if (success) {
          JustBaddoUI.toast(`Added to playlist "${pl.title}"`, 'success');
        } else {
          JustBaddoUI.toast(`Track is already in "${pl.title}"`, 'info');
        }
        JustBaddoUI.closeModal('jb-add-to-playlist-modal');
        return;
      }

      // Create new playlist form submit
      const createPlBtn = e.target.closest('#jb-create-playlist-btn');
      if (createPlBtn) {
        e.preventDefault();
        const input = document.getElementById('jb-new-playlist-title');
        const descInput = document.getElementById('jb-new-playlist-desc');
        const title = input ? input.value.trim() : '';
        const desc = descInput ? descInput.value.trim() : '';

        if (!title) {
          JustBaddoUI.toast('Please provide a playlist name', 'warning');
          return;
        }

        const newPl = JustBaddoState.createUserPlaylist(title, desc);
        if (this.pendingTrackId) {
          JustBaddoState.addTrackToPlaylist(newPl.id, this.pendingTrackId);
          JustBaddoUI.toast(`Created "${title}" and added track`, 'success');
        } else {
          JustBaddoUI.toast(`Created playlist "${title}"`, 'success');
        }

        if (input) input.value = '';
        if (descInput) descInput.value = '';
        JustBaddoUI.closeModal('jb-add-to-playlist-modal');
        JustBaddoUI.closeModal('jb-create-playlist-modal');
        return;
      }
    });
  }
};
