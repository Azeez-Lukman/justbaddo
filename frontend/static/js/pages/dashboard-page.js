/**
 * JUSTBADDO — User Dashboard Page Logic
 * Renders user stats, recently played songs, saved tracks list, and personal playlists.
 */

document.addEventListener('DOMContentLoaded', () => {
  const savedTracksContainer = document.getElementById('jb-dash-saved-tracks');
  const playlistsContainer = document.getElementById('jb-dash-playlists');
  const savedCountEl = document.getElementById('jb-dash-saved-count');

  function renderSavedTracks() {
    if (!savedTracksContainer) return;

    const savedIds = JustBaddoState.state.savedTrackIds;
    if (savedCountEl) savedCountEl.textContent = savedIds.length;

    if (!savedIds || savedIds.length === 0) {
      savedTracksContainer.innerHTML = `
        <div class="p-8 text-center text-zinc-500 border border-zinc-800 rounded-2xl">
          <i data-lucide="heart" class="w-8 h-8 mx-auto mb-2 opacity-40"></i>
          <p class="text-xs">No saved tracks yet. Click the heart icon on any song to save it here.</p>
        </div>
      `;
    } else {
      const tracks = savedIds.map(id => JUSTBADDO_CATALOGUE.getTrackById(id)).filter(Boolean);
      savedTracksContainer.innerHTML = tracks.map((track, idx) => `
        <div class="flex items-center justify-between p-3 rounded-xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition-all group">
          <div class="flex items-center gap-3.5 min-w-0">
            <span class="text-xs font-mono text-zinc-500 w-4">${idx + 1}</span>
            <button class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 group-hover:bg-amber-500 group-hover:text-black flex items-center justify-center transition-colors shrink-0" data-play-track-id="${track.id}">
              <i data-lucide="play" class="w-4 h-4 fill-current"></i>
            </button>
            <div class="min-w-0">
              <a href="track.html?id=${track.id}" class="text-sm font-semibold text-zinc-200 group-hover:text-amber-400 transition-colors truncate block">${track.title}</a>
              <span class="text-xs text-zinc-400 truncate block">${track.featured ? `ft. ${track.featured}` : (track.albumTitle || 'Olamide')}</span>
            </div>
          </div>
          <div class="flex items-center gap-4 text-xs">
            <span class="text-zinc-500 font-mono">${track.duration}</span>
            <button class="text-rose-500 hover:text-rose-400 p-1" data-remove-saved-track="${track.id}" title="Remove from saved">
              <i data-lucide="heart" class="w-4 h-4 fill-current"></i>
            </button>
          </div>
        </div>
      `).join('');
    }

    JustBaddoUI.refreshIcons();
  }

  function renderPlaylists() {
    if (!playlistsContainer) return;
    const playlists = JustBaddoState.state.userPlaylists;

    playlistsContainer.innerHTML = playlists.map(pl => `
      <a href="playlists.html" class="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800 hover:border-amber-500/50 transition-all flex items-center justify-between group">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-zinc-800 flex items-center justify-center text-amber-400 font-bold text-xs">
            ${pl.title.substring(0, 2).toUpperCase()}
          </div>
          <div>
            <h5 class="text-xs font-bold text-zinc-200 group-hover:text-amber-400 transition-colors">${pl.title}</h5>
            <span class="text-[11px] text-zinc-500">${pl.trackIds.length} tracks</span>
          </div>
        </div>
        <span class="text-xs text-amber-500 font-semibold">View →</span>
      </a>
    `).join('');

    JustBaddoUI.refreshIcons();
  }

  document.addEventListener('click', (e) => {
    const removeBtn = e.target.closest('[data-remove-saved-track]');
    if (removeBtn) {
      const trackId = removeBtn.getAttribute('data-remove-saved-track');
      JustBaddoState.toggleSaveTrack(trackId);
      renderSavedTracks();
      JustBaddoUI.toast('Track removed from saved list', 'info');
    }
  });

  JustBaddoState.on('saved-tracks-updated', () => {
    renderSavedTracks();
  });

  JustBaddoState.on('playlists-updated', () => {
    renderPlaylists();
  });

  renderSavedTracks();
  renderPlaylists();
});
