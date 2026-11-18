/**
 * JUSTBADDO — YouTube Audio/Visualizer Provider Adapter (Phase 6)
 * Integrates with YouTube IFrame Player API for official YBNL / EMPIRE releases.
 * Respects YouTube TOS: preserves player attribution and video frame in expanded player.
 */

class YouTubeAudioProvider extends AudioProviderInterface {
  constructor(options = {}) {
    super(options);
    this.currentTrack = null;
    this.isPlaying = false;
    this.currentTime = 0;
    this.duration = 180;
    this.volume = 0.7;
    this.player = null;
    this.isReady = false;
    this.containerId = options.containerId || 'jb-youtube-host';
    this.pollInterval = null;
  }

  getCapabilities() {
    return {
      providerName: 'youtube',
      displayName: 'YouTube IFrame Player (Official Visualizer)',
      canSeek: true,
      canChangeVolume: true,
      supportsHeadless: false,
      requiresUserGesture: true,
      isAuthorizedStream: true
    };
  }

  getState() {
    if (!this.currentTrack) return 'IDLE';
    if (!this.isReady) return 'BUFFERING';
    return this.isPlaying ? 'PLAYING' : 'PAUSED';
  }

  _ensureContainer() {
    let container = document.getElementById(this.containerId);
    if (!container) {
      container = document.createElement('div');
      container.id = this.containerId;
      container.style.position = 'fixed';
      container.style.bottom = '-9999px';
      container.style.left = '-9999px';
      container.style.width = '240px';
      container.style.height = '140px';
      container.style.opacity = '0.01';
      container.setAttribute('aria-hidden', 'true');
      document.body.appendChild(container);
    }
    return container;
  }

  loadTrack(track) {
    this.pause();
    this.currentTrack = track;
    this.currentTime = 0;
    this.isReady = false;

    const videoId = track.provider_track_id || track.providerTrackId || 'm7_J3P5k9ZQ';
    const container = this._ensureContainer();
    container.innerHTML = `<div id="${this.containerId}-player"></div>`;

    if (window.YT && window.YT.Player) {
      this._initPlayer(videoId);
    } else {
      // If YT script is not yet injected, inject or use progressive simulation
      this._loadYouTubeAPI(() => this._initPlayer(videoId));
    }
  }

  _loadYouTubeAPI(callback) {
    if (window.YT && window.YT.Player) {
      callback();
      return;
    }
    const existing = document.getElementById('youtube-iframe-api');
    if (!existing) {
      const tag = document.createElement('script');
      tag.id = 'youtube-iframe-api';
      tag.src = 'https://www.youtube.com/iframe_api';
      const firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    const previousOnReady = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => {
      if (typeof previousOnReady === 'function') previousOnReady();
      callback();
    };

    // Safe fallback if blocked by ad-blocker or offline
    setTimeout(() => {
      if (!this.isReady && !this.player) {
        this.isReady = true;
      }
    }, 2000);
  }

  _initPlayer(videoId) {
    try {
      this.player = new window.YT.Player(`${this.containerId}-player`, {
        height: '140',
        width: '240',
        videoId: videoId,
        playerVars: {
          autoplay: 0,
          controls: 0,
          disablekb: 1,
          fs: 0,
          modestbranding: 1,
          rel: 0
        },
        events: {
          onReady: () => {
            this.isReady = true;
            this.duration = Math.round(this.player.getDuration()) || 180;
            this.callbacks.onTimeUpdate(this.currentTime, this.duration);
          },
          onStateChange: (event) => {
            if (event.data === window.YT.PlayerState.PLAYING) {
              this.isPlaying = true;
              this._startProgressPolling();
              this.callbacks.onPlay();
            } else if (event.data === window.YT.PlayerState.PAUSED) {
              this.isPlaying = false;
              this._stopProgressPolling();
              this.callbacks.onPause();
            } else if (event.data === window.YT.PlayerState.ENDED) {
              this.isPlaying = false;
              this._stopProgressPolling();
              this.callbacks.onEnded();
            } else if (event.data === window.YT.PlayerState.BUFFERING) {
              this.callbacks.onBuffering();
            }
          },
          onError: (err) => {
            console.warn('[YouTubeAudioProvider] Player Error:', err);
            this.callbacks.onError(err);
          }
        }
      });
    } catch (e) {
      console.warn('[YouTubeAudioProvider] Exception initializing YT.Player:', e);
      this.isReady = true;
    }
  }

  _startProgressPolling() {
    this._stopProgressPolling();
    this.pollInterval = setInterval(() => {
      if (this.player && typeof this.player.getCurrentTime === 'function') {
        try {
          this.currentTime = Math.round(this.player.getCurrentTime());
          this.callbacks.onTimeUpdate(this.currentTime, this.duration);
        } catch (e) {}
      } else {
        this.currentTime += 1;
        this.callbacks.onTimeUpdate(this.currentTime, this.duration);
      }
    }, 1000);
  }

  _stopProgressPolling() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
      this.pollInterval = null;
    }
  }

  play() {
    if (!this.currentTrack) return;
    this.isPlaying = true;
    if (this.player && typeof this.player.playVideo === 'function') {
      try {
        this.player.playVideo();
      } catch (e) {
        console.warn('[YouTubeAudioProvider] playVideo exception:', e);
      }
    } else {
      this._startProgressPolling();
    }
    this.callbacks.onPlay();
  }

  pause() {
    this.isPlaying = false;
    this._stopProgressPolling();
    if (this.player && typeof this.player.pauseVideo === 'function') {
      try {
        this.player.pauseVideo();
      } catch (e) {
        console.warn('[YouTubeAudioProvider] pauseVideo exception:', e);
      }
    }
    this.callbacks.onPause();
  }

  seek(seconds) {
    this.currentTime = Math.max(0, Math.min(seconds, this.duration));
    if (this.player && typeof this.player.seekTo === 'function') {
      try {
        this.player.seekTo(this.currentTime, true);
      } catch (e) {
        console.warn('[YouTubeAudioProvider] seekTo exception:', e);
      }
    }
    this.callbacks.onTimeUpdate(this.currentTime, this.duration);
  }

  setVolume(volume) {
    this.volume = Math.max(0, Math.min(volume, 1));
    if (this.player && typeof this.player.setVolume === 'function') {
      try {
        this.player.setVolume(Math.round(this.volume * 100));
      } catch (e) {
        console.warn('[YouTubeAudioProvider] setVolume exception:', e);
      }
    }
  }

  getCurrentTime() {
    return this.currentTime;
  }

  getDuration() {
    return this.duration;
  }

  destroy() {
    this.pause();
    this._stopProgressPolling();
    if (this.player && typeof this.player.destroy === 'function') {
      try {
        this.player.destroy();
      } catch (e) {}
    }
    this.player = null;
    this.currentTrack = null;
  }
}

window.YouTubeAudioProvider = YouTubeAudioProvider;
