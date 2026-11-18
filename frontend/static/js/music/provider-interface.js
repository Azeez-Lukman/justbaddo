/**
 * JUSTBADDO — Music Provider Interface (Phase 6)
 * Abstract contract for audio playback engines.
 * Enables interchangeable providers: Mock Provider (Web Audio API Synth),
 * SoundCloud Widget API, YouTube IFrame Player API, and Self-Hosted Licensed CDN.
 */

class AudioProviderInterface {
  constructor(options = {}) {
    this.options = options;
    this.callbacks = {
      onPlay: () => {},
      onPause: () => {},
      onTimeUpdate: (currentTime, duration) => {},
      onBuffering: () => {},
      onEnded: () => {},
      onError: (err) => {},
      onStateChange: (state) => {}
    };
  }

  setCallbacks(callbacks) {
    this.callbacks = { ...this.callbacks, ...callbacks };
  }

  getCapabilities() {
    return {
      providerName: 'abstract',
      displayName: 'Abstract Provider',
      canSeek: false,
      canChangeVolume: false,
      supportsHeadless: false,
      requiresUserGesture: false,
      isAuthorizedStream: false
    };
  }

  loadTrack(track) {
    throw new Error('Method loadTrack(track) must be implemented.');
  }

  play() {
    throw new Error('Method play() must be implemented.');
  }

  pause() {
    throw new Error('Method pause() must be implemented.');
  }

  resume() {
    return this.play();
  }

  stop() {
    this.pause();
    this.seek(0);
  }

  seek(seconds) {
    throw new Error('Method seek(seconds) must be implemented.');
  }

  setVolume(volume) { // 0.0 to 1.0
    throw new Error('Method setVolume(volume) must be implemented.');
  }

  mute() {
    this.setVolume(0);
  }

  unmute(previousVolume = 0.7) {
    this.setVolume(previousVolume);
  }

  getCurrentTime() {
    return 0;
  }

  getDuration() {
    return 0;
  }

  getState() {
    return 'IDLE'; // IDLE, LOADING, PLAYING, PAUSED, BUFFERING, ERROR, ENDED
  }

  destroy() {
    // cleanup event listeners, iframes, timers
  }
}

window.AudioProviderInterface = AudioProviderInterface;
