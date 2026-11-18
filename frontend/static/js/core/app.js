/**
 * JUSTBADDO — Global Application Coordinator
 * Boots state, player, UI listeners, navigation highlights, and keyboard shortcuts.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize State & Storage
  if (window.JustBaddoState) {
    JustBaddoState.init();
  }

  // 2. Initialize UI & Icons
  if (window.JustBaddoUI) {
    JustBaddoUI.init();
  }

  // 3. Initialize Audio Player Engine
  if (window.JustBaddoPlayer) {
    JustBaddoPlayer.init();
  }

  // 4. Initialize Queue Manager
  if (window.JustBaddoQueue) {
    JustBaddoQueue.init();
  }

  // 5. Initialize Playlists Controller
  if (window.JustBaddoPlaylists) {
    JustBaddoPlaylists.init();
  }

  // 6. Navigation highlighting & Mobile Drawer
  setupNavigation();

  // 7. Global Keyboard Shortcuts
  setupKeyboardShortcuts();

  // 8. Global Quick Search Handler
  setupQuickSearch();
});

function setupNavigation() {
  // Mobile drawer toggle
  const mobileMenuBtn = document.getElementById('jb-mobile-menu-btn');
  const mobileDrawer = document.getElementById('jb-mobile-drawer');
  const mobileDrawerClose = document.getElementById('jb-mobile-drawer-close');

  if (mobileMenuBtn && mobileDrawer) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileDrawer.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
      JustBaddoUI.refreshIcons();
    });
  }

  if (mobileDrawerClose && mobileDrawer) {
    mobileDrawerClose.addEventListener('click', () => {
      mobileDrawer.classList.add('hidden');
      document.body.style.overflow = '';
    });
  }

  // Highlight current active nav item
  const currentPath = window.location.pathname.toLowerCase();
  document.querySelectorAll('.jb-nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    const isHome = (href === '/' || href.endsWith('index.html')) && (currentPath.endsWith('/') || currentPath.endsWith('index.html') || currentPath === '');
    const isMatch = href !== '/' && currentPath.includes(href.replace('../', '').replace('./', ''));
    if (isHome || isMatch) {
      link.classList.add('text-amber-400', 'font-semibold');
      link.classList.remove('text-zinc-400');
    }
  });
}

function setupKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // If active in an input/textarea, do not capture media keys
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
      return;
    }

    // Spacebar toggles playback
    if (e.code === 'Space') {
      e.preventDefault();
      if (window.JustBaddoPlayer) {
        JustBaddoPlayer.togglePlay();
      }
    }

    // '/' key focuses global search bar
    if (e.key === '/') {
      e.preventDefault();
      const searchInput = document.querySelector('.jb-global-search-input');
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
    }
  });
}

function setupQuickSearch() {
  document.querySelectorAll('.jb-search-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('input[type="search"], input[type="text"]');
      if (input && input.value.trim()) {
        const query = encodeURIComponent(input.value.trim());
        // Check if we are inside /pages or root
        const isInPages = window.location.pathname.includes('/pages/');
        const targetUrl = isInPages ? `search.html?q=${query}` : `pages/search.html?q=${query}`;
        window.location.href = targetUrl;
      }
    });
  });
}
