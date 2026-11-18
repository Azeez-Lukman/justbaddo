/**
 * JUSTBADDO — Audio Provider Manager (Phase 6)
 * Orchestrates provider adapters, dynamic resolution, capabilities reporting,
 * and graceful fallback across Web Audio API Synth, SoundCloud, YouTube, and Self-Hosted CDN.
 */

class AudioProviderManager {
  constructor(options = {}) {
    this.options = options;
    this.providers = {};
    this.activeProviderName = 'web_audio_synth';
    this.activeProvider = null;
    this.currentTrack = null;
    this.callbacks = {
      onPlay: () => {},
      onPause: () => {},
      onTimeUpdate: (currentTime, duration) => {},
      onBuffering: () => {},
      onEnded: () => {},
      onError: (err) => {},
      onStateChange: (state) => {}
    };

    this._initializeProviders();
  }

  _initializeProviders() {
    // 1. Web Audio API Synth (Zero-Copyright Fallback)
    if (typeof MockAudioProvider !== 'undefined') {
      this.providers['web_audio_synth'] = new MockAudioProvider();
    }
    // 2. SoundCloud Widget API
    if (typeof SoundCloudAudioProvider !== 'undefined') {
      this.providers['soundcloud'] = new SoundCloudAudioProvider();
    }
    // 3. YouTube IFrame Player API
    if (typeof YouTubeAudioProvider !== 'undefined') {
      this.providers['youtube'] = new YouTubeAudioProvider();
    }
    // 4. Self-Hosted Licensed Stream (HTML5 Audio)
    if (typeof SelfHostedAudioProvider !== 'undefined') {
      this.providers['self_hosted'] = new SelfHostedAudioProvider();
    }

    // Default to web_audio_synth
    this.activeProvider = this.providers['web_audio_synth'] || null;
    if (this.activeProvider) {
      this.activeProvider.setCallbacks(this.callbacks);
    }
  }

  setCallbacks(callbacks) {
    this.callbacks = { ...this.callbacks, ...callbacks };
    Object.values(this.providers).forEach(p => p.setCallbacks(this._wrapCallbacks(p)));
  }

  _wrapCallbacks(provider) {
    return {
      onPlay: () => {
        if (provider === this.activeProvider) this.callbacks.onPlay();
      },
      onPause: () => {
        if (provider === this.activeProvider) this.callbacks.onPause();
      },
      onTimeUpdate: (cur, dur) => {
        if (provider === this.activeProvider) this.callbacks.onTimeUpdate(cur, dur);
      },
      onBuffering: () => {
        if (provider === this.activeProvider) this.callbacks.onBuffering();
      },
      onEnded: () => {
        if (provider === this.activeProvider) this.callbacks.onEnded();
      },
      onError: (err) => {
        if (provider === this.activeProvider) {
          console.warn(`[AudioProviderManager] Provider '${this.activeProviderName}' failed, falling back to Web Audio Synth...`, err);
          this._fallbackToSynth(err);
        }
      },
      onStateChange: (state) => {
        if (provider === this.activeProvider) this.callbacks.onStateChange(state);
      }
    };
  }

  _fallbackToSynth(originalError) {
    const fallback = this.providers['web_audio_synth'];
    if (fallback && this.activeProvider !== fallback) {
      this.activeProvider = fallback;
      this.activeProviderName = 'web_audio_synth';
      if (this.currentTrack) {
        fallback.loadTrack(this.currentTrack);
        fallback.play();
      }
      if (window.JustBaddoUI) {
        JustBaddoUI.toast('Partner stream unavailable. Switched to synthetic demonstration audio.', 'info');
      }
    } else {
      this.callbacks.onError(originalError);
    }
  }

  resolveProvider(track, sessionData = {}) {
    // 1. Session resolution from backend has highest authority
    if (sessionData && sessionData.provider && this.providers[sessionData.provider]) {
      return sessionData.provider;
    }

    // 2. Track metadata provider
    const prov = (track.provider || track.provider_name || '').toLowerCase();
    if (prov === 'soundcloud' && this.providers['soundcloud']) return 'soundcloud';
    if (prov === 'youtube' && this.providers['youtube']) return 'youtube';
    if (prov === 'self_hosted' && this.providers['self_hosted']) return 'self_hosted';

    // 3. Fallback
    return 'web_audio_synth';
  }

  loadTrack(track, sessionData = {}) {
    this.currentTrack = track;
    const targetProviderName = this.resolveProvider(track, sessionData);

    if (this.activeProvider && this.activeProviderName !== targetProviderName) {
      this.activeProvider.pause();
    }

    this.activeProviderName = targetProviderName;
    this.activeProvider = this.providers[targetProviderName] || this.providers['web_audio_synth'];

    if (this.activeProvider) {
      this.activeProvider.loadTrack(track);
    }
  }

  play() {
    if (this.activeProvider) {
      this.activeProvider.play();
    }
  }

  pause() {
    if (this.activeProvider) {
      this.activeProvider.pause();
    }
  }

  resume() {
    if (this.activeProvider) {
      this.activeProvider.resume();
    }
  }

  stop() {
    if (this.activeProvider) {
      this.activeProvider.stop();
    }
  }

  seek(seconds) {
    if (this.activeProvider) {
      this.activeProvider.seek(seconds);
    }
  }

  setVolume(volume) {
    Object.values(this.providers).forEach(p => p.setVolume(volume));
  }

  getCurrentTime() {
    return this.activeProvider ? this.activeProvider.getCurrentTime() : 0;
  }

  getDuration() {
    return this.activeProvider ? this.activeProvider.getDuration() : 180;
  }

  getCapabilities() {
    return this.activeProvider ? this.activeProvider.getCapabilities() : {
      canSeek: true,
      canChangeVolume: true,
      providerName: 'none',
      isAuthorizedStream: false
    };
  }

  getState() {
    return this.activeProvider ? this.activeProvider.getState() : 'IDLE';
  }

  destroy() {
    Object.values(this.providers).forEach(p => p.destroy());
    this.currentTrack = null;
    this.activeProvider = null;
  }
}

window.AudioProviderManager = AudioProviderManager;
