/**
 * JUSTBADDO — Music Discovery & Catalogue Page Logic
 * Handles interactive release filtering, sorting, category switching, and track search.
 */

document.addEventListener('DOMContentLoaded', () => {
  const albumsContainer = document.getElementById('jb-music-albums-grid');
  const singlesContainer = document.getElementById('jb-music-singles-list');
  const searchInput = document.getElementById('jb-music-filter-search');
  const sortSelect = document.getElementById('jb-music-sort-select');

  let activeType = 'ALL';
  let searchQuery = '';
  let currentSort = 'year-desc';

  function renderCatalogue() {
    if (!albumsContainer) return;

    let albums = [...JUSTBADDO_CATALOGUE.albums];
    let singles = [...JUSTBADDO_CATALOGUE.singlesAndFeatures];

    // Filter by Search Query
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      albums = albums.filter(a => 
        a.title.toLowerCase().includes(q) || 
        a.description.toLowerCase().includes(q) ||
        (a.featuredArtists && a.featuredArtists.some(f => f.toLowerCase().includes(q))) ||
        (a.tracks && a.tracks.some(t => t.title.toLowerCase().includes(q)))
      );
      singles = singles.filter(s =>
        s.title.toLowerCase().includes(q) ||
        (s.featured && s.featured.toLowerCase().includes(q)) ||
        (s.producer && s.producer.toLowerCase().includes(q))
      );
    }

    // Filter by Type
    if (activeType === 'ALBUMS') {
      albums = albums.filter(a => a.type === 'Studio Album');
      singles = [];
    } else if (activeType === 'EPS') {
      albums = albums.filter(a => a.type === 'EP');
      singles = [];
    } else if (activeType === 'SINGLES') {
      albums = [];
      singles = singles.filter(s => s.type === 'Single');
    }

    // Sort
    if (currentSort === 'year-desc') {
      albums.sort((a, b) => b.releaseYear - a.releaseYear);
      singles.sort((a, b) => b.releaseYear - a.releaseYear);
    } else if (currentSort === 'year-asc') {
      albums.sort((a, b) => a.releaseYear - b.releaseYear);
      singles.sort((a, b) => a.releaseYear - b.releaseYear);
    } else if (currentSort === 'title') {
      albums.sort((a, b) => a.title.localeCompare(b.title));
      singles.sort((a, b) => a.title.localeCompare(b.title));
    }

    // Render Albums
    if (albums.length === 0 && singles.length === 0) {
      albumsContainer.innerHTML = `
        <div class="col-span-full py-16 text-center text-zinc-500">
          <i data-lucide="disc-3" class="w-12 h-12 mx-auto mb-3 opacity-40"></i>
          <p class="text-base font-semibold text-zinc-300">No releases match your filter</p>
          <p class="text-xs text-zinc-500 mt-1">Try clearing your search keyword or switching categories</p>
        </div>
      `;
    } else {
      albumsContainer.innerHTML = albums.map(album => `
        <div class="group relative rounded-2xl bg-zinc-900/70 border border-zinc-800/80 hover:border-zinc-700 p-4 transition-all duration-300 flex flex-col justify-between">
          <div class="relative aspect-square rounded-xl overflow-hidden mb-4 bg-zinc-950">
            <img src="${album.coverArt}" alt="${album.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-3">
              <button class="w-10 h-10 rounded-full bg-amber-500 hover:bg-amber-400 text-black flex items-center justify-center shadow-lg transition-transform transform hover:scale-110 ml-auto" data-play-album-id="${album.id}" title="Play Album">
                <i data-lucide="play" class="w-4 h-4 fill-current"></i>
              </button>
            </div>
          </div>
          <div>
            <div class="flex items-center justify-between text-[11px] text-zinc-500 font-mono mb-1">
              <span>${album.releaseYear}</span>
              <span class="px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-300">${album.type}</span>
            </div>
            <a href="album.html?slug=${album.slug}" class="text-sm font-bold text-zinc-100 group-hover:text-amber-400 transition-colors line-clamp-1">${album.title}</a>
            <p class="text-xs text-zinc-400 line-clamp-2 mt-1 leading-snug">${album.description}</p>
            <div class="mt-4 pt-3 border-t border-zinc-800/70 flex items-center justify-between text-xs">
              <span class="text-zinc-500">${album.trackCount} tracks</span>
              <a href="album.html?slug=${album.slug}" class="text-amber-500 hover:text-amber-400 font-semibold flex items-center gap-1">
                <span>View</span>
                <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
              </a>
            </div>
          </div>
        </div>
      `).join('');
    }

    // Render Singles
    if (singlesContainer) {
      if (singles.length === 0) {
        singlesContainer.innerHTML = `
          <div class="p-8 text-center text-zinc-500 text-xs border border-zinc-800/60 rounded-2xl">
            No singles in this view.
          </div>
        `;
      } else {
        singlesContainer.innerHTML = singles.map(s => {
          const statusObj = JUSTBADDO_CATALOGUE.playbackStatuses[s.status] || JUSTBADDO_CATALOGUE.playbackStatuses.JUSTBADDO_STREAMING;
          return `
            <div class="flex items-center justify-between p-3.5 rounded-xl border border-zinc-800/80 bg-zinc-900/50 hover:bg-zinc-850 hover:border-zinc-700 transition-all group">
              <div class="flex items-center gap-3.5 min-w-0">
                <button class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 group-hover:bg-amber-500 group-hover:text-black flex items-center justify-center transition-colors shrink-0" data-play-track-id="${s.id}">
                  <i data-lucide="play" class="w-4 h-4 fill-current"></i>
                </button>
                <div class="min-w-0">
                  <h4 class="text-sm font-semibold text-zinc-100 group-hover:text-amber-400 transition-colors truncate">${s.title}</h4>
                  <p class="text-xs text-zinc-400 truncate">${s.featured ? `ft. ${s.featured}` : (s.producer ? `Prod. ${s.producer}` : 'Olamide')}</p>
                </div>
              </div>
              <div class="flex items-center gap-3 shrink-0">
                <span class="hidden sm:inline-block text-[10px] px-2 py-0.5 rounded-full border ${statusObj.badgeClass}">${statusObj.label}</span>
                <span class="text-xs text-zinc-500 font-mono">${s.duration}</span>
                <button class="text-zinc-500 hover:text-amber-400 p-1" data-action-add-to-playlist="${s.id}" title="Add to Playlist">
                  <i data-lucide="plus" class="w-4 h-4"></i>
                </button>
              </div>
            </div>
          `;
        }).join('');
      }
    }

    JustBaddoUI.refreshIcons();
  }

  // Filter Buttons
  document.querySelectorAll('[data-music-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-music-filter]').forEach(b => {
        b.classList.remove('bg-amber-500', 'text-black', 'font-semibold');
        b.classList.add('bg-zinc-900', 'text-zinc-400', 'hover:text-white');
      });
      btn.classList.remove('bg-zinc-900', 'text-zinc-400', 'hover:text-white');
      btn.classList.add('bg-amber-500', 'text-black', 'font-semibold');
      activeType = btn.getAttribute('data-music-filter');
      renderCatalogue();
    });
  });

  // Search Input
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim();
      renderCatalogue();
    });
  }

  // Sort Select
  if (sortSelect) {
    sortSelect.addEventListener('change', (e) => {
      currentSort = e.target.value;
      renderCatalogue();
    });
  }

  // Initial render
  renderCatalogue();
});
