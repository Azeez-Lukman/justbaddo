/**
 * JUSTBADDO — Playlists Page Logic
 * Renders user custom playlists, editorial playlists, and interactive playlist track inspector.
 */

document.addEventListener('DOMContentLoaded', () => {
  const userPlaylistsContainer = document.getElementById('jb-user-playlists-grid');
  const inspectorSection = document.getElementById('jb-playlist-inspector');
  const inspectorTitle = document.getElementById('jb-inspector-title');
  const inspectorDesc = document.getElementById('jb-inspector-desc');
  const inspectorTracklist = document.getElementById('jb-inspector-tracklist');
  const inspectorPlayAllBtn = document.getElementById('jb-inspector-play-all');

  let activePlaylist = null;

  function renderUserPlaylists() {
    if (!userPlaylistsContainer) return;
    const playlists = JustBaddoState.state.userPlaylists;

    if (!playlists || playlists.length === 0) {
      userPlaylistsContainer.innerHTML = `
        <div class="col-span-full py-10 text-center text-zinc-500 border border-zinc-800/80 rounded-2xl">
          <i data-lucide="folder-plus" class="w-8 h-8 mx-auto mb-2 opacity-40"></i>
          <p class="text-xs">No custom playlists created yet.</p>
        </div>
      `;
    } else {
      userPlaylistsContainer.innerHTML = playlists.map(pl => `
        <div class="p-4 rounded-2xl bg-zinc-900/60 border border-zinc-800 hover:border-amber-500/50 transition-all cursor-pointer group flex flex-col justify-between" data-inspect-playlist-id="${pl.id}">
          <div class="flex items-center gap-3.5 mb-3">
            <div class="w-12 h-12 rounded-xl bg-zinc-800 border border-zinc-700 flex items-center justify-center text-amber-400 font-bold text-sm shrink-0">
              ${pl.title.substring(0, 2).toUpperCase()}
            </div>
            <div class="min-w-0">
              <h4 class="text-sm font-bold text-zinc-200 group-hover:text-amber-400 transition-colors truncate">${pl.title}</h4>
              <p class="text-xs text-zinc-500 mt-0.5">${pl.trackIds.length} tracks</p>
            </div>
          </div>
          <p class="text-xs text-zinc-400 line-clamp-1 mb-3">${pl.description || 'Personal playlist'}</p>
          <div class="flex items-center justify-between text-xs text-zinc-500 pt-2 border-t border-zinc-800/60">
            <span>Created ${pl.createdAt}</span>
            <span class="text-amber-400 font-semibold group-hover:translate-x-1 transition-transform">Open →</span>
          </div>
        </div>
      `).join('');
    }

    JustBaddoUI.refreshIcons();
  }

  function inspectPlaylist(playlist) {
    if (!inspectorSection || !playlist) return;
    activePlaylist = playlist;

    inspectorSection.classList.remove('hidden');
    if (inspectorTitle) inspectorTitle.textContent = playlist.title;
    if (inspectorDesc) inspectorDesc.textContent = playlist.description || `${playlist.trackIds.length} curated tracks`;

    const tracks = playlist.trackIds.map(id => JUSTBADDO_CATALOGUE.getTrackById(id)).filter(Boolean);

    if (inspectorPlayAllBtn) {
      inspectorPlayAllBtn.onclick = () => {
        if (tracks.length > 0) {
          JustBaddoState.setQueue(tracks);
          JustBaddoPlayer.playTrack(tracks[0]);
          JustBaddoUI.toast(`Playing playlist "${playlist.title}"`, 'success');
        } else {
          JustBaddoUI.toast('Playlist has no tracks yet', 'info');
        }
      };
    }

    if (inspectorTracklist) {
      if (tracks.length === 0) {
        inspectorTracklist.innerHTML = `
          <div class="p-8 text-center text-zinc-500 text-xs">
            This playlist has no tracks. Add songs from any album or catalogue page!
          </div>
        `;
      } else {
        inspectorTracklist.innerHTML = tracks.map((track, idx) => `
          <div class="flex items-center justify-between p-3.5 rounded-xl border border-zinc-800/80 bg-zinc-950/60 hover:bg-zinc-900 transition-all group">
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
              <button class="text-zinc-500 hover:text-rose-400 p-1" data-remove-pl-track="${track.id}" title="Remove track">
                <i data-lucide="trash-2" class="w-4 h-4"></i>
              </button>
            </div>
          </div>
        `).join('');
      }
    }

    JustBaddoUI.refreshIcons();
    inspectorSection.scrollIntoView({ behavior: 'smooth' });
  }

  // Click on user playlist card
  document.addEventListener('click', (e) => {
    const plCard = e.target.closest('[data-inspect-playlist-id]');
    if (plCard) {
      const plId = plCard.getAttribute('data-inspect-playlist-id');
      const pl = JustBaddoState.state.userPlaylists.find(p => p.id === plId);
      if (pl) inspectPlaylist(pl);
      return;
    }

    // Click on editorial playlist
    const edCard = e.target.closest('[data-inspect-editorial-id]');
    if (edCard) {
      const edId = edCard.getAttribute('data-inspect-editorial-id');
      const ed = JUSTBADDO_CATALOGUE.playlists.find(p => p.id === edId);
      if (ed) inspectPlaylist(ed);
      return;
    }

    // Remove track from current playlist
    const removeBtn = e.target.closest('[data-remove-pl-track]');
    if (removeBtn && activePlaylist) {
      const trackId = removeBtn.getAttribute('data-remove-pl-track');
      JustBaddoState.removeTrackFromPlaylist(activePlaylist.id, trackId);
      const updated = JustBaddoState.state.userPlaylists.find(p => p.id === activePlaylist.id);
      if (updated) {
        inspectPlaylist(updated);
        renderUserPlaylists();
        JustBaddoUI.toast('Track removed from playlist', 'info');
      }
      return;
    }
  });

  JustBaddoState.on('playlists-updated', () => {
    renderUserPlaylists();
  });

  renderUserPlaylists();
  // Open first editorial playlist by default
  if (JUSTBADDO_CATALOGUE.playlists.length > 0) {
    inspectPlaylist(JUSTBADDO_CATALOGUE.playlists[0]);
  }
});
