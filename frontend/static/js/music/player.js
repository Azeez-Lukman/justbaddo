/**
 * JUSTBADDO — Persistent Music Player Controller
 * Orchestrates playback provider, bottom player bar, expanded player modal, and queue advancement.
 */

window.JustBaddoPlayer = {
  provider: null,
  currentSessionId: null,

  init() {
    this.provider = new AudioProviderManager();

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
      onBuffering: () => {
        document.querySelectorAll('.jb-player-status-badge').forEach(el => {
          el.textContent = 'BUFFERING...';
        });
      },
      onEnded: () => {
        const finishedTrack = JustBaddoState.state.player.currentTrack;
        if (finishedTrack && window.JustBaddoApi) {
          window.JustBaddoApi.playback.logPlay({
            track_id: finishedTrack.id,
            session_id: this.currentSessionId,
            duration_played: Math.round(this.provider.getDuration() || 180),
            completed: true
          }).catch(e => console.warn('[Playback Log Sync]', e.message));
        }
        this.currentSessionId = null;
        this.next(true); // advance to next track
      },
      onError: (err) => {
        console.error('[JustBaddoPlayer] Error:', err);
        JustBaddoUI.toast('Playback error. Switched to fallback audio.', 'error');
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

  updatePlayerUI(track, badgeLabel = null, badgeClass = null) {
    document.querySelectorAll('.jb-player-title').forEach(el => el.textContent = track.title);
    document.querySelectorAll('.jb-player-artist').forEach(el => el.textContent = track.featured ? `Olamide ft. ${track.featured}` : 'Olamide');
    document.querySelectorAll('.jb-player-album').forEach(el => el.textContent = track.albumTitle || 'Catalogue Track');
    document.querySelectorAll('.jb-player-cover').forEach(el => {
      if (el.tagName === 'IMG') {
        el.onerror = () => { el.src = '/static/images/defaults/default-album-cover.svg'; };
        el.src = track.coverArt || track.albumCover || '/static/images/defaults/default-album-cover.svg';
      }
    });

    if (badgeLabel) {
      document.querySelectorAll('.jb-player-status-badge').forEach(el => {
        el.className = `jb-player-status-badge text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded-full border ${badgeClass || 'border-zinc-700 bg-zinc-800 text-zinc-300'}`;
        el.textContent = badgeLabel;
      });
    }
  },

  loadTrack(track, autoPlay = true) {
    if (!track) return;

    const statusUpper = (track.status || '').toUpperCase();

    // Availability validation before attempting playback
    if (statusUpper === 'METADATA_ONLY') {
      this.updatePlayerUI(track, 'METADATA ONLY', 'border-zinc-700 bg-zinc-800 text-zinc-400');
      JustBaddoUI.toast(`"${track.title}" is a metadata-only catalogue entry. Audio is not cleared for streaming.`, 'info');
      this.updatePlayPauseUI(false);
      return;
    }
    if (statusUpper === 'RESTRICTED') {
      this.updatePlayerUI(track, 'RESTRICTED', 'border-rose-800 bg-rose-950/60 text-rose-400');
      JustBaddoUI.toast(`"${track.title}" is restricted from playback in your territory.`, 'warning');
      this.updatePlayPauseUI(false);
      return;
    }
    if (statusUpper === 'WITHDRAWN') {
      this.updatePlayerUI(track, 'WITHDRAWN', 'border-red-900 bg-red-950/80 text-red-400');
      JustBaddoUI.toast(`"${track.title}" has been withdrawn by rightsholders.`, 'warning');
      this.updatePlayPauseUI(false);
      return;
    }

    this.updatePlayerUI(track);
    this.updateProgressUI(0, this.provider.getDuration());
    this.updateLikeButtonUI();

    // Initialize backend playback session for rights validation & telemetry
    if (window.JustBaddoApi && track.id) {
      window.JustBaddoApi.playback.createSession(track.id)
        .then(res => {
          const session = (res && res.data) ? res.data : null;
          if (session && session.session_id) {
            this.currentSessionId = session.session_id;
            this.provider.loadTrack(track, session);

            // Update badge based on verified server session
            const provName = (session.provider || '').toLowerCase();
            if (session.availability_state === 'self_hosted_available') {
              this.updatePlayerUI(track, 'DIRECT LICENSED', 'border-emerald-600 bg-emerald-950/50 text-emerald-400');
            } else if (provName === 'soundcloud') {
              this.updatePlayerUI(track, 'SOUNDCLOUD PARTNER', 'border-amber-600 bg-amber-950/50 text-amber-400');
            } else if (provName === 'youtube') {
              this.updatePlayerUI(track, 'YOUTUBE OFFICIAL', 'border-red-600 bg-red-950/50 text-red-400');
            } else {
              this.updatePlayerUI(track, 'DEMO SYNTH PULSE', 'border-amber-700 bg-amber-950/40 text-amber-400');
            }
          } else {
            this.provider.loadTrack(track);
          }

          JustBaddoState.setPlayerState({ currentTrack: track, currentTime: 0, duration: this.provider.getDuration() });
          if (autoPlay) this.play();
        })
        .catch(err => {
          console.warn('[Playback Session Verification]', err);
          if (err.status === 403) {
            this.updatePlayerUI(track, 'RESTRICTED', 'border-rose-800 bg-rose-950/60 text-rose-400');
            JustBaddoUI.toast(err.message || 'Track playback is restricted.', 'warning');
            this.updatePlayPauseUI(false);
          } else {
            // Local offline fallback
            this.provider.loadTrack(track);
            JustBaddoState.setPlayerState({ currentTrack: track, currentTime: 0, duration: this.provider.getDuration() });
            if (autoPlay) this.play();
          }
        });
    } else {
      this.provider.loadTrack(track);
      JustBaddoState.setPlayerState({ currentTrack: track, currentTime: 0, duration: this.provider.getDuration() });
      if (autoPlay) this.play();
    }
  },

  playTrack(track) {
    if (!track.isPlayable && (track.status || '').toUpperCase() !== 'JUSTBADDO_STREAMING') {
      const msg = (track.status || '').toUpperCase() === 'METADATA_ONLY'
        ? `"${track.title}" is metadata-only. Audio rights not cleared.`
        : `Track status is "${track.status}". Playback restricted.`;
      JustBaddoUI.toast(msg, 'warning');
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
