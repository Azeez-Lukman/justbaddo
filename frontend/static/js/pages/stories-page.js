/**
 * JUSTBADDO — Fan Stories Page Logic
 * Renders editorial fan essays, handles story reader modal, and story submission.
 */

document.addEventListener('DOMContentLoaded', () => {
  const storiesContainer = document.getElementById('jb-stories-list');
  const readerModal = document.getElementById('jb-story-reader-modal');

  function renderStories() {
    if (!storiesContainer) return;
    const stories = JUSTBADDO_STORIES;

    storiesContainer.innerHTML = stories.map(story => `
      <article class="group p-6 rounded-3xl bg-zinc-900/60 border border-zinc-800 hover:border-zinc-700 transition-all flex flex-col justify-between">
        <div>
          <div class="aspect-video rounded-2xl overflow-hidden mb-5 bg-zinc-950">
            <img src="${story.coverImage}" alt="${story.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
          </div>
          <div class="flex items-center gap-2 mb-3">
            <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">${story.tags[0] || 'Fan Reflection'}</span>
            <span class="text-xs text-zinc-500 font-mono">${story.readTime}</span>
          </div>
          <h3 class="text-lg font-bold text-zinc-100 group-hover:text-amber-400 transition-colors mb-2 leading-snug">${story.title}</h3>
          <p class="text-xs text-zinc-400 leading-relaxed line-clamp-3 mb-4">${story.excerpt}</p>
        </div>

        <div class="pt-4 border-t border-zinc-800/80 flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <img src="${story.authorAvatar}" alt="${story.author}" class="w-8 h-8 rounded-full object-cover border border-zinc-700">
            <div>
              <h5 class="text-xs font-semibold text-zinc-200">${story.author}</h5>
              <span class="text-[10px] text-zinc-500">${story.authorRole}</span>
            </div>
          </div>
          <button class="px-4 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold transition-colors" data-read-story-id="${story.id}">
            Read Story
          </button>
        </div>
      </article>
    `).join('');

    JustBaddoUI.refreshIcons();
  }

  function openStoryReader(storyId) {
    const story = JUSTBADDO_STORIES.find(s => s.id === storyId);
    if (!story) return;

    const titleEl = document.getElementById('jb-reader-title');
    const authorEl = document.getElementById('jb-reader-author');
    const dateEl = document.getElementById('jb-reader-date');
    const contentEl = document.getElementById('jb-reader-content');
    const coverEl = document.getElementById('jb-reader-cover');

    if (titleEl) titleEl.textContent = story.title;
    if (authorEl) authorEl.textContent = `${story.author} (${story.authorRole})`;
    if (dateEl) dateEl.textContent = `${story.date} • ${story.readTime}`;
    if (contentEl) contentEl.innerHTML = story.content;
    if (coverEl) coverEl.src = story.coverImage;

    JustBaddoUI.openModal('jb-story-reader-modal');
  }

  document.addEventListener('click', (e) => {
    const readBtn = e.target.closest('[data-read-story-id]');
    if (readBtn) {
      const storyId = readBtn.getAttribute('data-read-story-id');
      openStoryReader(storyId);
      return;
    }

    // Submit story form
    const submitStoryForm = e.target.closest('#jb-submit-story-form');
    if (submitStoryForm) {
      e.preventDefault();
      const titleInput = document.getElementById('jb-story-submit-title');
      const textInput = document.getElementById('jb-story-submit-content');
      if (titleInput && textInput && titleInput.value.trim() && textInput.value.trim()) {
        JUSTBADDO_STORIES.unshift({
          id: 'story-' + Date.now(),
          title: titleInput.value.trim(),
          author: JUSTBADDO_COMMUNITY.currentUser.displayName,
          authorRole: 'Community Member',
          authorAvatar: JUSTBADDO_COMMUNITY.currentUser.avatar,
          date: 'Just now',
          readTime: '3 min read',
          coverImage: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80',
          excerpt: textInput.value.trim().substring(0, 140) + '...',
          content: `<p class="mb-4 text-zinc-300 leading-relaxed">${textInput.value.trim()}</p>`,
          likes: 1,
          tags: ['Community Submission']
        });
        renderStories();
        JustBaddoUI.closeModal('jb-submit-story-modal');
        titleInput.value = '';
        textInput.value = '';
        JustBaddoUI.toast('Your story was submitted for community publication!', 'success');
      }
    }
  });

  renderStories();
});
