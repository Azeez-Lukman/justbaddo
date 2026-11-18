/**
 * JUSTBADDO — Track Detail Page Script
 * Reads ?id= from URL (defaults to 'ikigai-02'), displays verified metadata, credits, and related tracks.
 */

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const trackId = urlParams.get('id') || 'ikigai-02';

  const track = JUSTBADDO_CATALOGUE.getTrackById(trackId) || JUSTBADDO_CATALOGUE.albums[0].tracks[0];
  if (!track) return;

  document.title = `${track.title} — Track Details — JUSTBADDO`;

  async function loadFromBackend() {
    if (!window.JustBaddoApi) return;
    try {
      const res = await window.JustBaddoApi.music.getTrack(trackId);
      if (res && res.data) {
        const liveTrack = res.data;
        if (titleEl) titleEl.textContent = liveTrack.title;
        if (artistEl) artistEl.textContent = liveTrack.featured_artists ? `Olamide ft. ${liveTrack.featured_artists}` : 'Olamide';
        if (producerEl && liveTrack.producer) producerEl.textContent = liveTrack.producer;
        if (bpmEl && liveTrack.bpm) bpmEl.textContent = `${liveTrack.bpm} BPM`;
        if (keyEl && liveTrack.musical_key) keyEl.textContent = liveTrack.musical_key;
        if (durationEl && liveTrack.duration_seconds) {
          durationEl.textContent = `${Math.floor(liveTrack.duration_seconds/60)}:${(liveTrack.duration_seconds%60).toString().padStart(2, '0')}`;
        }
      }
    } catch (e) {
      // Keep demo fallback
    }
  }

  loadFromBackend();

  // Track Cover & Titles
  const coverImg = document.getElementById('jb-track-cover');
  if (coverImg) coverImg.src = track.coverArt || track.albumCover || 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=400&q=80';

  const titleEl = document.getElementById('jb-track-title');
  if (titleEl) titleEl.textContent = track.title;

  const artistEl = document.getElementById('jb-track-artist');
  if (artistEl) artistEl.textContent = track.featured ? `Olamide ft. ${track.featured}` : 'Olamide';

  const albumLink = document.getElementById('jb-track-album-link');
  if (albumLink) {
    albumLink.textContent = track.albumTitle || 'Catalogue Release';
    if (track.albumSlug && track.albumSlug !== 'singles') {
      albumLink.href = `album.html?slug=${track.albumSlug}`;
    } else {
      albumLink.href = 'music.html';
    }
  }

  // Playback Status Badge
  const statusObj = JUSTBADDO_CATALOGUE.playbackStatuses[track.status] || JUSTBADDO_CATALOGUE.playbackStatuses.JUSTBADDO_STREAMING;
  const statusBadge = document.getElementById('jb-track-status-badge');
  if (statusBadge) {
    statusBadge.className = `text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded-full border ${statusObj.badgeClass}`;
    statusBadge.textContent = statusObj.label;
  }

  // Bind Primary Play Button
  const playBtn = document.getElementById('jb-track-play-btn');
  if (playBtn) {
    playBtn.setAttribute('data-play-track-id', track.id);
  }

  // Bind Add to Playlist Button
  const addToPlBtn = document.getElementById('jb-track-add-pl-btn');
  if (addToPlBtn) {
    addToPlBtn.setAttribute('data-action-add-to-playlist', track.id);
  }

  // Metadata Fields
  const durationEl = document.getElementById('jb-meta-duration');
  if (durationEl) durationEl.textContent = track.duration || '3:00';

  const producerEl = document.getElementById('jb-meta-producer');
  if (producerEl) producerEl.textContent = track.producer || 'YBNL Sound Lab';

  const bpmEl = document.getElementById('jb-meta-bpm');
  if (bpmEl) bpmEl.textContent = track.bpm ? `${track.bpm} BPM` : '108 BPM';

  const keyEl = document.getElementById('jb-meta-key');
  if (keyEl) keyEl.textContent = track.key || 'A Minor';

  // Related Tracks from same project
  const relatedContainer = document.getElementById('jb-track-related-list');
  if (relatedContainer) {
    let relatedTracks = [];
    if (track.albumSlug && track.albumSlug !== 'singles') {
      const alb = JUSTBADDO_CATALOGUE.getAlbumBySlug(track.albumSlug);
      if (alb && alb.tracks) {
        relatedTracks = alb.tracks.filter(t => t.id !== track.id).slice(0, 4);
      }
    }
    if (relatedTracks.length === 0) {
      relatedTracks = JUSTBADDO_CATALOGUE.getAllPlayableTracks().slice(0, 4);
    }

    relatedContainer.innerHTML = relatedTracks.map(rt => `
      <div class="flex items-center justify-between p-3 rounded-xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition-all group">
        <div class="flex items-center gap-3 min-w-0">
          <button class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 group-hover:bg-amber-500 group-hover:text-black flex items-center justify-center transition-colors shrink-0" data-play-track-id="${rt.id}">
            <i data-lucide="play" class="w-4 h-4 fill-current"></i>
          </button>
          <div class="min-w-0">
            <a href="track.html?id=${rt.id}" class="text-xs font-semibold text-zinc-200 group-hover:text-amber-400 transition-colors truncate block">${rt.title}</a>
            <span class="text-[11px] text-zinc-500">${rt.featured ? `ft. ${rt.featured}` : 'Olamide'}</span>
          </div>
        </div>
        <span class="text-xs text-zinc-500 font-mono">${rt.duration}</span>
      </div>
    `).join('');
  }

  JustBaddoUI.refreshIcons();
});
