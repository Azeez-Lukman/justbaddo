/**
 * JUSTBADDO — Unified Backend API Client
 * Provides authenticated, CSRF-protected communication between the frontend interface
 * and Django REST Framework endpoints (/api/v1/...).
 */

(function () {
  'use strict';

  class JustBaddoApiClient {
    constructor() {
      this.baseUrl = '/api/v1';
    }

    /**
     * Retrieve CSRF token from document cookies.
     */
    getCsrfToken() {
      const name = 'csrftoken=';
      const decodedCookie = decodeURIComponent(document.cookie);
      const ca = decodedCookie.split(';');
      for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(name) === 0) {
          return c.substring(name.length, c.length);
        }
      }
      return null;
    }

    /**
     * Generic HTTP request handler with automatic JSON serialization,
     * credential inclusion, and error formatting.
     */
    async request(endpoint, options = {}) {
      const method = (options.method || 'GET').toUpperCase();
      let url = endpoint;
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        if (!url.startsWith('/api/')) {
          url = `${this.baseUrl}/${url.replace(/^\//, '')}`;
        }
      }

      const headers = {
        'Accept': 'application/json',
        ...(options.headers || {})
      };

      if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
        const csrfToken = this.getCsrfToken();
        if (csrfToken) {
          headers['X-CSRFToken'] = csrfToken;
        }
      }

      if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(options.body);
      }

      const fetchOptions = {
        method,
        headers,
        credentials: 'include', // Ensures session cookie is transmitted
        ...options
      };

      try {
        const response = await fetch(url, fetchOptions);
        let data = null;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          data = await response.json();
        } else {
          data = await response.text();
        }

        if (!response.ok) {
          const errorMessage = (data && data.message) || (data && data.detail) || `Request failed with status ${response.status}`;
          const err = new Error(errorMessage);
          err.status = response.status;
          err.data = data;
          throw err;
        }

        return data;
      } catch (error) {
        console.warn(`[JustBaddoApiClient] Error on ${method} ${url}:`, error.message);
        throw error;
      }
    }

    // ================= DOMAIN APIS =================

    /* Accounts & Authentication */
    auth = {
      register: (userData) => this.request('accounts/register/', { method: 'POST', body: userData }),
      login: (credentials) => this.request('accounts/login/', { method: 'POST', body: credentials }),
      logout: () => this.request('accounts/logout/', { method: 'POST' }),
      getProfile: () => this.request('accounts/profile/'),
      getPublicProfile: (username) => this.request(`accounts/profile/${encodeURIComponent(username)}/`),
      getSettings: () => this.request('accounts/settings/'),
      updateSettings: (settingsData) => this.request('accounts/settings/', { method: 'PUT', body: settingsData }),
      requestPasswordReset: (email) => this.request('accounts/password-reset/', { method: 'POST', body: { email } })
    };

    /* Music Discovery & Catalogue */
    music = {
      getArtist: () => this.request('music/artist/'),
      getAlbums: (params) => {
        const qs = params ? '?' + new URLSearchParams(params).toString() : '';
        return this.request(`music/albums/${qs}`);
      },
      getAlbum: (slug) => this.request(`music/albums/${encodeURIComponent(slug)}/`),
      getSingles: (params) => {
        const qs = params ? '?' + new URLSearchParams(params).toString() : '';
        return this.request(`music/singles/${qs}`);
      },
      getTracks: (params) => {
        const qs = params ? '?' + new URLSearchParams(params).toString() : '';
        return this.request(`music/tracks/${qs}`);
      },
      getTrack: (trackId) => this.request(`music/tracks/${encodeURIComponent(trackId)}/`),
      search: (query) => this.request(`music/search/?q=${encodeURIComponent(query)}`),
      getTimeline: () => this.request('music/timeline/')
    };

    /* Playback & Telemetry */
    playback = {
      checkRights: (trackId) => this.request(`playback/check/${encodeURIComponent(trackId)}/`),
      createSession: (trackId) => this.request('playback/session/', { method: 'POST', body: { track_id: trackId } }),
      logPlay: (logData) => this.request('playback/log/', { method: 'POST', body: logData }),
      getHistory: () => this.request('playback/history/')
    };

    /* Playlists */
    playlists = {
      list: () => this.request('playlists/'),
      get: (playlistId) => this.request(`playlists/${playlistId}/`),
      create: (data) => this.request('playlists/', { method: 'POST', body: data }),
      addTrack: (playlistId, trackId) => this.request(`playlists/${playlistId}/tracks/`, { method: 'POST', body: { track_id: trackId } }),
      removeTrack: (playlistId, trackId) => this.request(`playlists/${playlistId}/tracks/${encodeURIComponent(trackId)}/`, { method: 'DELETE' })
    };

    /* Community */
    community = {
      getFeed: (category) => {
        const qs = category && category !== 'ALL' ? `?category=${encodeURIComponent(category)}` : '';
        return this.request(`community/feed/${qs}`);
      },
      getPosts: (category) => {
        const qs = category && category !== 'ALL' ? `?category=${encodeURIComponent(category)}` : '';
        return this.request(`community/posts/${qs}`);
      },
      getPost: (postId) => this.request(`community/posts/${postId}/`),
      createPost: (postData) => this.request('community/posts/', { method: 'POST', body: postData }),
      addComment: (postId, content) => this.request(`community/posts/${postId}/comments/`, { method: 'POST', body: { content } }),
      toggleLike: (postId) => this.request(`community/posts/${postId}/like/`, { method: 'POST' }),
      toggleFollow: (username) => this.request(`community/follow/${encodeURIComponent(username)}/`, { method: 'POST' })
    };

    /* Fan Arena */
    arena = {
      getPolls: () => this.request('arena/polls/'),
      votePoll: (pollId, optionId) => this.request(`arena/polls/${pollId}/vote/`, { method: 'POST', body: { option_id: optionId } }),
      getBattles: () => this.request('arena/battles/'),
      voteBattle: (battleId, trackChoice) => this.request(`arena/battles/${battleId}/vote/`, { method: 'POST', body: { track_choice: trackChoice } }),
      getTriviaQuiz: () => this.request('arena/trivia/quiz/'),
      submitTrivia: (submission) => this.request('arena/trivia/submit/', { method: 'POST', body: submission }),
      getLeaderboard: () => this.request('arena/leaderboard/')
    };

    /* Fan Stories */
    stories = {
      list: () => this.request('stories/'),
      get: (storyId) => this.request(`stories/${storyId}/`),
      submit: (storyData) => this.request('stories/', { method: 'POST', body: storyData })
    };

    /* Notifications */
    notifications = {
      list: () => this.request('notifications/'),
      getUnreadCount: () => this.request('notifications/unread-count/'),
      markRead: (notificationId) => this.request(`notifications/${notificationId}/read/`, { method: 'POST' }),
      markAllRead: () => this.request('notifications/mark-all-read/', { method: 'POST' })
    };

    /* Licensing */
    licensing = {
      getRecords: () => this.request('licensing/records/'),
      check: (trackId) => this.request(`licensing/check/${encodeURIComponent(trackId)}/`),
      submitInquiry: (inquiryData) => this.request('licensing/inquiry/', { method: 'POST', body: inquiryData })
    };

    /* Moderation */
    moderation = {
      submitReport: (reportData) => this.request('moderation/report/', { method: 'POST', body: reportData })
    };
  }

  // Expose as global singleton
  window.JustBaddoApi = new JustBaddoApiClient();
})();
