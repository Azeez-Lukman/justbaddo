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
    currentUser: null,
    isAuthenticated: false,
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

    // Try synchronizing session with live backend API
    this.syncWithBackend();
  },

  async syncWithBackend() {
    if (!window.JustBaddoApi) return;
    try {
      const res = await window.JustBaddoApi.auth.getProfile();
      if (res && res.data) {
        this.state.currentUser = res.data;
        this.state.isAuthenticated = true;
        this.emit('auth-changed', this.state.currentUser);

        // Fetch live user playlists from PostgreSQL
        try {
          const plRes = await window.JustBaddoApi.playlists.list();
          if (plRes && plRes.data && Array.isArray(plRes.data)) {
            this.state.userPlaylists = plRes.data.map(p => ({
              id: p.id,
              title: p.title,
              description: p.description,
              createdAt: p.created_at,
              trackIds: p.tracks ? p.tracks.map(t => t.id || t) : []
            }));
            this.emit('playlists-updated', this.state.userPlaylists);
          }
        } catch (e) {
          // Keep local fallback
        }

        // Fetch live notifications from PostgreSQL
        try {
          const notifRes = await window.JustBaddoApi.notifications.list();
          if (notifRes && notifRes.data && Array.isArray(notifRes.data)) {
            this.state.notifications = notifRes.data.map(n => ({
              id: n.id,
              title: n.title,
              message: n.message,
              time: n.created_at || 'Just now',
              read: n.is_read,
              type: n.notification_type
            }));
            this.emit('notifications-updated', this.state.notifications);
          }
        } catch (e) {
          // Keep local fallback
        }
      }
    } catch (err) {
      // User is unauthenticated / guest visitor
      this.state.currentUser = null;
      this.state.isAuthenticated = false;
      this.emit('auth-changed', null);
    }
  },

  async login(credentials) {
    if (!window.JustBaddoApi) throw new Error('API client unavailable');
    const res = await window.JustBaddoApi.auth.login(credentials);
    if (res && res.data) {
      this.state.currentUser = res.data;
      this.state.isAuthenticated = true;
      this.emit('auth-changed', this.state.currentUser);
      await this.syncWithBackend();
    }
    return res;
  },

  async logout() {
    if (window.JustBaddoApi) {
      try {
        await window.JustBaddoApi.auth.logout();
      } catch (e) {
        // Continue client cleanup even if server error
      }
    }
    // Invalidate client-side state
    this.state.currentUser = null;
    this.state.isAuthenticated = false;

    // Clear private cached profile and storage
    if (window.JustBaddoStorage) {
      JustBaddoStorage.remove('user_profile');
      JustBaddoStorage.remove('user_settings');
    }

    this.emit('auth-changed', null);
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

    if (this.state.isAuthenticated && window.JustBaddoApi) {
      window.JustBaddoApi.playlists.create({
        title: title.trim(),
        description: description.trim(),
        is_public: true
      }).then(res => {
        if (res && res.data && res.data.id) {
          newPlaylist.id = res.data.id;
          JustBaddoStorage.set('user_playlists', this.state.userPlaylists);
          this.emit('playlists-updated', this.state.userPlaylists);
        }
      }).catch(err => console.warn('[Playlist API Create]', err.message));
    }

    return newPlaylist;
  },

  addTrackToPlaylist(playlistId, trackId) {
    const playlist = this.state.userPlaylists.find(p => p.id === playlistId);
    if (playlist && !playlist.trackIds.includes(trackId)) {
      playlist.trackIds.push(trackId);
      JustBaddoStorage.set('user_playlists', this.state.userPlaylists);
      this.emit('playlists-updated', this.state.userPlaylists);

      if (this.state.isAuthenticated && window.JustBaddoApi && !playlistId.startsWith('user-pl-')) {
        window.JustBaddoApi.playlists.addTrack(playlistId, trackId)
          .catch(err => console.warn('[Playlist API Add]', err.message));
      }
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

      if (this.state.isAuthenticated && window.JustBaddoApi && !playlistId.startsWith('user-pl-')) {
        window.JustBaddoApi.playlists.removeTrack(playlistId, trackId)
          .catch(err => console.warn('[Playlist API Remove]', err.message));
      }
      return true;
    }
    return false;
  }
};
