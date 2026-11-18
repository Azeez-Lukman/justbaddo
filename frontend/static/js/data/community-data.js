/**
 * JUSTBADDO — Community Demonstration Data
 * Realistic fan posts, discussions, replies, member profiles, and engagement counters.
 * All identities are clearly marked demonstration fan personas.
 */

window.JUSTBADDO_COMMUNITY = {
  currentUser: {
    id: 'user-baddo-fan-01',
    username: 'BaddoCitizen',
    displayName: 'Baddo Citizen',
    handle: '@BaddoCitizen',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
    joinedDate: 'May 2023',
    tier: 'Bariga Club',
    bio: 'Music enthusiast, collector of YBNL vinyls and live concert veteran. Bariga to the world.',
    followingCount: 142,
    followersCount: 389,
    savedTracksCount: 46,
    playlistsCount: 5
  },

  members: [
    {
      id: 'm-01',
      username: 'BarigaBoy_92',
      displayName: 'Tunde Adeyemi',
      handle: '@BarigaBoy_92',
      badge: 'Veteran Fan',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80',
      bio: 'Witnessed the Eni Duro era live in Bariga. YBNL archivist since 2011.'
    },
    {
      id: 'm-02',
      username: 'FolakeVibes',
      displayName: 'Folake Lawal',
      handle: '@FolakeVibes',
      badge: 'Curator',
      avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=200&q=80',
      bio: 'Music journalist & Afrobeats researcher. Writing about West African rap evolution.'
    },
    {
      id: 'm-03',
      username: 'LagosNawaLover',
      displayName: 'Chinedu Eze',
      handle: '@LagosNawaLover',
      badge: 'Arena Champ',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80',
      bio: 'Wo!! dance challenge semi-finalist (2017). Live music lover.'
    },
    {
      id: 'm-04',
      username: 'AminatAfro',
      displayName: 'Amina Bello',
      handle: '@AminatAfro',
      badge: 'Super Contributor',
      avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80',
      bio: 'UY Scuti is timeless art. Deep catalogue listener from Abuja.'
    }
  ],

  posts: [
    {
      id: 'post-01',
      author: {
        id: 'm-02',
        name: 'Folake Lawal',
        handle: '@FolakeVibes',
        avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=200&q=80',
        badge: 'Curator'
      },
      timeAgo: '2 hours ago',
      category: 'Album Analysis',
      title: 'How Carpe Diem redefined Olamide sonic trajectory',
      content: 'When Carpe Diem dropped in October 2020, people did not immediately realise we were entering a whole new artistic era. Moving away from the sheer frenzy of 120+ BPM street bangers into silky, mid-tempo afro-fusion (Infinity, Green Light, Triumphant) opened doors for the current UY Scuti and Unruly sound. What is your favourite track from that record?',
      taggedTrack: { id: 'cd-03', title: 'Infinity (feat. Omah Lay)', album: 'Carpe Diem' },
      likes: 184,
      isLiked: false,
      commentsCount: 42,
      sharesCount: 19,
      comments: [
        {
          id: 'c-01',
          author: 'BarigaBoy_92',
          avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80',
          time: '1 hour ago',
          text: 'P.Priime production across that entire album was simply immaculate. "Triumphant" with Bella Shmurda hits home every single time.'
        },
        {
          id: 'c-02',
          author: 'AminatAfro',
          avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80',
          time: '45 mins ago',
          text: 'Totally agree. It showed true artistic maturity without losing an ounce of street credibility.'
        }
      ]
    },
    {
      id: 'post-02',
      author: {
        id: 'm-01',
        name: 'Tunde Adeyemi',
        handle: '@BarigaBoy_92',
        badge: 'Veteran Fan'
      },
      timeAgo: '5 hours ago',
      category: 'Catalogue Nostalgia',
      title: 'Remembering the iconic one-take "Eni Duro" video (2010)',
      content: '14 years later, nothing matches the raw hunger of Eni Duro. Shot in Lagos with rapid outfit changes and that unforgettable opening line. It shifted Nigerian indigenous rap from niche underground curiosity straight into mainstream hegemony.',
      taggedTrack: { id: 'rap-01', title: 'Eni Duro', album: 'Rapsodi' },
      likes: 295,
      isLiked: true,
      commentsCount: 68,
      sharesCount: 54,
      comments: [
        {
          id: 'c-03',
          author: 'LagosNawaLover',
          avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80',
          time: '3 hours ago',
          text: 'I memorized every lyric in high school! ID Cabasa cooked timeless magic on that beat.'
        }
      ]
    },
    {
      id: 'post-03',
      author: {
        id: 'm-03',
        name: 'Chinedu Eze',
        handle: '@LagosNawaLover',
        badge: 'Arena Champ'
      },
      timeAgo: '1 day ago',
      category: 'Discussion',
      title: 'Eyan Mayweather: 21 tracks, ZERO features. Has any other African rapper done this?',
      content: 'In 2015 Baddo dropped Eyan Mayweather without a single featured artist. 21 tracks of pure solo execution including Bobo, Melo Melo, Matters Arising and Lagos Boys. That confidence was unreal.',
      taggedTrack: { id: 'em-03', title: 'Bobo (Shakiti Bobo)', album: 'Eyan Mayweather' },
      likes: 412,
      isLiked: false,
      commentsCount: 94,
      sharesCount: 82,
      comments: []
    }
  ]
};
