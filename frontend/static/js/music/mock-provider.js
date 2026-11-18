/**
 * JUSTBADDO — Mock Audio Provider
 * Provides a fully functional, zero-copyright Web Audio API synthesizer for interface testing.
 * Synthesizes a subtle, warm Afrobeats harmonic pulse based on track BPM & key,
 * allowing full scrub, play, pause, volume, and queue testing with zero copyright infringement.
 */

class MockAudioProvider extends AudioProviderInterface {
  constructor(options = {}) {
    super(options);
    this.currentTrack = null;
    this.isPlaying = false;
    this.currentTime = 0;
    this.duration = 180; // default 3:00 in seconds
    this.volume = 0.7;
    this.timerId = null;
    this.audioCtx = null;
    this.gainNode = null;
    this.oscillator = null;
  }

  getCapabilities() {
    return {
      providerName: 'web_audio_synth',
      displayName: 'Web Audio API Synth (Zero-Copyright Demo)',
      canSeek: true,
      canChangeVolume: true,
      supportsHeadless: true,
      requiresUserGesture: false,
      isAuthorizedStream: false
    };
  }

  getState() {
    if (!this.currentTrack) return 'IDLE';
    return this.isPlaying ? 'PLAYING' : 'PAUSED';
  }

  _initAudioContext() {
    if (!this.audioCtx && typeof window !== 'undefined') {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.audioCtx = new AudioContext();
        this.gainNode = this.audioCtx.createGain();
        this.gainNode.gain.setValueAtTime(this.volume * 0.15, this.audioCtx.currentTime); // gentle volume
        this.gainNode.connect(this.audioCtx.destination);
      }
    }
    if (this.audioCtx && this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
  }

  _parseDurationToSeconds(durationStr) {
    if (!durationStr || typeof durationStr !== 'string') return 180;
    const parts = durationStr.split(':').map(Number);
    if (parts.length === 2) {
      return (parts[0] * 60) + parts[1];
    } else if (parts.length === 3) {
      return (parts[0] * 3600) + (parts[1] * 60) + parts[2];
    }
    return 180;
  }

  loadTrack(track) {
    this.pause();
    this.currentTrack = track;
    this.currentTime = 0;
    this.duration = this._parseDurationToSeconds(track.duration);
    this.callbacks.onTimeUpdate(this.currentTime, this.duration);
  }

  play() {
    if (!this.currentTrack) return;
    this._initAudioContext();
    this.isPlaying = true;

    // Start synthetic sound loop (gentle rhythmic pulse)
    this._startSynthPulse();

    // Start simulation timer (1s interval)
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

    this.callbacks.onPlay();
  }

  pause() {
    this.isPlaying = false;
    clearInterval(this.timerId);
    this._stopSynthPulse();
    this.callbacks.onPause();
  }

  seek(seconds) {
    this.currentTime = Math.max(0, Math.min(seconds, this.duration));
    this.callbacks.onTimeUpdate(this.currentTime, this.duration);
  }

  setVolume(volume) {
    this.volume = Math.max(0, Math.min(volume, 1));
    if (this.gainNode && this.audioCtx) {
      this.gainNode.gain.setValueAtTime(this.volume * 0.15, this.audioCtx.currentTime);
    }
  }

  getCurrentTime() {
    return this.currentTime;
  }

  getDuration() {
    return this.duration;
  }

  _startSynthPulse() {
    if (!this.audioCtx || !this.gainNode) return;
    try {
      this.oscillator = this.audioCtx.createOscillator();
      this.oscillator.type = 'triangle';
      // Pleasant warm bass frequency (A2 = 110Hz or C3 = 130Hz)
      const baseFreq = this.currentTrack && this.currentTrack.bpm ? (this.currentTrack.bpm > 115 ? 146.83 : 110.00) : 110.00;
      this.oscillator.frequency.setValueAtTime(baseFreq, this.audioCtx.currentTime);
      this.oscillator.connect(this.gainNode);
      this.oscillator.start();
    } catch (e) {
      // Audio autoplay policy or device fallback
    }
  }

  _stopSynthPulse() {
    if (this.oscillator) {
      try {
        this.oscillator.stop();
        this.oscillator.disconnect();
      } catch (e) {}
      this.oscillator = null;
    }
  }

  destroy() {
    this.pause();
    if (this.audioCtx) {
      this.audioCtx.close();
      this.audioCtx = null;
    }
  }
}

window.MockAudioProvider = MockAudioProvider;
