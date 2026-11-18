/**
 * JUSTBADDO — Music Provider Interface
 * Abstract contract for audio playback engines.
 * Enables interchangeable providers: Mock Provider (dev/demo),
 * Authorised Streaming Provider (Phase 5), or JustBaddo CDN (Phase 7).
 */

class AudioProviderInterface {
  constructor(options = {}) {
    this.options = options;
    this.callbacks = {
      onPlay: () => {},
      onPause: () => {},
      onTimeUpdate: (currentTime, duration) => {},
      onEnded: () => {},
      onError: (err) => {}
    };
  }

  setCallbacks(callbacks) {
    this.callbacks = { ...this.callbacks, ...callbacks };
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

  seek(seconds) {
    throw new Error('Method seek(seconds) must be implemented.');
  }

  setVolume(volume) { // 0.0 to 1.0
    throw new Error('Method setVolume(volume) must be implemented.');
  }

  getCurrentTime() {
    return 0;
  }

  getDuration() {
    return 0;
  }

  destroy() {
    // cleanup resources
  }
}

window.AudioProviderInterface = AudioProviderInterface;
