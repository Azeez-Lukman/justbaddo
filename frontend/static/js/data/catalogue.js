/**
 * JUSTBADDO — Verified Olamide Discography & Music Catalogue Data
 * Source of truth for albums, tracks, release dates, credits and playback availability states.
 * Respects licensing restrictions: playback statuses clearly differentiate between
 * metadata, authorised provider, demo/synthetic preview, and restricted tracks.
 */

window.JUSTBADDO_CATALOGUE = {
  playbackStatuses: {
    METADATA_ONLY: { id: 'metadata_only', label: 'Catalogue Record', badgeClass: 'bg-zinc-800 text-zinc-400 border-zinc-700' },
    AUTHORISED_PROVIDER: { id: 'authorised_provider', label: 'Authorised Provider', badgeClass: 'bg-emerald-950 text-emerald-400 border-emerald-800' },
    JUSTBADDO_STREAMING: { id: 'justbaddo_streaming', label: 'JustBaddo Preview', badgeClass: 'bg-amber-950 text-amber-400 border-amber-800' },
    RESTRICTED: { id: 'restricted', label: 'Territory Restricted', badgeClass: 'bg-rose-950 text-rose-400 border-rose-800' },
    WITHDRAWN: { id: 'withdrawn', label: 'Archived / Withdrawn', badgeClass: 'bg-zinc-900 text-zinc-500 border-zinc-800' }
  },

  albums: [
    {
      id: 'ikigai-vol-1',
      title: 'Ikigai / 生き甲斐, Vol. 1',
      slug: 'ikigai-vol-1',
      type: 'EP',
      releaseYear: 2024,
      releaseDate: 'June 26, 2024',
      trackCount: 7,
      duration: '21:14',
      coverArt: 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation / EMPIRE',
      distributor: 'EMPIRE',
      description: 'Japanese for "a reason for being", Ikigai captures Olamide in a reflective yet high-energy frame of mind, blending street instincts with international polish and showcasing rising and established YBNL royalty.',
      featuredArtists: ['Fireboy DML', 'Asake', 'Sabri', 'Young Jonn'],
      producers: ['Pheelz', 'BBM', 'Semzi'],
      tracks: [
        { id: 'ikigai-01', number: 1, title: 'Metaverse', duration: '2:47', featured: '', producer: 'Semzi', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 104, key: 'F#m' },
        { id: 'ikigai-02', number: 2, title: 'Uptown Disco', duration: '3:15', featured: 'Fireboy DML & Asake', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 118, key: 'Am' },
        { id: 'ikigai-03', number: 3, title: 'Makaveli', duration: '2:56', featured: '', producer: 'BBM', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 108, key: 'Gm' },
        { id: 'ikigai-04', number: 4, title: 'Knockout', duration: '3:04', featured: 'Sabri', producer: 'BBM', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 100, key: 'Cm' },
        { id: 'ikigai-05', number: 5, title: 'Hello Habibi', duration: '3:18', featured: '', producer: 'Semzi', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 112, key: 'Dm' },
        { id: 'ikigai-06', number: 6, title: 'Morowore', duration: '2:50', featured: '', producer: 'Pheelz', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 105, key: 'Em' },
        { id: 'ikigai-07', number: 7, title: 'Synchro System', duration: '3:04', featured: 'Pheelz, Young Jonn & Lil Kesh', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 120, key: 'Bm' }
      ]
    },
    {
      id: 'unruly',
      title: 'Unruly',
      slug: 'unruly',
      type: 'Studio Album',
      releaseYear: 2023,
      releaseDate: 'August 11, 2023',
      trackCount: 15,
      duration: '42:18',
      coverArt: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation / EMPIRE',
      distributor: 'EMPIRE',
      description: 'Olamide tenth studio album marks a celebratory summit of an unparalleled career. Unruly balances melodic afrobeats, dancehall influences and street-tested verses with guest turns from Asake, CKay, BNXN, Rema and Fireboy DML.',
      featuredArtists: ['CKay', 'Asake', 'Fireboy DML', 'BNXN', 'Rema'],
      producers: ['Eskeez', 'Magicsticks', 'P.Priime'],
      tracks: [
        { id: 'unruly-01', number: 1, title: 'Celebrate', duration: '2:44', featured: '', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 106, key: 'Ab' },
        { id: 'unruly-02', number: 2, title: 'Jinja', duration: '2:51', featured: '', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 110, key: 'Eb' },
        { id: 'unruly-03', number: 3, title: 'Problem', duration: '2:40', featured: '', producer: 'Eskeez', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 114, key: 'Bb' },
        { id: 'unruly-04', number: 4, title: 'Gaza', duration: '2:38', featured: '', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 112, key: 'Fm' },
        { id: 'unruly-05', number: 5, title: 'Doom', duration: '2:47', featured: '', producer: 'Eskeez', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 102, key: 'C#m' },
        { id: 'unruly-06', number: 6, title: 'Trumpet', duration: '2:49', featured: 'CKay', producer: 'P.Priime & CKay', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 100, key: 'Bbm' },
        { id: 'unruly-07', number: 7, title: 'Window', duration: '2:35', featured: '', producer: 'Magicsticks', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 108, key: 'G#m' },
        { id: 'unruly-08', number: 8, title: 'New Religion', duration: '2:41', featured: 'Asake', producer: 'Magicsticks & B-Bankz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 115, key: 'Am' },
        { id: 'unruly-09', number: 9, title: 'Shibebe', duration: '2:48', featured: 'Fireboy DML', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 112, key: 'Dm' },
        { id: 'unruly-10', number: 10, title: 'Mukulu', duration: '2:52', featured: 'Rema', producer: 'P.Priime', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 105, key: 'Em' },
        { id: 'unruly-11', number: 11, title: 'Hardcore', duration: '2:33', featured: '', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 116, key: 'Cm' },
        { id: 'unruly-12', number: 12, title: 'Supplier', duration: '2:45', featured: '', producer: 'Eskeez', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 108, key: 'F#m' },
        { id: 'unruly-13', number: 13, title: 'Life Goes On', duration: '2:58', featured: '', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 98, key: 'A' },
        { id: 'unruly-14', number: 14, title: 'No Worries', duration: '2:40', featured: '', producer: 'Eskeez', status: 'RESTRICTED', isPlayable: false, bpm: 104, key: 'D' },
        { id: 'unruly-15', number: 15, title: 'Street Jam', duration: '2:27', featured: '', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 120, key: 'Gm' }
      ]
    },
    {
      id: 'uy-scuti',
      title: 'UY Scuti',
      slug: 'uy-scuti',
      type: 'Studio Album',
      releaseYear: 2021,
      releaseDate: 'June 18, 2021',
      trackCount: 11,
      duration: '32:04',
      coverArt: 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation / EMPIRE',
      distributor: 'EMPIRE',
      description: 'Named after one of the largest known stars in the universe, UY Scuti reveals a sublime, intimate sonic direction, trading rapid-fire bar delivery for warm reggae bounce, acoustic guitars and effortless melodies.',
      featuredArtists: ['Phyno', 'Fave', 'Jaywillz', 'Layydoe'],
      producers: ['Eskeez', 'P.Priime', 'B-Bankz'],
      tracks: [
        { id: 'uy-01', number: 1, title: 'Need for Speed', duration: '2:43', featured: '', producer: 'P.Priime', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 98, key: 'Dm' },
        { id: 'uy-02', number: 2, title: 'Jailer', duration: '3:05', featured: 'Jaywillz', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 102, key: 'Am' },
        { id: 'uy-03', number: 3, title: 'Rock', duration: '3:05', featured: '', producer: 'P.Priime', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 100, key: 'F' },
        { id: 'uy-04', number: 4, title: 'Julie', duration: '2:43', featured: '', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 104, key: 'C' },
        { id: 'uy-05', number: 5, title: 'Rough Up', duration: '2:56', featured: 'Layydoe', producer: 'Eskeez', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 96, key: 'Bb' },
        { id: 'uy-06', number: 6, title: 'Want', duration: '2:40', featured: 'Fave', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 102, key: 'Gm' },
        { id: 'uy-07', number: 7, title: 'PonPon', duration: '2:57', featured: 'Fave', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 105, key: 'Em' },
        { id: 'uy-08', number: 8, title: 'Cup of Tea', duration: '2:48', featured: '', producer: 'Eskeez', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 99, key: 'Am' },
        { id: 'uy-09', number: 9, title: 'Somebody', duration: '2:58', featured: 'Phyno', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 104, key: 'Fm' },
        { id: 'uy-10', number: 10, title: 'So Much More', duration: '3:02', featured: '', producer: 'Eskeez', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 95, key: 'Dm' },
        { id: 'uy-11', number: 11, title: 'Fly (Bonus)', duration: '2:47', featured: '', producer: 'Eskeez', status: 'METADATA_ONLY', isPlayable: false, bpm: 100, key: 'G' }
      ]
    },
    {
      id: 'carpe-diem',
      title: 'Carpe Diem',
      slug: 'carpe-diem',
      type: 'Studio Album',
      releaseYear: 2020,
      releaseDate: 'October 8, 2020',
      trackCount: 12,
      duration: '38:20',
      coverArt: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation / EMPIRE',
      distributor: 'EMPIRE',
      description: 'Carpe Diem signalled the beginning of Olamide partnership with EMPIRE and a sophisticated musical chapter. Blending mid-tempo melodies with razor-sharp lyricism, the project produced historic hits including Infinity and Loading.',
      featuredArtists: ['Omah Lay', 'Fireboy DML', 'Bad Boy Timz', 'Bella Shmurda', 'Peruzzi', 'Phyno'],
      producers: ['P.Priime', 'Pheelz', 'ID Cabasa', 'Vstix'],
      tracks: [
        { id: 'cd-01', number: 1, title: 'Another Level', duration: '2:55', featured: '', producer: 'P.Priime', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 102, key: 'Ab' },
        { id: 'cd-02', number: 2, title: 'Green Light', duration: '3:15', featured: '', producer: 'P.Priime', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 105, key: 'Eb' },
        { id: 'cd-03', number: 3, title: 'Infinity', duration: '2:52', featured: 'Omah Lay', producer: 'P.Priime', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 100, key: 'Gm' },
        { id: 'cd-04', number: 4, title: 'Eru', duration: '3:03', featured: '', producer: 'P.Priime', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 112, key: 'Cm' },
        { id: 'cd-05', number: 5, title: 'Chimichanga', duration: '2:59', featured: '', producer: 'P.Priime', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 104, key: 'Fm' },
        { id: 'cd-06', number: 6, title: 'Shilalo', duration: '2:58', featured: 'Phyno', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 106, key: 'Bbm' },
        { id: 'cd-07', number: 7, title: 'Loading', duration: '3:15', featured: 'Bad Boy Timz', producer: 'P.Priime', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 118, key: 'Am' },
        { id: 'cd-08', number: 8, title: 'Unconditionally', duration: '3:27', featured: 'Peruzzi', producer: 'Vstix', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 100, key: 'Dm' },
        { id: 'cd-09', number: 9, title: 'Somebody', duration: '3:04', featured: 'Phyno', producer: 'P.Priime', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 108, key: 'Em' },
        { id: 'cd-10', number: 10, title: 'Do Better', duration: '3:14', featured: '', producer: 'Young Jonn', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 105, key: 'C' },
        { id: 'cd-11', number: 11, title: 'Triumphant', duration: '3:21', featured: 'Bella Shmurda', producer: 'P.Priime', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 98, key: 'G' },
        { id: 'cd-12', number: 12, title: 'Wonnasun', duration: '3:07', featured: '', producer: 'ID Cabasa', status: 'METADATA_ONLY', isPlayable: false, bpm: 110, key: 'D' }
      ]
    },
    {
      id: 'lagos-nawa',
      title: 'Lagos Nawa',
      slug: 'lagos-nawa',
      type: 'Studio Album',
      releaseYear: 2017,
      releaseDate: 'November 17, 2017',
      trackCount: 17,
      duration: '56:30',
      coverArt: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation',
      distributor: 'YBNL Nation',
      description: 'Recorded reportedly in only 48 hours, Lagos Nawa celebrated the "Wobey Sound"—an unfiltered, energetic street rhythm that defined Lagos nightlife in late 2017, led by the monster viral track Wo!!.',
      featuredArtists: ['Reminisce', 'Timaya', 'Tiwa Savage', 'Phyno'],
      producers: ['Young Jonn'],
      tracks: [
        { id: 'ln-01', number: 1, title: 'Fe Nu Shey Street', duration: '3:10', featured: '', producer: 'Young Jonn', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 118, key: 'Am' },
        { id: 'ln-02', number: 2, title: 'Radio Lagos', duration: '3:32', featured: '', producer: 'Young Jonn', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 116, key: 'Dm' },
        { id: 'ln-03', number: 3, title: 'Yagaga', duration: '3:22', featured: '', producer: 'Young Jonn', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 114, key: 'Em' },
        { id: 'ln-04', number: 4, title: 'The Way', duration: '3:28', featured: '', producer: 'Young Jonn', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 115, key: 'Gm' },
        { id: 'ln-05', number: 5, title: 'Everyday Is Not A Christmas', duration: '3:14', featured: '', producer: 'Young Jonn', status: 'METADATA_ONLY', isPlayable: false, bpm: 110, key: 'F' },
        { id: 'ln-06', number: 6, title: 'Lagos Nawa', duration: '3:07', featured: '', producer: 'Young Jonn', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 120, key: 'C' },
        { id: 'ln-07', number: 7, title: 'Bend You', duration: '3:35', featured: '', producer: 'Young Jonn', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 118, key: 'G' },
        { id: 'ln-08', number: 8, title: 'Sheevita Juice', duration: '3:12', featured: 'Skepta', producer: 'Young Jonn', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 112, key: 'Bb' },
        { id: 'ln-09', number: 9, title: 'Wo!!', duration: '3:15', featured: '', producer: 'Young Jonn', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 125, key: 'Am' },
        { id: 'ln-10', number: 10, title: 'SaysayMaley', duration: '3:05', featured: '', producer: 'Young Jonn', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 122, key: 'Dm' }
      ]
    },
    {
      id: 'the-glory',
      title: 'The Glory',
      slug: 'the-glory',
      type: 'Studio Album',
      releaseYear: 2016,
      releaseDate: 'December 26, 2016',
      trackCount: 16,
      duration: '52:10',
      coverArt: 'https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation',
      distributor: 'YBNL Nation',
      description: 'Released intentionally on Boxing Day alongside OLIC 3, The Glory saw Olamide return uncompromisingly to his rap foundations, answering fans who yearned for unadulterated hip-hop bars.',
      featuredArtists: ['Phyno', 'Wande Coal', 'Burna Boy', 'Davolee', 'Sossi'],
      producers: ['Pheelz', 'Young Jonn', 'Sossick'],
      tracks: [
        { id: 'tg-01', number: 1, title: 'The Glory Intro', duration: '2:31', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 90, key: 'Cm' },
        { id: 'tg-02', number: 2, title: 'Letter to Milli', duration: '4:15', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 88, key: 'Gm' },
        { id: 'tg-03', number: 3, title: 'Journey of a Thousand Miles', duration: '3:39', featured: '', producer: 'Pheelz', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 92, key: 'Dm' },
        { id: 'tg-04', number: 4, title: 'Underground', duration: '3:11', featured: 'Akuchi', producer: 'Young Jonn', status: 'METADATA_ONLY', isPlayable: false, bpm: 94, key: 'Am' },
        { id: 'tg-05', number: 5, title: 'Pepper Dem Gang', duration: '3:30', featured: 'Davolee', producer: 'Young Jonn', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 118, key: 'Em' },
        { id: 'tg-06', number: 6, title: 'Owo Blow', duration: '3:20', featured: '', producer: 'Major Bangz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 110, key: 'Fm' }
      ]
    },
    {
      id: 'eyan-mayweather',
      title: 'Eyan Mayweather',
      slug: 'eyan-mayweather',
      type: 'Studio Album',
      releaseYear: 2015,
      releaseDate: 'November 23, 2015',
      trackCount: 21,
      duration: '1:11:45',
      coverArt: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation',
      distributor: 'YBNL Nation',
      description: 'A staggering achievement in solo execution: 21 tracks with zero guest features. Eyan Mayweather produced the national dance phenomenon Bobo, the emotional ballad Melo Melo, and explosive street anthems.',
      featuredArtists: [],
      producers: ['Pheelz', 'Young Jonn', 'B-Banks', 'ID Cabasa'],
      tracks: [
        { id: 'em-01', number: 1, title: 'Eyan Mayweather', duration: '3:24', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 112, key: 'Am' },
        { id: 'em-02', number: 2, title: 'Inferiority Complex', duration: '3:12', featured: '', producer: 'Pheelz', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 108, key: 'Dm' },
        { id: 'em-03', number: 3, title: 'Bobo (Shakiti Bobo)', duration: '4:11', featured: '', producer: 'Young Jonn', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 118, key: 'C' },
        { id: 'em-04', number: 4, title: 'Boom Boom Boom', duration: '3:18', featured: '', producer: 'Pheelz', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 114, key: 'F' },
        { id: 'em-05', number: 5, title: 'Lagos Boys', duration: '3:45', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 120, key: 'G' },
        { id: 'em-06', number: 6, title: 'Melo Melo', duration: '3:38', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 95, key: 'Em' },
        { id: 'em-07', number: 7, title: 'Matters Arising', duration: '3:50', featured: '', producer: 'Pheelz', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 104, key: 'Bm' }
      ]
    },
    {
      id: 'street-ot',
      title: 'Street OT',
      slug: 'street-ot',
      type: 'Studio Album',
      releaseYear: 2014,
      releaseDate: 'November 14, 2014',
      trackCount: 22,
      duration: '1:17:10',
      coverArt: 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation',
      distributor: 'YBNL Nation',
      description: 'Street OT cemented Olamide status as the undisputed voice of Nigerian street reality. Housing "Story For The Gods", "Goons Mi", and the iconic "Skelemba" featuring Don Jazzy, the album defined an entire generation.',
      featuredArtists: ['Don Jazzy', 'Phyno', 'Viktoh', 'Chinko Ekun', 'Lil Kesh', 'Pasuma'],
      producers: ['Pheelz', 'Young Jonn', 'B-Banks'],
      tracks: [
        { id: 'sot-01', number: 1, title: 'Prayer for Client', duration: '3:20', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 110, key: 'Gm' },
        { id: 'sot-02', number: 2, title: 'Goons Mi', duration: '3:45', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 115, key: 'Am' },
        { id: 'sot-03', number: 3, title: 'Story For The Gods', duration: '3:32', featured: '', producer: 'Young Jonn', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 118, key: 'Dm' },
        { id: 'sot-04', number: 4, title: 'Skelemba', duration: '3:27', featured: 'Don Jazzy', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 122, key: 'C' },
        { id: 'sot-05', number: 5, title: 'Up In The Club', duration: '3:15', featured: 'Viktoh', producer: 'Pheelz', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 124, key: 'Em' }
      ]
    },
    {
      id: 'baddest-guy-ever-liveth',
      title: 'Baddest Guy Ever Liveth (BGEL)',
      slug: 'baddest-guy-ever-liveth',
      type: 'Studio Album',
      releaseYear: 2013,
      releaseDate: 'November 7, 2013',
      trackCount: 21,
      duration: '1:16:30',
      coverArt: 'https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation',
      distributor: 'YBNL Nation',
      description: 'Winner of Album of the Year and Best Rap Album at The Headies 2014, BGEL is widely considered one of the finest Nigerian hip-hop records in history, producing timeless cultural anthems like Durosoke, Turn Up, and Yemi My Lover.',
      featuredArtists: ['Do-2d-tun', 'Phyno', 'Ice Prince', 'Burna Boy', 'Pheelz', 'Buckwyla'],
      producers: ['Pheelz'],
      tracks: [
        { id: 'bgel-01', number: 1, title: 'Intro', duration: '2:10', featured: 'Do-2d-tun', producer: 'Pheelz', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 90, key: 'Cm' },
        { id: 'bgel-02', number: 2, title: 'Yemi My Lover', duration: '3:18', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 112, key: 'Am' },
        { id: 'bgel-03', number: 3, title: 'Durosoke', duration: '4:02', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 114, key: 'Dm' },
        { id: 'bgel-04', number: 4, title: 'Anifowose', duration: '3:58', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 96, key: 'Fm' },
        { id: 'bgel-05', number: 5, title: 'Turn Up', duration: '3:45', featured: '', producer: 'Pheelz', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 120, key: 'C' }
      ]
    },
    {
      id: 'ybnl',
      title: 'YBNL (Yahoo Boy No Laptop)',
      slug: 'ybnl',
      type: 'Studio Album',
      releaseYear: 2012,
      releaseDate: 'November 12, 2012',
      trackCount: 20,
      duration: '1:12:40',
      coverArt: 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=600&q=80',
      label: 'YBNL Nation',
      distributor: 'YBNL Nation',
      description: 'Olamide breakthrough sophomore album and the herald of his independent record label. Featuring "First of All", "Voice of the Street", "Stupid Love" and "Ilefo Illuminati", YBNL proved his hitmaking supremacy.',
      featuredArtists: ['Kay Switch', 'Dammy Krane', 'Davido', 'Tiwa Savage', 'Reminisce', 'Samklef'],
      producers: ['Tyrone', 'Samklef', '2Kriss', 'Pheelz', 'ID Cabasa'],
      tracks: [
        { id: 'ybnl-01', number: 1, title: 'First of All', duration: '3:10', featured: '', producer: 'Tyrone', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 122, key: 'Am' },
        { id: 'ybnl-02', number: 2, title: 'Voice of the Street', duration: '3:50', featured: '', producer: 'Tyrone', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 92, key: 'Dm' },
        { id: 'ybnl-03', number: 3, title: 'Stupid Love', duration: '3:45', featured: '', producer: 'Samklef', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 120, key: 'C' },
        { id: 'ybnl-04', number: 4, title: 'Ilefo Illuminati', duration: '3:30', featured: '', producer: '2Kriss', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 115, key: 'Em' }
      ]
    },
    {
      id: 'rapsodi',
      title: 'Rapsodi',
      slug: 'rapsodi',
      type: 'Studio Album',
      releaseYear: 2011,
      releaseDate: 'March 14, 2011',
      trackCount: 16,
      duration: '58:24',
      coverArt: 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=600&q=80',
      label: 'Coded Tunes / NotJustOk',
      distributor: 'Coded Tunes',
      description: 'The iconic debut album that introduced Olamide Adedeji from Bariga to the world. Anchored by the groundbreaking breakout single "Eni Duro" and featuring Wizkid on "Omo To Shan".',
      featuredArtists: ['Wizkid', 'ID Cabasa', 'Reminisce', '9ice', 'D\'Banj', 'Lord of Ajasa'],
      producers: ['ID Cabasa'],
      tracks: [
        { id: 'rap-01', number: 1, title: 'Eni Duro', duration: '4:15', featured: '', producer: 'ID Cabasa', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 98, key: 'Am' },
        { id: 'rap-02', number: 2, title: 'Omo To Shan', duration: '3:40', featured: 'Wizkid', producer: 'ID Cabasa', status: 'JUSTBADDO_STREAMING', isPlayable: true, bpm: 104, key: 'F' },
        { id: 'rap-03', number: 3, title: 'Apa Ti Jona', duration: '3:52', featured: 'ID Cabasa', producer: 'ID Cabasa', status: 'AUTHORISED_PROVIDER', isPlayable: true, bpm: 100, key: 'Dm' },
        { id: 'rap-04', number: 4, title: 'Legendary Hustlers', duration: '4:02', featured: 'Reminisce & 9ice', producer: 'ID Cabasa', status: 'METADATA_ONLY', isPlayable: false, bpm: 94, key: 'Em' }
      ]
    }
  ],

  singlesAndFeatures: [
    { id: 's-01', title: 'Motigbana', releaseYear: 2018, type: 'Single', duration: '3:15', producer: 'Killertunes', featured: '', status: 'JUSTBADDO_STREAMING', isPlayable: true, coverArt: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80' },
    { id: 's-02', title: 'Science Student', releaseYear: 2018, type: 'Single', duration: '3:42', producer: 'Young Jonn & BBanks', featured: '', status: 'JUSTBADDO_STREAMING', isPlayable: true, coverArt: 'https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=400&q=80' },
    { id: 's-03', title: 'Kana', releaseYear: 2018, type: 'Single', duration: '3:48', producer: 'Mut4y', featured: 'Wizkid', status: 'AUTHORISED_PROVIDER', isPlayable: true, coverArt: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=400&q=80' },
    { id: 's-04', title: 'Poverty Die', releaseYear: 2018, type: 'Single', duration: '3:20', producer: 'Pheelz', featured: '', status: 'JUSTBADDO_STREAMING', isPlayable: true, coverArt: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80' },
    { id: 's-05', title: 'Woske', releaseYear: 2019, type: 'Single', duration: '3:05', producer: 'Killertunes', featured: '', status: 'JUSTBADDO_STREAMING', isPlayable: true, coverArt: 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=400&q=80' },
    { id: 's-06', title: 'Oil & Gas', releaseYear: 2019, type: 'Single', duration: '3:00', producer: 'Pheelz', featured: '', status: 'JUSTBADDO_STREAMING', isPlayable: true, coverArt: 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=400&q=80' },
    { id: 's-07', title: 'Pawon', releaseYear: 2019, type: 'Single', duration: '3:10', producer: 'Cracker Mallo', featured: '', status: 'AUTHORISED_PROVIDER', isPlayable: true, coverArt: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=400&q=80' },
    { id: 's-08', title: 'Omo Ologo', releaseYear: 2022, type: 'Single', duration: '2:12', producer: 'B-Bankz', featured: '', status: 'JUSTBADDO_STREAMING', isPlayable: true, coverArt: 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=400&q=80' }
  ],

  playlists: [
    {
      id: 'pl-baddo-essentials',
      title: 'Baddo Essentials',
      creator: 'JustBaddo Editorial',
      description: 'The defining anthems spanning Bariga beginnings, street classics, to world-class modern afrobeats.',
      coverArt: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=600&q=80',
      trackIds: ['ikigai-02', 'unruly-08', 'cd-03', 'ln-09', 'em-03', 'bgel-03', 'ybnl-01', 'rap-01']
    },
    {
      id: 'pl-street-anthems',
      title: 'Bariga to the World: Street Anthems',
      creator: 'JustBaddo Editorial',
      description: 'High-octane street sound, iconic slangs and unrelenting energy from YBNL chief.',
      coverArt: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80',
      trackIds: ['sot-02', 'sot-03', 'ln-09', 'em-05', 'ybnl-02', 'tg-06', 's-01', 's-02']
    },
    {
      id: 'pl-mellow-baddo',
      title: 'Midnight Baddo: Melodic & Intimate',
      creator: 'JustBaddo Editorial',
      description: 'Sublime acoustics, relaxed afrobeats tempo and soulful reflections from Carpe Diem and UY Scuti.',
      coverArt: 'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=600&q=80',
      trackIds: ['uy-03', 'uy-04', 'cd-02', 'cd-11', 'unruly-06', 'em-06', 'ikigai-01']
    }
  ]
};

// Helper methods for easy querying
window.JUSTBADDO_CATALOGUE.getAlbumBySlug = function(slug) {
  return this.albums.find(a => a.slug === slug || a.id === slug);
};

window.JUSTBADDO_CATALOGUE.getTrackById = function(trackId) {
  for (const album of this.albums) {
    const track = album.tracks.find(t => t.id === trackId);
    if (track) {
      return { ...track, albumTitle: album.title, albumCover: album.coverArt, albumSlug: album.slug };
    }
  }
  const single = this.singlesAndFeatures.find(s => s.id === trackId);
  if (single) {
    return { ...single, albumTitle: single.type, albumCover: single.coverArt, albumSlug: 'singles' };
  }
  return null;
};

window.JUSTBADDO_CATALOGUE.getAllPlayableTracks = function() {
  const list = [];
  this.albums.forEach(album => {
    album.tracks.forEach(track => {
      if (track.isPlayable) {
        list.push({ ...track, albumTitle: album.title, albumCover: album.coverArt, albumSlug: album.slug });
      }
    });
  });
  this.singlesAndFeatures.forEach(single => {
    if (single.isPlayable) {
      list.push({ ...single, albumTitle: single.type, albumCover: single.coverArt, albumSlug: 'singles' });
    }
  });
  return list;
};
