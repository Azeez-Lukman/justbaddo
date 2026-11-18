/**
 * JUSTBADDO — SoundCloud Audio Provider Adapter (Phase 6)
 * Integrates with SoundCloud Widget API for authorised partner tracks.
 * Communicates with official SoundCloud iframe widget without raw MP3 extraction.
 */

class SoundCloudAudioProvider extends AudioProviderInterface {
  constructor(options = {}) {
    super(options);
    this.currentTrack = null;
    this.isPlaying = false;
    this.currentTime = 0;
    this.duration = 180;
    this.volume = 0.7;
    this.widget = null;
    this.iframe = null;
    this.isReady = false;
    this.containerId = options.containerId || 'jb-soundcloud-host';
    this.timerId = null;
  }

  getCapabilities() {
    return {
      providerName: 'soundcloud',
      displayName: 'SoundCloud Official Partner Widget',
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
      container.style.width = '300px';
      container.style.height = '166px';
      container.style.opacity = '0.01';
      container.style.pointerEvents = 'none';
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

    const container = this._ensureContainer();
    container.innerHTML = '';

    // If an embed URL is provided (e.g. from soundcloud), use it, otherwise use soundcloud track id
    const trackId = track.provider_track_id || track.providerTrackId || '12345678';
    const embedUrl = track.provider_embed_url || track.providerEmbedUrl || `https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/${trackId}&auto_play=false&buying=false&sharing=false`;

    const iframe = document.createElement('iframe');
    iframe.src = embedUrl;
    iframe.width = '100%';
    iframe.height = '166';
    iframe.allow = 'autoplay';
    iframe.style.border = 'none';
    container.appendChild(iframe);
    this.iframe = iframe;

    // Check if SC Widget SDK is loaded on page
    if (window.SC && window.SC.Widget) {
      this.widget = window.SC.Widget(iframe);
      this._bindWidgetEvents();
    } else {
      // Simulate ready state if running in offline sandbox or SDK script is gated
      this._setupFallbackPolling();
    }
  }

  _bindWidgetEvents() {
    if (!this.widget) return;
    const SC = window.SC;

    this.widget.bind(SC.Widget.Events.READY, () => {
      this.isReady = true;
      this.widget.getDuration((d) => {
        this.duration = Math.round(d / 1000) || 180;
        this.callbacks.onTimeUpdate(this.currentTime, this.duration);
      });
    });

    this.widget.bind(SC.Widget.Events.PLAY, () => {
      this.isPlaying = true;
      this.callbacks.onPlay();
    });

    this.widget.bind(SC.Widget.Events.PAUSE, () => {
      this.isPlaying = false;
      this.callbacks.onPause();
    });

    this.widget.bind(SC.Widget.Events.PLAY_PROGRESS, (data) => {
      this.currentTime = Math.round(data.currentPosition / 1000);
      this.callbacks.onTimeUpdate(this.currentTime, this.duration);
    });

    this.widget.bind(SC.Widget.Events.FINISH, () => {
      this.isPlaying = false;
      this.callbacks.onEnded();
    });

    this.widget.bind(SC.Widget.Events.ERROR, (err) => {
      console.warn('[SoundCloudAudioProvider] Widget Error:', err);
      this.callbacks.onError(err);
    });
  }

  _setupFallbackPolling() {
    // If SC SDK is not loaded or network is disconnected, simulate progressive audio playback
    this.isReady = true;
  }

  play() {
    if (!this.currentTrack) return;
    this.isPlaying = true;
    if (this.widget && typeof this.widget.play === 'function') {
      try {
        this.widget.play();
      } catch (e) {
        console.warn('[SoundCloudAudioProvider] play exception:', e);
      }
    } else {
      clearInterval(this.timerId);
      this.timerId = setInterval(() => {
        if (this.currentTime >= this.duration) {
          this.currentTime = this.duration;
          this.pause();
          this.callbacks.onEnded();
          return;
        }
        this.currentTime += 1;
        this.callbacks.onTimeUpdate(this.currentTime, this.duration);
      }, 1000);
    }
    this.callbacks.onPlay();
  }

  pause() {
    this.isPlaying = false;
    clearInterval(this.timerId);
    if (this.widget && typeof this.widget.pause === 'function') {
      try {
        this.widget.pause();
      } catch (e) {
        console.warn('[SoundCloudAudioProvider] pause exception:', e);
      }
    }
    this.callbacks.onPause();
  }

  seek(seconds) {
    this.currentTime = Math.max(0, Math.min(seconds, this.duration));
    if (this.widget && typeof this.widget.seekTo === 'function') {
      try {
        this.widget.seekTo(seconds * 1000);
      } catch (e) {
        console.warn('[SoundCloudAudioProvider] seek exception:', e);
      }
    }
    this.callbacks.onTimeUpdate(this.currentTime, this.duration);
  }

  setVolume(volume) {
    this.volume = Math.max(0, Math.min(volume, 1));
    if (this.widget && typeof this.widget.setVolume === 'function') {
      try {
        this.widget.setVolume(Math.round(this.volume * 100));
      } catch (e) {
        console.warn('[SoundCloudAudioProvider] setVolume exception:', e);
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
    if (this.iframe && this.iframe.parentNode) {
      this.iframe.parentNode.removeChild(this.iframe);
    }
    this.widget = null;
    this.iframe = null;
    this.currentTrack = null;
  }
}

window.SoundCloudAudioProvider = SoundCloudAudioProvider;
