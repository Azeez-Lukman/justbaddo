/**
 * JUSTBADDO — Persistent Music Player Controller
 * Orchestrates playback provider, bottom player bar, expanded player modal, and queue advancement.
 */

window.JustBaddoPlayer = {
  provider: null,

  init() {
    this.provider = new MockAudioProvider();

    // Wire callbacks from provider to central state
    this.provider.setCallbacks({
      onPlay: () => {
        JustBaddoState.setPlayerState({ isPlaying: true });
        this.updatePlayPauseUI(true);
      },
      onPause: () => {
        JustBaddoState.setPlayerState({ isPlaying: false });
        this.updatePlayPauseUI(false);
      },
      onTimeUpdate: (currentTime, duration) => {
        this.updateProgressUI(currentTime, duration);
      },
      onEnded: () => {
        this.next(true); // advance to next track
      },
      onError: (err) => {
        console.error('[JustBaddoPlayer] Error:', err);
        JustBaddoUI.toast('Unable to play track in demonstration mode', 'error');
      }
    });

    // Listen to state events
    JustBaddoState.on('track-play-requested', (track) => {
      this.playTrack(track);
    });

    JustBaddoState.on('saved-tracks-updated', () => {
      this.updateLikeButtonUI();
    });

    // Check if state already has a track to load
    const currentTrack = JustBaddoState.state.player.currentTrack;
    if (currentTrack) {
      this.loadTrack(currentTrack, false);
    }

    this.bindDOMEvents();
    this.updateLikeButtonUI();
  },

  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  },

  loadTrack(track, autoPlay = true) {
    if (!track) return;
    this.provider.loadTrack(track);
    JustBaddoState.setPlayerState({ currentTrack: track, currentTime: 0, duration: this.provider.getDuration() });

    // Update Player UI elements (bottom bar + expanded modal)
    document.querySelectorAll('.jb-player-title').forEach(el => el.textContent = track.title);
    document.querySelectorAll('.jb-player-artist').forEach(el => el.textContent = track.featured ? `Olamide ft. ${track.featured}` : 'Olamide');
    document.querySelectorAll('.jb-player-album').forEach(el => el.textContent = track.albumTitle || 'Catalogue Track');
    document.querySelectorAll('.jb-player-cover').forEach(el => {
      if (el.tagName === 'IMG') {
        el.onerror = () => { el.src = 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=300&q=80'; };
        el.src = track.coverArt || track.albumCover || 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=300&q=80';
      }
    });

    // Update status badge in expanded player
    const statusObj = JUSTBADDO_CATALOGUE.playbackStatuses[track.status] || JUSTBADDO_CATALOGUE.playbackStatuses.JUSTBADDO_STREAMING;
    document.querySelectorAll('.jb-player-status-badge').forEach(el => {
      el.className = `jb-player-status-badge text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded-full border ${statusObj.badgeClass}`;
      el.textContent = statusObj.label;
    });

    this.updateProgressUI(0, this.provider.getDuration());
    this.updateLikeButtonUI();

    if (autoPlay) {
      this.play();
    }
  },

  playTrack(track) {
    if (!track.isPlayable) {
      JustBaddoUI.toast(`Track status is "${track.status}". Demonstration playback unavailable.`, 'warning');
      return;
    }
    this.loadTrack(track, true);
  },

  play() {
    const currentTrack = JustBaddoState.state.player.currentTrack;
    if (!currentTrack) {
      const firstInQueue = JustBaddoState.state.queue[0];
      if (firstInQueue) {
        this.loadTrack(firstInQueue, true);
      }
      return;
    }
    this.provider.play();
  },

  pause() {
    this.provider.pause();
  },

  togglePlay() {
    if (JustBaddoState.state.player.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  },

  seek(percentage) {
    const duration = this.provider.getDuration();
    const targetSeconds = (percentage / 100) * duration;
    this.provider.seek(targetSeconds);
  },

  setVolume(val) {
    const volume = parseFloat(val);
    this.provider.setVolume(volume);
    JustBaddoState.setPlayerState({ volume, isMuted: volume === 0 });
    document.querySelectorAll('.jb-volume-slider').forEach(el => el.value = volume);
    this.updateVolumeIcon(volume);
  },

  toggleMute() {
    const currentMute = JustBaddoState.state.player.isMuted;
    if (currentMute) {
      const vol = JustBaddoState.state.player.volume || 0.7;
      this.setVolume(vol);
      JustBaddoState.setPlayerState({ isMuted: false });
    } else {
      this.setVolume(0);
      JustBaddoState.setPlayerState({ isMuted: true });
    }
  },

  next(autoAdvance = false) {
    const queue = JustBaddoState.state.queue;
    if (!queue || queue.length === 0) return;
    const currentTrack = JustBaddoState.state.player.currentTrack;
    const currentIndex = queue.findIndex(t => t.id === (currentTrack && currentTrack.id));

    let nextIndex = 0;
    if (JustBaddoState.state.player.isShuffle) {
      nextIndex = Math.floor(Math.random() * queue.length);
    } else {
      if (currentIndex > -1 && currentIndex < queue.length - 1) {
        nextIndex = currentIndex + 1;
      } else {
        if (autoAdvance && JustBaddoState.state.player.repeatMode === 'off') {
          this.pause();
          return;
        }
        nextIndex = 0; // loop back to first
      }
    }

    const nextTrack = queue[nextIndex];
    if (nextTrack) {
      this.playTrack(nextTrack);
    }
  },

  prev() {
    const queue = JustBaddoState.state.queue;
    if (!queue || queue.length === 0) return;
    const currentTrack = JustBaddoState.state.player.currentTrack;
    const currentIndex = queue.findIndex(t => t.id === (currentTrack && currentTrack.id));

    let prevIndex = 0;
    if (currentIndex > 0) {
      prevIndex = currentIndex - 1;
    } else {
      prevIndex = queue.length - 1;
    }

    const prevTrack = queue[prevIndex];
    if (prevTrack) {
      this.playTrack(prevTrack);
    }
  },

  toggleShuffle() {
    const isShuffle = !JustBaddoState.state.player.isShuffle;
    JustBaddoState.setPlayerState({ isShuffle });
    document.querySelectorAll('.jb-player-shuffle-btn').forEach(btn => {
      btn.classList.toggle('text-amber-500', isShuffle);
      btn.classList.toggle('text-zinc-400', !isShuffle);
    });
    JustBaddoUI.toast(isShuffle ? 'Shuffle enabled' : 'Shuffle disabled', 'info');
  },

  toggleRepeat() {
    const modes = ['off', 'all', 'one'];
    const currentMode = JustBaddoState.state.player.repeatMode;
    const nextMode = modes[(modes.indexOf(currentMode) + 1) % modes.length];
    JustBaddoState.setPlayerState({ repeatMode: nextMode });

    document.querySelectorAll('.jb-player-repeat-btn').forEach(btn => {
      btn.classList.toggle('text-amber-500', nextMode !== 'off');
      btn.classList.toggle('text-zinc-400', nextMode === 'off');
      const badge = btn.querySelector('.jb-repeat-badge');
      if (badge) {
        badge.textContent = nextMode === 'one' ? '1' : '';
        badge.classList.toggle('hidden', nextMode !== 'one');
      }
    });
    JustBaddoUI.toast(`Repeat mode: ${nextMode.toUpperCase()}`, 'info');
  },

  updatePlayPauseUI(isPlaying) {
    document.querySelectorAll('.jb-play-pause-icon').forEach(el => {
      el.setAttribute('data-lucide', isPlaying ? 'pause' : 'play');
    });
    document.querySelectorAll('.jb-play-pause-btn').forEach(btn => {
      btn.setAttribute('aria-label', isPlaying ? 'Pause' : 'Play');
    });
    JustBaddoUI.refreshIcons();
  },

  updateProgressUI(currentTime, duration) {
    const percent = duration > 0 ? (currentTime / duration) * 100 : 0;
    document.querySelectorAll('.jb-player-current-time').forEach(el => el.textContent = this.formatTime(currentTime));
    document.querySelectorAll('.jb-player-duration').forEach(el => el.textContent = this.formatTime(duration));
    document.querySelectorAll('.jb-progress-bar-fill').forEach(el => el.style.width = `${percent}%`);
    document.querySelectorAll('.jb-progress-slider').forEach(el => el.value = percent);
  },

  updateVolumeIcon(vol) {
    let icon = 'volume-2';
    if (vol === 0 || JustBaddoState.state.player.isMuted) icon = 'volume-x';
    else if (vol < 0.5) icon = 'volume-1';
    document.querySelectorAll('.jb-volume-icon').forEach(el => {
      el.setAttribute('data-lucide', icon);
    });
    JustBaddoUI.refreshIcons();
  },

  updateLikeButtonUI() {
    const currentTrack = JustBaddoState.state.player.currentTrack;
    if (!currentTrack) return;
    const isLiked = JustBaddoState.isTrackSaved(currentTrack.id);
    document.querySelectorAll('.jb-player-like-btn').forEach(btn => {
      btn.classList.toggle('text-rose-500', isLiked);
      btn.classList.toggle('text-zinc-400', !isLiked);
      const icon = btn.querySelector('i');
      if (icon) {
        icon.setAttribute('data-lucide', isLiked ? 'heart' : 'heart');
        icon.classList.toggle('fill-rose-500', isLiked);
      }
    });
    JustBaddoUI.refreshIcons();
  },

  bindDOMEvents() {
    // Play/Pause button
    document.addEventListener('click', (e) => {
      const playPauseBtn = e.target.closest('.jb-play-pause-btn');
      if (playPauseBtn) {
        e.preventDefault();
        this.togglePlay();
        return;
      }

      // Next / Prev buttons
      if (e.target.closest('.jb-player-next-btn')) {
        e.preventDefault();
        this.next();
        return;
      }
      if (e.target.closest('.jb-player-prev-btn')) {
        e.preventDefault();
        this.prev();
        return;
      }

      // Shuffle & Repeat buttons
      if (e.target.closest('.jb-player-shuffle-btn')) {
        e.preventDefault();
        this.toggleShuffle();
        return;
      }
      if (e.target.closest('.jb-player-repeat-btn')) {
        e.preventDefault();
        this.toggleRepeat();
        return;
      }

      // Like current track
      if (e.target.closest('.jb-player-like-btn')) {
        e.preventDefault();
        const currentTrack = JustBaddoState.state.player.currentTrack;
        if (currentTrack) {
          const isSaved = JustBaddoState.toggleSaveTrack(currentTrack.id);
          JustBaddoUI.toast(isSaved ? `Added "${currentTrack.title}" to saved tracks` : `Removed "${currentTrack.title}" from saved tracks`, 'info');
        }
        return;
      }

      // Expand Player toggle
      if (e.target.closest('.jb-player-expand-btn')) {
        e.preventDefault();
        JustBaddoUI.openModal('jb-expanded-player-modal');
        return;
      }

      // Queue drawer toggle
      if (e.target.closest('.jb-player-queue-btn')) {
        e.preventDefault();
        JustBaddoUI.openModal('jb-queue-drawer');
        return;
      }

      // Click on any track card or row with data-play-track-id
      const playTrigger = e.target.closest('[data-play-track-id]');
      if (playTrigger) {
        e.preventDefault();
        const trackId = playTrigger.getAttribute('data-play-track-id');
        const track = JUSTBADDO_CATALOGUE.getTrackById(trackId);
        if (track) {
          JustBaddoState.addToQueue(track, true);
        }
        return;
      }

      // Click on album card play button
      const albumPlayTrigger = e.target.closest('[data-play-album-id]');
      if (albumPlayTrigger) {
        e.preventDefault();
        const albumId = albumPlayTrigger.getAttribute('data-play-album-id');
        const album = JUSTBADDO_CATALOGUE.getAlbumBySlug(albumId);
        if (album && album.tracks && album.tracks.length > 0) {
          const playableTracks = album.tracks.filter(t => t.isPlayable).map(t => ({
            ...t,
            albumTitle: album.title,
            albumCover: album.coverArt,
            albumSlug: album.slug
          }));
          if (playableTracks.length > 0) {
            JustBaddoState.setQueue(playableTracks);
            this.playTrack(playableTracks[0]);
            JustBaddoUI.toast(`Playing album: ${album.title}`, 'success');
          }
        }
        return;
      }
    });

    // Progress slider seeking
    document.querySelectorAll('.jb-progress-slider').forEach(slider => {
      slider.addEventListener('input', (e) => {
        this.seek(e.target.value);
      });
    });

    // Volume slider
    document.querySelectorAll('.jb-volume-slider').forEach(slider => {
      slider.addEventListener('input', (e) => {
        this.setVolume(e.target.value);
      });
    });

    // Mute toggle
    document.querySelectorAll('.jb-volume-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleMute();
      });
    });
  }
};
