/**
 * JUSTBADDO — Global Search & Filter Page
 * Live querying across catalogue tracks, studio albums, and community discussions.
 */

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('jb-search-page-input');
  const queryDisplay = document.getElementById('jb-search-query-display');
  const tracksContainer = document.getElementById('jb-search-tracks-results');
  const albumsContainer = document.getElementById('jb-search-albums-results');
  const postsContainer = document.getElementById('jb-search-posts-results');
  const emptyState = document.getElementById('jb-search-empty-state');
  const resultsContainer = document.getElementById('jb-search-results-section');

  const urlParams = new URLSearchParams(window.location.search);
  let currentQuery = urlParams.get('q') || '';

  if (searchInput && currentQuery) {
    searchInput.value = currentQuery;
  }

  function executeSearch() {
    const q = currentQuery.trim().toLowerCase();
    if (queryDisplay) {
      queryDisplay.textContent = q ? `"${q}"` : 'All Content';
    }

    if (!q) {
      if (emptyState) emptyState.classList.remove('hidden');
      if (resultsContainer) resultsContainer.classList.add('hidden');
      return;
    }

    if (emptyState) emptyState.classList.add('hidden');
    if (resultsContainer) resultsContainer.classList.remove('hidden');

    // 1. Search Tracks
    const allTracks = JUSTBADDO_CATALOGUE.getAllPlayableTracks();
    const matchedTracks = allTracks.filter(t => 
      t.title.toLowerCase().includes(q) ||
      (t.featured && t.featured.toLowerCase().includes(q)) ||
      (t.producer && t.producer.toLowerCase().includes(q)) ||
      (t.albumTitle && t.albumTitle.toLowerCase().includes(q))
    );

    if (tracksContainer) {
      if (matchedTracks.length === 0) {
        tracksContainer.innerHTML = '<p class="text-xs text-zinc-500 py-2">No tracks matched your query.</p>';
      } else {
        tracksContainer.innerHTML = matchedTracks.map(t => `
          <div class="flex items-center justify-between p-3 rounded-xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition-all group">
            <div class="flex items-center gap-3 min-w-0">
              <button class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 group-hover:bg-amber-500 group-hover:text-black flex items-center justify-center transition-colors shrink-0" data-play-track-id="${t.id}">
                <i data-lucide="play" class="w-4 h-4 fill-current"></i>
              </button>
              <div class="min-w-0">
                <a href="track.html?id=${t.id}" class="text-sm font-semibold text-zinc-100 group-hover:text-amber-400 transition-colors truncate block">${t.title}</a>
                <span class="text-xs text-zinc-400 truncate block">${t.featured ? `ft. ${t.featured} • ` : ''}${t.albumTitle || 'Catalogue'}</span>
              </div>
            </div>
            <div class="flex items-center gap-3 shrink-0">
              <span class="text-xs text-zinc-500 font-mono">${t.duration}</span>
              <button class="text-zinc-500 hover:text-amber-400 p-1" data-action-add-to-playlist="${t.id}">
                <i data-lucide="plus" class="w-4 h-4"></i>
              </button>
            </div>
          </div>
        `).join('');
      }
    }

    // 2. Search Albums
    const matchedAlbums = JUSTBADDO_CATALOGUE.albums.filter(a =>
      a.title.toLowerCase().includes(q) ||
      a.description.toLowerCase().includes(q) ||
      (a.featuredArtists && a.featuredArtists.some(f => f.toLowerCase().includes(q))) ||
      (a.producers && a.producers.some(p => p.toLowerCase().includes(q)))
    );

    if (albumsContainer) {
      if (matchedAlbums.length === 0) {
        albumsContainer.innerHTML = '<p class="text-xs text-zinc-500 py-2">No albums matched your query.</p>';
      } else {
        albumsContainer.innerHTML = matchedAlbums.map(a => `
          <a href="album.html?slug=${a.slug}" class="group p-3 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition-all flex items-center gap-3.5">
            <img src="${a.coverArt}" alt="${a.title}" onerror="this.onerror=null;this.src='https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=300&q=80'" class="w-14 h-14 rounded-xl object-cover shrink-0">
            <div class="min-w-0">
              <span class="text-[10px] text-zinc-500 font-mono block">${a.releaseYear} • ${a.type}</span>
              <h4 class="text-sm font-bold text-zinc-100 group-hover:text-amber-400 transition-colors truncate">${a.title}</h4>
              <p class="text-xs text-zinc-400 line-clamp-1 mt-0.5">${a.trackCount} tracks • ${a.label}</p>
            </div>
          </a>
        `).join('');
      }
    }

    // 3. Search Community Discussions
    const matchedPosts = JUSTBADDO_COMMUNITY.posts.filter(p =>
      p.title.toLowerCase().includes(q) ||
      p.content.toLowerCase().includes(q) ||
      p.category.toLowerCase().includes(q)
    );

    if (postsContainer) {
      if (matchedPosts.length === 0) {
        postsContainer.innerHTML = '<p class="text-xs text-zinc-500 py-2">No discussions matched your query.</p>';
      } else {
        postsContainer.innerHTML = matchedPosts.map(p => `
          <div class="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition-colors">
            <div class="flex items-center justify-between text-xs text-zinc-400 mb-2">
              <span class="font-semibold text-zinc-200">${p.author.name}</span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-zinc-800">${p.category}</span>
            </div>
            <h4 class="text-sm font-bold text-zinc-100 mb-1">${p.title}</h4>
            <p class="text-xs text-zinc-400 line-clamp-2">${p.content}</p>
            <div class="mt-3 pt-2 border-t border-zinc-800/60 flex items-center justify-between text-xs">
              <span class="text-zinc-500">${p.likes} likes • ${p.commentsCount} replies</span>
              <a href="community.html" class="text-amber-400 hover:underline">View in Community</a>
            </div>
          </div>
        `).join('');
      }
    }

    JustBaddoUI.refreshIcons();
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentQuery = e.target.value;
      executeSearch();
    });
  }

  // Quick suggestion chips
  document.querySelectorAll('[data-suggestion-chip]').forEach(chip => {
    chip.addEventListener('click', () => {
      const val = chip.getAttribute('data-suggestion-chip');
      if (searchInput) {
        searchInput.value = val;
        currentQuery = val;
        executeSearch();
      }
    });
  });

  executeSearch();
});
