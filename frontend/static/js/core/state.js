/**
 * JUSTBADDO — Central Reactive State Store
 * Manages player state, active queue, user playlists, liked tracks, and notifications.
 * Emits events to decouple UI components from data persistence.
 */

window.JustBaddoState = {
  events: {},

  // Default Initial State
  state: {
    player: {
      currentTrack: null,
      isPlaying: false,
      currentTime: 0,
      duration: 180, // seconds
      volume: 0.8,
      isMuted: false,
      isShuffle: false,
      repeatMode: 'off' // 'off' | 'all' | 'one'
    },
    queue: [],
    savedTrackIds: [],
    userPlaylists: [],
    notifications: [
      { id: 'notif-1', title: 'New Poll in Fan Arena', message: 'Which Baddo era represents his peak cultural impact? Vote now.', time: '10m ago', read: false, type: 'arena' },
      { id: 'notif-2', title: 'Community Discussion', message: 'Folake Lawal mentioned you in "How Carpe Diem redefined Olamide".', time: '1h ago', read: false, type: 'community' },
      { id: 'notif-3', title: 'Discography Update', message: 'Verified credits added for "Ikigai / 生き甲斐, Vol. 1".', time: '1d ago', read: true, type: 'catalogue' }
    ]
  },

  init() {
    // Restore persisted state from storage
    const savedPlayer = JustBaddoStorage.get('player_state');
    if (savedPlayer) {
      this.state.player = { ...this.state.player, ...savedPlayer, isPlaying: false };
    }

    const savedQueue = JustBaddoStorage.get('player_queue');
    if (savedQueue && Array.isArray(savedQueue) && savedQueue.length > 0) {
      this.state.queue = savedQueue;
    } else {
      // Initialize with a verified default track
      const defaultTrack = JUSTBADDO_CATALOGUE.getTrackById('ikigai-02'); // Uptown Disco
      if (defaultTrack) {
        this.state.queue = [defaultTrack];
        if (!this.state.player.currentTrack) {
          this.state.player.currentTrack = defaultTrack;
        }
      }
    }

    const savedTracks = JustBaddoStorage.get('saved_tracks');
    if (savedTracks && Array.isArray(savedTracks)) {
      this.state.savedTrackIds = savedTracks;
    } else {
      this.state.savedTrackIds = ['ikigai-02', 'cd-03', 'ln-09', 'em-03'];
    }

    const savedPlaylists = JustBaddoStorage.get('user_playlists');
    if (savedPlaylists && Array.isArray(savedPlaylists)) {
      this.state.userPlaylists = savedPlaylists;
    } else {
      this.state.userPlaylists = [
        {
          id: 'user-pl-1',
          title: 'My Bariga Classics',
          description: 'Essential nostalgic jams from early YBNL days',
          createdAt: '2024-01-10',
          trackIds: ['rap-01', 'ybnl-01', 'bgel-03']
        },
        {
          id: 'user-pl-2',
          title: 'Afro-Fusion Chill',
          description: 'Smooth evening listening from Carpe Diem and UY Scuti',
          createdAt: '2024-03-22',
          trackIds: ['cd-03', 'uy-03', 'ikigai-01']
        }
      ];
    }
  },

  // Event Subscription
  on(eventName, callback) {
    if (!this.events[eventName]) {
      this.events[eventName] = [];
    }
    this.events[eventName].push(callback);
  },

  emit(eventName, data) {
    if (this.events[eventName]) {
      this.events[eventName].forEach(fn => fn(data));
    }
  },

  // State Mutators
  setPlayerState(partial) {
    this.state.player = { ...this.state.player, ...partial };
    JustBaddoStorage.set('player_state', {
      currentTrack: this.state.player.currentTrack,
      volume: this.state.player.volume,
      isMuted: this.state.player.isMuted,
      isShuffle: this.state.player.isShuffle,
      repeatMode: this.state.player.repeatMode
    });
    this.emit('player-updated', this.state.player);
  },

  setQueue(newQueue) {
    this.state.queue = newQueue;
    JustBaddoStorage.set('player_queue', newQueue);
    this.emit('queue-updated', this.state.queue);
  },

  addToQueue(track, playImmediately = false) {
    if (!track) return;
    const exists = this.state.queue.find(t => t.id === track.id);
    if (!exists) {
      this.state.queue.push(track);
      JustBaddoStorage.set('player_queue', this.state.queue);
      this.emit('queue-updated', this.state.queue);
    }
    if (playImmediately) {
      this.setPlayerState({ currentTrack: track, isPlaying: true, currentTime: 0 });
      this.emit('track-play-requested', track);
    }
  },

  removeFromQueue(trackId) {
    this.state.queue = this.state.queue.filter(t => t.id !== trackId);
    JustBaddoStorage.set('player_queue', this.state.queue);
    this.emit('queue-updated', this.state.queue);
  },

  clearQueue() {
    this.state.queue = this.state.player.currentTrack ? [this.state.player.currentTrack] : [];
    JustBaddoStorage.set('player_queue', this.state.queue);
    this.emit('queue-updated', this.state.queue);
  },

  toggleSaveTrack(trackId) {
    const idx = this.state.savedTrackIds.indexOf(trackId);
    let isSaved = false;
    if (idx > -1) {
      this.state.savedTrackIds.splice(idx, 1);
      isSaved = false;
    } else {
      this.state.savedTrackIds.push(trackId);
      isSaved = true;
    }
    JustBaddoStorage.set('saved_tracks', this.state.savedTrackIds);
    this.emit('saved-tracks-updated', { trackId, isSaved, all: this.state.savedTrackIds });
    return isSaved;
  },

  isTrackSaved(trackId) {
    return this.state.savedTrackIds.includes(trackId);
  },

  createUserPlaylist(title, description = '') {
    const newPlaylist = {
      id: 'user-pl-' + Date.now(),
      title: title.trim(),
      description: description.trim(),
      createdAt: new Date().toISOString().split('T')[0],
      trackIds: []
    };
    this.state.userPlaylists.unshift(newPlaylist);
    JustBaddoStorage.set('user_playlists', this.state.userPlaylists);
    this.emit('playlists-updated', this.state.userPlaylists);
    return newPlaylist;
  },

  addTrackToPlaylist(playlistId, trackId) {
    const playlist = this.state.userPlaylists.find(p => p.id === playlistId);
    if (playlist && !playlist.trackIds.includes(trackId)) {
      playlist.trackIds.push(trackId);
      JustBaddoStorage.set('user_playlists', this.state.userPlaylists);
      this.emit('playlists-updated', this.state.userPlaylists);
      return true;
    }
    return false;
  },

  removeTrackFromPlaylist(playlistId, trackId) {
    const playlist = this.state.userPlaylists.find(p => p.id === playlistId);
    if (playlist) {
      playlist.trackIds = playlist.trackIds.filter(id => id !== trackId);
      JustBaddoStorage.set('user_playlists', this.state.userPlaylists);
      this.emit('playlists-updated', this.state.userPlaylists);
      return true;
    }
    return false;
  }
};
