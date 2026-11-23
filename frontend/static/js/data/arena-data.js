/**
 * JUSTBADDO — Fan Arena Demonstration Data
 * Contains interactive polls, song battles, verified trivia quizzes and leaderboard rankings.
 * All quiz facts are verified against public records, album credits and official awards.
 */

window.JUSTBADDO_ARENA = {
  polls: [
    {
      id: 'poll-time-and-space',
      question: 'Which track on Time and Space (2026) defines this new era for you?',
      description: 'Ten tracks, zero filler. Vote on your standout track from Olamide 11th studio album.',
      totalVotes: 1140,
      hasVoted: false,
      userVotedOption: null,
      options: [
        { id: 'opt-ts-1', text: 'Elohim (Opening Statement)', votes: 285, percentage: 25 },
        { id: 'opt-ts-2', text: 'Jaiye (feat. FOLA)', votes: 513, percentage: 45 },
        { id: 'opt-ts-3', text: 'Say Less', votes: 194, percentage: 17 },
        { id: 'opt-ts-4', text: 'Jogor (Closing Statement)', votes: 148, percentage: 13 }
      ]
    },
    {
      id: 'poll-01',
      question: 'Which Olamide release era represents his peak cultural impact?',
      description: 'Vote on the period that most profoundly transformed Nigerian popular culture.',
      totalVotes: 1420,
      hasVoted: false,
      userVotedOption: null,
      options: [
        { id: 'opt-1', text: 'Street Supremacy (Rapsodi & YBNL: 2011–2012)', votes: 312, percentage: 22 },
        { id: 'opt-2', text: 'Golden Anthems (BGEL & Street OT: 2013–2014)', votes: 568, percentage: 40 },
        { id: 'opt-3', text: 'Solo Domination (Eyan Mayweather & The Glory: 2015–2016)', votes: 284, percentage: 20 },
        { id: 'opt-4', text: 'Global Master (Carpe Diem & UY Scuti: 2020–2021)', votes: 256, percentage: 18 }
      ]
    },
    {
      id: 'poll-02',
      question: 'Best album opening track across the discography?',
      description: 'Which opening song set the highest bar for the album that followed?',
      totalVotes: 890,
      hasVoted: false,
      userVotedOption: null,
      options: [
        { id: 'opt-2a', text: 'Voice of the Street (YBNL, 2012)', votes: 410, percentage: 46 },
        { id: 'opt-2b', text: 'The Glory Intro (The Glory, 2016)', votes: 240, percentage: 27 },
        { id: 'opt-2c', text: 'Another Level (Carpe Diem, 2020)', votes: 130, percentage: 15 },
        { id: 'opt-2d', text: 'Celebrate (Unruly, 2023)', votes: 110, percentage: 12 }
      ]
    }
  ],

  battles: [
    {
      id: 'battle-01',
      title: 'The Viral Dance Clash',
      category: 'Street Anthems',
      description: 'Two colossal national anthems that conquered party floors across Africa and the diaspora.',
      totalVotes: 2314,
      hasVoted: false,
      userVotedSong: null,
      trackA: {
        id: 'ln-09',
        title: 'Wo!!',
        album: 'Lagos Nawa (2017)',
        producer: 'Young Jonn',
        releaseYear: 2017,
        coverArt: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80',
        votes: 1250,
        percentage: 54
      },
      trackB: {
        id: 'em-03',
        title: 'Bobo (Shakiti Bobo)',
        album: 'Eyan Mayweather (2015)',
        producer: 'Young Jonn',
        releaseYear: 2015,
        coverArt: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=400&q=80',
        votes: 1064,
        percentage: 46
      }
    },
    {
      id: 'battle-02',
      title: 'The Melodic Fusion Face-off',
      category: 'Collaborations',
      description: 'Mid-tempo masterclasses that showcased Olamide seamless bridge between rap and afrobeats.',
      totalVotes: 1840,
      hasVoted: false,
      userVotedSong: null,
      trackA: {
        id: 'cd-03',
        title: 'Infinity',
        featured: 'feat. Omah Lay',
        album: 'Carpe Diem (2020)',
        producer: 'P.Priime',
        releaseYear: 2020,
        coverArt: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=400&q=80',
        votes: 1012,
        percentage: 55
      },
      trackB: {
        id: 'cd-07',
        title: 'Loading',
        featured: 'feat. Bad Boy Timz',
        album: 'Carpe Diem (2020)',
        producer: 'P.Priime',
        releaseYear: 2020,
        coverArt: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=400&q=80',
        votes: 828,
        percentage: 45
      }
    }
  ],

  quizzes: [
    {
      id: 'quiz-01',
      title: 'The Baddo Discography Master Quiz',
      subtitle: 'Test your knowledge on verified releases, producers and historic milestones.',
      difficulty: 'Intermediate',
      pointsReward: 300,
      questions: [
        {
          id: 'q1',
          question: 'Which legendary Nigerian producer signed and executive-produced Olamide debut album "Rapsodi"?',
          options: ['Don Jazzy', 'ID Cabasa', 'Sarz', 'Cobhams Asuquo'],
          correctIndex: 1,
          explanation: 'ID Cabasa signed Olamide to Coded Tunes and produced the landmark breakout single "Eni Duro" as well as the majority of Rapsodi.'
        },
        {
          id: 'q2',
          question: 'What is the full title of Olamide iconic 2012 sophomore album abbreviated as "YBNL"?',
          options: ['Young Boys Never Lose', 'Yahoo Boy No Laptop', 'Youth Brigade Nigeria Limited', 'Yoruba Boy Natural Lyricist'],
          correctIndex: 1,
          explanation: 'YBNL stands for "Yahoo Boy No Laptop", declaring honest hustle through music rather than cyber fraud.'
        },
        {
          id: 'q3',
          question: 'Which 2015 studio album by Olamide contained 21 songs with zero featured guest artists?',
          options: ['Street OT', 'The Glory', 'Eyan Mayweather', 'Lagos Nawa'],
          correctIndex: 2,
          explanation: 'Eyan Mayweather was released in November 2015 with 21 solo tracks including Bobo and Melo Melo.'
        },
        {
          id: 'q4',
          question: 'At The Headies 2014, which project won both "Album of the Year" and "Best Rap Album"?',
          options: ['Baddest Guy Ever Liveth (BGEL)', 'Rapsodi', 'YBNL', 'Street OT'],
          correctIndex: 0,
          explanation: 'Baddest Guy Ever Liveth won Album of the Year and Best Rap Album at The Headies 2014.'
        },
        {
          id: 'q5',
          question: 'What international record and distribution company signed a joint venture with YBNL Nation in 2020 prior to "Carpe Diem"?',
          options: ['Sony Music', 'Universal Music Group', 'EMPIRE', 'Warner Music'],
          correctIndex: 2,
          explanation: 'In early 2020, Olamide announced a historic joint venture deal between YBNL Nation and EMPIRE.'
        },
        {
          id: 'q6',
          question: 'On Olamide\'s 2026 album "Time and Space", which rising artist is the sole featured guest on "Jaiye"?',
          options: ['Asake', 'FOLA', 'Fireboy DML', 'CKay'],
          correctIndex: 1,
          explanation: 'FOLA is the sole featured guest artist on Time and Space, appearing on track 7 "Jaiye".'
        }
      ]
    }
  ],

  leaderboard: [
    { rank: 1, name: 'Tunde Adeyemi', handle: '@BarigaBoy_92', points: 3450, badge: 'Bariga Veteran', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80' },
    { rank: 2, name: 'Folake Lawal', handle: '@FolakeVibes', points: 3120, badge: 'Lead Curator', avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=150&q=80' },
    { rank: 3, name: 'Chinedu Eze', handle: '@LagosNawaLover', points: 2890, badge: 'Arena Master', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80' },
    { rank: 4, name: 'Amina Bello', handle: '@AminatAfro', points: 2540, badge: 'Discography Expert', avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=150&q=80' },
    { rank: 5, name: 'Damola O.', handle: '@KolewerkFan', points: 2210, badge: 'Trivia Sharp', avatar: 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=150&q=80' }
  ]
};
