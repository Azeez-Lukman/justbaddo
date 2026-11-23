/**
 * JUSTBADDO — Community Feed & Interactive Discussions
 * Manages post composition, like reactions, threaded comments, and feed category filters.
 */

window.JustBaddoCommunity = {
  activeCategory: 'All',

  init() {
    this.renderPosts();
    this.bindEvents();
    this.loadFromBackend();
  },

  async loadFromBackend() {
    if (!window.JustBaddoApi) return;
    try {
      const res = await window.JustBaddoApi.community.getFeed(this.activeCategory);
      if (res && res.data && Array.isArray(res.data) && res.data.length > 0) {
        JUSTBADDO_COMMUNITY.posts = res.data.map(p => ({
          id: p.id,
          author: {
            id: p.author?.id || 'auth-1',
            name: p.author?.display_name || p.author?.username || 'Fan Citizen',
            handle: `@${p.author?.username || 'baddofan'}`,
            avatar: p.author?.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80',
            badge: p.author?.badge || 'Bariga Club'
          },
          timeAgo: p.created_at || 'Recently',
          category: p.category || 'General',
          title: p.title,
          content: p.content,
          likes: p.likes_count || 0,
          isLiked: p.is_liked || false,
          commentsCount: p.comments_count || (p.comments ? p.comments.length : 0),
          sharesCount: 0,
          comments: (p.comments || []).map(c => ({
            id: c.id,
            author: c.author?.display_name || c.author?.username || 'Community Fan',
            avatar: c.author?.avatar_url || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=120&q=80',
            time: c.created_at || 'Just now',
            text: c.content
          }))
        }));
        this.renderPosts();
      }
    } catch (e) {
      // Keep demo fallback
    }
  },

  renderPosts() {
    const container = document.getElementById('jb-community-feed');
    if (!container) return;

    let posts = JUSTBADDO_COMMUNITY.posts;
    if (this.activeCategory !== 'All') {
      posts = posts.filter(p => p.category === this.activeCategory);
    }

    if (!posts || posts.length === 0) {
      container.innerHTML = `
        <div class="p-12 text-center rounded-2xl border border-zinc-800 bg-zinc-900/40">
          <i data-lucide="message-square" class="w-10 h-10 mx-auto text-zinc-600 mb-3"></i>
          <h4 class="text-zinc-300 font-medium">No discussions in this category yet</h4>
          <p class="text-xs text-zinc-500 mt-1">Start the first conversation below!</p>
        </div>
      `;
      JustBaddoUI.refreshIcons();
      return;
    }

    container.innerHTML = posts.map(post => {
      const isLiked = post.isLiked;
      return `
        <article class="p-6 rounded-2xl border border-zinc-800/80 bg-zinc-900/50 hover:border-zinc-700/80 transition-all duration-200" data-post-id="${post.id}">
          <!-- Post Header -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <img src="${post.author.avatar}" alt="${post.author.name}" class="w-10 h-10 rounded-full object-cover border border-zinc-700">
              <div>
                <div class="flex items-center gap-2">
                  <h4 class="text-sm font-semibold text-zinc-100">${post.author.name}</h4>
                  ${post.author.badge ? `<span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">${post.author.badge}</span>` : ''}
                </div>
                <div class="flex items-center gap-2 text-xs text-zinc-400">
                  <span>${post.author.handle}</span>
                  <span>•</span>
                  <span>${post.timeAgo}</span>
                </div>
              </div>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-md bg-zinc-800 text-zinc-400 font-medium">${post.category}</span>
          </div>

          <!-- Post Content -->
          <h3 class="text-base font-bold text-zinc-100 mb-2 leading-snug">${post.title}</h3>
          <p class="text-sm text-zinc-300 leading-relaxed mb-4">${post.content}</p>

          ${post.taggedTrack ? `
            <div class="flex items-center justify-between p-3 rounded-xl bg-zinc-950/60 border border-zinc-800 mb-4 group cursor-pointer" data-play-track-id="${post.taggedTrack.id}">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 group-hover:bg-amber-500 group-hover:text-black transition-colors">
                  <i data-lucide="play" class="w-4 h-4 fill-current"></i>
                </div>
                <div>
                  <h5 class="text-xs font-semibold text-zinc-200 group-hover:text-amber-400 transition-colors">${post.taggedTrack.title}</h5>
                  <p class="text-[11px] text-zinc-500">${post.taggedTrack.album}</p>
                </div>
              </div>
              <span class="text-[11px] text-amber-500 font-medium">Listen Track</span>
            </div>
          ` : ''}

          <!-- Post Footer Controls -->
          <div class="flex items-center justify-between pt-4 border-t border-zinc-800/60 text-xs text-zinc-400">
            <div class="flex items-center gap-6">
              <button class="flex items-center gap-1.5 transition-colors ${isLiked ? 'text-rose-500 font-semibold' : 'hover:text-rose-400'}" data-action-like-post="${post.id}">
                <i data-lucide="heart" class="w-4 h-4 ${isLiked ? 'fill-rose-500' : ''}"></i>
                <span>${post.likes}</span>
              </button>
              <button class="flex items-center gap-1.5 hover:text-zinc-200 transition-colors" data-action-toggle-comments="${post.id}">
                <i data-lucide="message-circle" class="w-4 h-4"></i>
                <span>${post.commentsCount || (post.comments ? post.comments.length : 0)}</span>
              </button>
              <button class="flex items-center gap-1.5 hover:text-amber-400 transition-colors" data-action-share-post="${post.id}">
                <i data-lucide="share-2" class="w-4 h-4"></i>
                <span>${post.sharesCount || 0}</span>
              </button>
            </div>
            <button class="hover:text-zinc-200 text-xs flex items-center gap-1" data-action-bookmark-post="${post.id}">
              <i data-lucide="bookmark" class="w-4 h-4"></i>
              <span>Save</span>
            </button>
          </div>

          <!-- Threaded Comments Section -->
          <div class="jb-comments-container hidden mt-4 pt-4 border-t border-zinc-800/80" id="comments-${post.id}">
            <div class="space-y-3 mb-4">
              ${(post.comments && post.comments.length > 0) ? post.comments.map(c => `
                <div class="flex items-start gap-3 p-3 rounded-xl bg-zinc-950/40 border border-zinc-800/40 text-xs">
                  <img src="${c.avatar}" alt="${c.author}" class="w-7 h-7 rounded-full object-cover shrink-0">
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between mb-1">
                      <span class="font-semibold text-zinc-200">${c.author}</span>
                      <span class="text-zinc-500 text-[10px]">${c.time}</span>
                    </div>
                    <p class="text-zinc-300">${c.text}</p>
                  </div>
                </div>
              `).join('') : '<p class="text-xs text-zinc-500">No comments yet. Join the conversation below.</p>'}
            </div>

            <!-- Comment Input -->
            <form class="flex items-center gap-2" data-submit-comment="${post.id}">
              <input type="text" placeholder="Write a thoughtful reply..." class="flex-1 bg-zinc-950 border border-zinc-800 focus:border-amber-500/80 rounded-xl px-3 py-2 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none transition-colors" required>
              <button type="submit" class="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-semibold text-xs transition-colors shrink-0">
                Reply
              </button>
            </form>
          </div>
        </article>
      `;
    }).join('');

    JustBaddoUI.refreshIcons();
  },

  bindEvents() {
    document.addEventListener('click', (e) => {
      // Category filter buttons
      const catBtn = e.target.closest('[data-community-category]');
      if (catBtn) {
        document.querySelectorAll('[data-community-category]').forEach(btn => {
          btn.classList.remove('bg-amber-500', 'text-black', 'font-semibold');
          btn.classList.add('bg-zinc-900', 'text-zinc-400', 'hover:text-white');
        });
        catBtn.classList.remove('bg-zinc-900', 'text-zinc-400', 'hover:text-white');
        catBtn.classList.add('bg-amber-500', 'text-black', 'font-semibold');
        this.activeCategory = catBtn.getAttribute('data-community-category');
        this.renderPosts();
        return;
      }

      // Like post action
      const likeBtn = e.target.closest('[data-action-like-post]');
      if (likeBtn) {
        e.preventDefault();
        const postId = likeBtn.getAttribute('data-action-like-post');
        const post = JUSTBADDO_COMMUNITY.posts.find(p => p.id === postId);
        if (post) {
          post.isLiked = !post.isLiked;
          post.likes += post.isLiked ? 1 : -1;
          this.renderPosts();
          JustBaddoUI.toast(post.isLiked ? 'Liked post' : 'Unliked post', 'info');

          if (window.JustBaddoApi && !postId.startsWith('post-demo')) {
            window.JustBaddoApi.community.toggleLike(postId).catch(err => {
              console.warn('[Community Like Sync]', err.message);
            });
          }
        }
        return;
      }

      // Toggle comments
      const commentToggleBtn = e.target.closest('[data-action-toggle-comments]');
      if (commentToggleBtn) {
        e.preventDefault();
        const postId = commentToggleBtn.getAttribute('data-action-toggle-comments');
        const commentsDiv = document.getElementById(`comments-${postId}`);
        if (commentsDiv) {
          commentsDiv.classList.toggle('hidden');
          JustBaddoUI.refreshIcons();
        }
        return;
      }

      // Share post
      const shareBtn = e.target.closest('[data-action-share-post]');
      if (shareBtn) {
        e.preventDefault();
        navigator.clipboard?.writeText(window.location.href);
        JustBaddoUI.toast('Post link copied to clipboard', 'success');
        return;
      }

      // Bookmark post
      const bookmarkBtn = e.target.closest('[data-action-bookmark-post]');
      if (bookmarkBtn) {
        e.preventDefault();
        JustBaddoUI.toast('Saved post to your reading list', 'info');
        return;
      }
    });

    // Handle Comment Submit
    document.addEventListener('submit', (e) => {
      const commentForm = e.target.closest('[data-submit-comment]');
      if (commentForm) {
        e.preventDefault();
        if (window.JustBaddoUI && !window.JustBaddoUI.requireAuth('post a reply')) return;
        const postId = commentForm.getAttribute('data-submit-comment');
        const input = commentForm.querySelector('input');
        const text = input ? input.value.trim() : '';
        if (!text) return;

        const post = JUSTBADDO_COMMUNITY.posts.find(p => p.id === postId);
        if (post) {
          if (!post.comments) post.comments = [];
          post.comments.push({
            id: 'c-' + Date.now(),
            author: JUSTBADDO_COMMUNITY.currentUser.displayName,
            avatar: JUSTBADDO_COMMUNITY.currentUser.avatar,
            time: 'Just now',
            text: text
          });
          post.commentsCount = post.comments.length;
          this.renderPosts();
          const targetComments = document.getElementById(`comments-${postId}`);
          if (targetComments) targetComments.classList.remove('hidden');
          JustBaddoUI.toast('Reply posted', 'success');

          if (window.JustBaddoApi && !postId.startsWith('post-demo')) {
            window.JustBaddoApi.community.addComment(postId, text).catch(err => {
              console.warn('[Comment Sync]', err.message);
            });
          }
        }
        return;
      }

      // Handle New Post Submit
      const createPostForm = e.target.closest('#jb-create-post-form');
      if (createPostForm) {
        e.preventDefault();
        if (window.JustBaddoUI && !window.JustBaddoUI.requireAuth('start a discussion')) return;
        const titleInput = document.getElementById('jb-post-title');
        const contentInput = document.getElementById('jb-post-content');
        const categorySelect = document.getElementById('jb-post-category');

        const title = titleInput ? titleInput.value.trim() : '';
        const content = contentInput ? contentInput.value.trim() : '';
        const category = categorySelect ? categorySelect.value : 'Discussion';

        if (!title || !content) {
          JustBaddoUI.toast('Please write a title and content for your post', 'warning');
          return;
        }

        const newPost = {
          id: 'post-' + Date.now(),
          author: {
            id: JUSTBADDO_COMMUNITY.currentUser.id,
            name: JUSTBADDO_COMMUNITY.currentUser.displayName,
            handle: JUSTBADDO_COMMUNITY.currentUser.handle,
            avatar: JUSTBADDO_COMMUNITY.currentUser.avatar,
            badge: 'Bariga Club'
          },
          timeAgo: 'Just now',
          category: category,
          title: title,
          content: content,
          likes: 1,
          isLiked: true,
          commentsCount: 0,
          sharesCount: 0,
          comments: []
        };

        JUSTBADDO_COMMUNITY.posts.unshift(newPost);
        this.renderPosts();

        if (window.JustBaddoApi) {
          window.JustBaddoApi.community.createPost({
            title: title,
            content: content,
            category: category
          }).then(res => {
            if (res && res.data && res.data.id) {
              newPost.id = res.data.id;
            }
          }).catch(err => console.warn('[Post Create Sync]', err.message));
        }

        if (titleInput) titleInput.value = '';
        if (contentInput) contentInput.value = '';
        JustBaddoUI.closeModal('jb-create-post-modal');
        JustBaddoUI.toast('Your discussion has been published to the community!', 'success');
      }
    });
  }
};
