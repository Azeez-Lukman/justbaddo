/**
 * JUSTBADDO — Album Detail Page Script
 * Reads ?slug= from URL (defaults to 'ikigai-vol-1'), renders album details, full tracklist, and credits.
 */

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const slug = urlParams.get('slug') || 'ikigai-vol-1';

  const album = JUSTBADDO_CATALOGUE.getAlbumBySlug(slug) || JUSTBADDO_CATALOGUE.albums[0];
  if (!album) return;

  // Set Page Title
  document.title = `${album.title} — Album Discography — JUSTBADDO`;

  async function loadFromBackend() {
    if (!window.JustBaddoApi) return;
    try {
      const res = await window.JustBaddoApi.music.getAlbum(slug);
      if (res && res.data) {
        const liveAlbum = res.data;
        if (titleEl) titleEl.textContent = liveAlbum.title;
        if (descEl && liveAlbum.description) descEl.textContent = liveAlbum.description;
        if (coverImg && liveAlbum.cover_image_url) coverImg.src = liveAlbum.cover_image_url;
        if (typeEl) typeEl.textContent = `${liveAlbum.release_year} • ${liveAlbum.album_type || 'Studio Album'}`;
        
        if (tracklistContainer && liveAlbum.tracks && liveAlbum.tracks.length > 0) {
          tracklistContainer.innerHTML = liveAlbum.tracks.map((track, idx) => {
            const isPlayable = track.is_playable || track.playback_status !== 'RESTRICTED';
            const statusKey = track.playback_status || 'JUSTBADDO_STREAMING';
            const statusObj = JUSTBADDO_CATALOGUE.playbackStatuses[statusKey] || JUSTBADDO_CATALOGUE.playbackStatuses.JUSTBADDO_STREAMING;
            return `
              <div class="flex items-center justify-between p-3.5 rounded-xl border border-zinc-800/60 bg-zinc-900/40 hover:bg-zinc-850 hover:border-zinc-700/80 transition-all group">
                <div class="flex items-center gap-3.5 min-w-0">
                  <span class="w-6 text-center text-xs font-mono text-zinc-500 group-hover:hidden">${idx + 1}</span>
                  <button class="w-6 h-6 rounded-md bg-amber-500/10 text-amber-400 group-hover:flex hidden items-center justify-center transition-colors" data-play-track-id="${track.id}" title="Play Track">
                    <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
                  </button>
                  <div class="min-w-0">
                    <a href="track.html?id=${track.id}" class="text-sm font-semibold text-zinc-200 group-hover:text-amber-400 transition-colors truncate block">${track.title}</a>
                    <span class="text-xs text-zinc-500 truncate block">${track.featured_artists || track.primary_artist_name || 'Olamide'} • Prod: ${track.producer || 'YBNL'}</span>
                  </div>
                </div>
                <div class="flex items-center gap-4 text-xs">
                  <span class="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full border ${statusObj.badgeClass}">${statusObj.label}</span>
                  <span class="text-zinc-500 font-mono">${track.duration_seconds ? `${Math.floor(track.duration_seconds/60)}:${(track.duration_seconds%60).toString().padStart(2, '0')}` : '3:00'}</span>
                  <button class="text-zinc-500 hover:text-amber-400 p-1" data-action-add-to-playlist="${track.id}">
                    <i data-lucide="plus" class="w-4 h-4"></i>
                  </button>
                </div>
              </div>
            `;
          }).join('');
          JustBaddoUI.refreshIcons();
        }
      }
    } catch (e) {
      // Keep local catalogue fallback
    }
  }

  loadFromBackend();

  // Render Header Details
  const coverImg = document.getElementById('jb-album-cover');
  if (coverImg) {
    coverImg.onerror = () => { coverImg.src = 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=600&q=80'; };
    coverImg.src = album.coverArt;
  }

  const titleEl = document.getElementById('jb-album-title');
  if (titleEl) titleEl.textContent = album.title;

  const typeEl = document.getElementById('jb-album-type');
  if (typeEl) typeEl.textContent = `${album.releaseYear} • ${album.type}`;

  const metaEl = document.getElementById('jb-album-meta');
  if (metaEl) {
    metaEl.innerHTML = `
      <span>${album.trackCount} Tracks</span>
      <span>•</span>
      <span>${album.duration} Total Time</span>
      <span>•</span>
      <span>${album.label}</span>
    `;
  }

  const descEl = document.getElementById('jb-album-desc');
  if (descEl) descEl.textContent = album.description;

  // Bind Play All Button
  const playAllBtn = document.getElementById('jb-album-play-all-btn');
  if (playAllBtn) {
    playAllBtn.setAttribute('data-play-album-id', album.id);
  }

  // Render Tracklist
  const tracklistContainer = document.getElementById('jb-album-tracklist');
  if (tracklistContainer && album.tracks) {
    tracklistContainer.innerHTML = album.tracks.map((track, idx) => {
      const statusObj = JUSTBADDO_CATALOGUE.playbackStatuses[track.status] || JUSTBADDO_CATALOGUE.playbackStatuses.JUSTBADDO_STREAMING;
      const isPlayable = track.isPlayable;

      return `
        <div class="flex items-center justify-between p-3.5 rounded-xl border border-zinc-800/60 bg-zinc-900/40 hover:bg-zinc-850 hover:border-zinc-700/80 transition-all group">
          <div class="flex items-center gap-3.5 min-w-0">
            <span class="w-6 text-center text-xs font-mono text-zinc-500 group-hover:hidden">${idx + 1}</span>
            <button class="w-6 h-6 rounded-md bg-amber-500/10 text-amber-400 group-hover:flex hidden items-center justify-center transition-colors" data-play-track-id="${track.id}" title="Play Track">
              <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
            </button>
            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <a href="track.html?id=${track.id}" class="text-sm font-semibold text-zinc-200 group-hover:text-amber-400 transition-colors truncate">${track.title}</a>
                <span class="text-[9px] px-2 py-0.5 rounded-full border ${statusObj.badgeClass}">${statusObj.label}</span>
              </div>
              <p class="text-xs text-zinc-400 truncate">
                ${track.featured ? `ft. ${track.featured} • ` : ''}Prod. ${track.producer || 'YBNL'}
              </p>
            </div>
          </div>
          <div class="flex items-center gap-4 text-xs shrink-0">
            <span class="text-zinc-500 font-mono">${track.duration}</span>
            <button class="text-zinc-500 hover:text-amber-400 p-1" data-action-add-to-playlist="${track.id}" title="Add to Playlist">
              <i data-lucide="plus" class="w-4 h-4"></i>
            </button>
          </div>
        </div>
      `;
    }).join('');
  }

  // Render Credits Box
  const creditsContainer = document.getElementById('jb-album-credits');
  if (creditsContainer) {
    creditsContainer.innerHTML = `
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
        <div class="p-4 rounded-xl bg-zinc-950/60 border border-zinc-800/80">
          <span class="text-zinc-500 block text-[10px] uppercase font-bold tracking-wider mb-1">Executive Producer</span>
          <span class="font-semibold text-zinc-200">Olamide Adedeji</span>
        </div>
        <div class="p-4 rounded-xl bg-zinc-950/60 border border-zinc-800/80">
          <span class="text-zinc-500 block text-[10px] uppercase font-bold tracking-wider mb-1">Key Producers</span>
          <span class="font-semibold text-zinc-200">${album.producers ? album.producers.join(', ') : 'Pheelz, Young Jonn'}</span>
        </div>
        <div class="p-4 rounded-xl bg-zinc-950/60 border border-zinc-800/80">
          <span class="text-zinc-500 block text-[10px] uppercase font-bold tracking-wider mb-1">Record Label</span>
          <span class="font-semibold text-zinc-200">${album.label}</span>
        </div>
        <div class="p-4 rounded-xl bg-zinc-950/60 border border-zinc-800/80">
          <span class="text-zinc-500 block text-[10px] uppercase font-bold tracking-wider mb-1">Distributor</span>
          <span class="font-semibold text-zinc-200">${album.distributor || 'EMPIRE / YBNL'}</span>
        </div>
      </div>
    `;
  }

  // Render Related Albums
  const relatedContainer = document.getElementById('jb-related-albums');
  if (relatedContainer) {
    const otherAlbums = JUSTBADDO_CATALOGUE.albums.filter(a => a.id !== album.id).slice(0, 4);
    relatedContainer.innerHTML = otherAlbums.map(rel => `
      <a href="album.html?slug=${rel.slug}" class="group p-3 rounded-xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition-all flex items-center gap-3">
        <img src="${rel.coverArt}" alt="${rel.title}" onerror="this.onerror=null;this.src='https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=300&q=80'" class="w-12 h-12 rounded-lg object-cover shrink-0">
        <div class="min-w-0">
          <h5 class="text-xs font-bold text-zinc-200 group-hover:text-amber-400 transition-colors truncate">${rel.title}</h5>
          <span class="text-[11px] text-zinc-500">${rel.releaseYear} • ${rel.type}</span>
        </div>
      </a>
    `).join('');
  }

  JustBaddoUI.refreshIcons();
});
