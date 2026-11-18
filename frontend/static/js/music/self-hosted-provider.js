/**
 * JUSTBADDO — Self-Hosted Licensed Audio Provider Adapter (Phase 6/7)
 * Implements HTML5 Audio delivery for directly licensed master recordings.
 * Connects to private CDN / HLS delivery with signed token authentication.
 */

class SelfHostedAudioProvider extends AudioProviderInterface {
  constructor(options = {}) {
    super(options);
    this.currentTrack = null;
    this.audioElement = new Audio();
    this.isPlaying = false;
    this.currentTime = 0;
    this.duration = 180;
    this.volume = 0.7;
    this._bindAudioEvents();
  }

  getCapabilities() {
    return {
      providerName: 'self_hosted',
      displayName: 'JustBaddo Direct Licensed CDN Stream',
      canSeek: true,
      canChangeVolume: true,
      supportsHeadless: true,
      requiresUserGesture: false,
      isAuthorizedStream: true
    };
  }

  getState() {
    if (!this.currentTrack) return 'IDLE';
    if (this.audioElement.seeking || this.audioElement.readyState < 3) return 'BUFFERING';
    return this.isPlaying ? 'PLAYING' : 'PAUSED';
  }

  _bindAudioEvents() {
    const a = this.audioElement;
    a.addEventListener('play', () => {
      this.isPlaying = true;
      this.callbacks.onPlay();
    });

    a.addEventListener('pause', () => {
      this.isPlaying = false;
      this.callbacks.onPause();
    });

    a.addEventListener('timeupdate', () => {
      this.currentTime = Math.round(a.currentTime);
      this.duration = Math.round(a.duration) || this.duration;
      this.callbacks.onTimeUpdate(this.currentTime, this.duration);
    });

    a.addEventListener('waiting', () => {
      this.callbacks.onBuffering();
    });

    a.addEventListener('ended', () => {
      this.isPlaying = false;
      this.callbacks.onEnded();
    });

    a.addEventListener('error', (e) => {
      console.warn('[SelfHostedAudioProvider] HTML5 Audio Error:', e);
      this.callbacks.onError(e);
    });
  }

  loadTrack(track) {
    this.pause();
    this.currentTrack = track;
    this.currentTime = 0;

    // Use signed streaming URL if available, or provider URL
    const streamUrl = track.stream_url || track.streamUrl || track.provider_embed_url || '';
    if (streamUrl) {
      this.audioElement.src = streamUrl;
      this.audioElement.load();
    } else {
      // In development without direct master files, prepare fallback
      this.duration = 180;
    }
  }

  play() {
    if (!this.currentTrack) return;
    if (this.audioElement.src) {
      this.audioElement.play().catch(e => {
        console.warn('[SelfHostedAudioProvider] Play rejected:', e);
        this.callbacks.onError(e);
      });
    } else {
      this.isPlaying = true;
      this.callbacks.onPlay();
    }
  }

  pause() {
    this.isPlaying = false;
    if (this.audioElement.src) {
      this.audioElement.pause();
    }
    this.callbacks.onPause();
  }

  seek(seconds) {
    this.currentTime = Math.max(0, Math.min(seconds, this.duration));
    if (this.audioElement.src) {
      this.audioElement.currentTime = this.currentTime;
    }
    this.callbacks.onTimeUpdate(this.currentTime, this.duration);
  }

  setVolume(volume) {
    this.volume = Math.max(0, Math.min(volume, 1));
    this.audioElement.volume = this.volume;
  }

  getCurrentTime() {
    return this.currentTime;
  }

  getDuration() {
    return this.duration;
  }

  destroy() {
    this.pause();
    this.audioElement.src = '';
    this.currentTrack = null;
  }
}

window.SelfHostedAudioProvider = SelfHostedAudioProvider;
