/**
 * JUSTBADDO — Global UI Manager
 * Handles authentication-aware navigation, toast alerts, modal dialogs,
 * keyboard accessibility, tab switching, dropdowns, and icon hydration.
 */

window.JustBaddoUI = {
  init() {
    this.setupToastsContainer();
    this.setupDropdownListeners();
    this.setupModalDismissListeners();
    this.setupAuthUI();
    this.refreshIcons();
  },

  getInitials(name) {
    if (!name) return 'JB';
    const parts = name.trim().split(/\s+/);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.slice(0, 2).toUpperCase();
  },

  setupAuthUI() {
    if (!window.JustBaddoState) return;

    const renderAuthElements = (user) => {
      const userMenu = document.getElementById('jb-user-menu');
      const userToggle = document.querySelector('[data-dropdown-toggle="jb-user-menu"]');
      const mobileDrawer = document.getElementById('jb-mobile-drawer');
      const currentPath = window.location.pathname + window.location.search;

      if (!userMenu) return;

      if (user) {
        // ================= AUTHENTICATED MEMBER STATE =================
        const displayName = user.display_name || user.username || 'Baddo Citizen';
        const initials = this.getInitials(displayName);
        const fanTier = user.fan_tier || 'Day One Disciple';
        const username = user.username || 'member';

        // Update trigger button (Avatar or Initials Monogram)
        if (userToggle) {
          userToggle.setAttribute('aria-label', `Account menu for ${displayName}`);
          if (user.avatar_url) {
            userToggle.innerHTML = `
              <img src="${user.avatar_url}" alt="${displayName}" onerror="this.onerror=null;this.parentElement.innerHTML='<div class=\\'w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-gradient-to-tr from-amber-600 to-amber-400 text-black font-extrabold text-xs flex items-center justify-center select-none shadow-sm shadow-amber-500/20\\'>${initials}</div>';" class="w-7 h-7 sm:w-8 sm:h-8 rounded-full object-cover shrink-0">
            `;
          } else {
            userToggle.innerHTML = `
              <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-gradient-to-tr from-amber-600 to-amber-400 text-black font-extrabold text-xs flex items-center justify-center select-none shadow-sm shadow-amber-500/20">${initials}</div>
            `;
          }
        }

        // Render full Member Account Menu
        userMenu.innerHTML = `
          <div class="px-3 py-2.5 border-b border-zinc-800 mb-1">
            <div class="flex items-center gap-2.5">
              ${user.avatar_url 
                ? `<img src="${user.avatar_url}" alt="${displayName}" onerror="this.onerror=null;this.parentElement.innerHTML='<div class=\\'w-7 h-7 rounded-full bg-gradient-to-tr from-amber-600 to-amber-400 text-black font-extrabold text-xs flex items-center justify-center select-none\\'>${initials}</div>';" class="w-7 h-7 rounded-full object-cover shrink-0">`
                : `<div class="w-7 h-7 rounded-full bg-gradient-to-tr from-amber-600 to-amber-400 text-black font-extrabold text-xs flex items-center justify-center select-none">${initials}</div>`
              }
              <div class="min-w-0 flex-1">
                <h5 class="text-xs font-bold text-zinc-100 truncate">${displayName}</h5>
                <span class="text-[10px] text-amber-500 font-medium block truncate">@${username} • ${fanTier}</span>
              </div>
            </div>
          </div>

          <div class="space-y-0.5 py-1">
            <a href="/pages/profile.html" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors">
              <i data-lucide="user" class="w-4 h-4 text-zinc-400"></i>
              <span>My Profile</span>
            </a>
            <a href="/pages/playlists.html#saved" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors">
              <i data-lucide="heart" class="w-4 h-4 text-zinc-400"></i>
              <span>Saved Music</span>
            </a>
            <a href="/pages/playlists.html" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors">
              <i data-lucide="list-music" class="w-4 h-4 text-zinc-400"></i>
              <span>My Playlists</span>
            </a>
            <a href="/pages/community.html" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors">
              <i data-lucide="message-square" class="w-4 h-4 text-zinc-400"></i>
              <span>Community</span>
            </a>
            <a href="/pages/settings.html" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors">
              <i data-lucide="settings" class="w-4 h-4 text-zinc-400"></i>
              <span>Account Settings</span>
            </a>
          </div>

          <div class="pt-1 mt-1 border-t border-zinc-800">
            <button id="jb-auth-signout-btn" class="flex items-center gap-2.5 w-full px-3 py-2 rounded-xl text-xs text-rose-400 hover:text-rose-300 hover:bg-zinc-800/80 transition-colors cursor-pointer text-left">
              <i data-lucide="log-out" class="w-4 h-4"></i>
              <span>Sign Out</span>
            </button>
          </div>
        `;

        // Wire Sign-Out handler (Instant POST-based logout with session invalidation)
        const signoutBtn = userMenu.querySelector('#jb-auth-signout-btn');
        if (signoutBtn) {
          signoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            signoutBtn.disabled = true;
            await JustBaddoState.logout();
            JustBaddoUI.toast("You've been signed out.", 'info');
            setTimeout(() => {
              window.location.href = '/';
            }, 400);
          });
        }

        // Mobile drawer updates for member
        if (mobileDrawer) {
          const authArea = mobileDrawer.querySelector('.jb-mobile-auth-area');
          if (authArea) {
            authArea.innerHTML = `
              <div class="p-3 rounded-2xl bg-zinc-900 border border-zinc-800 mb-3 flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-amber-600 to-amber-400 text-black font-extrabold text-xs flex items-center justify-center select-none">${initials}</div>
                <div class="min-w-0 flex-1">
                  <div class="text-xs font-bold text-zinc-100 truncate">${displayName}</div>
                  <div class="text-[10px] text-amber-500 font-medium">@${username}</div>
                </div>
              </div>
              <button id="jb-mobile-signout-btn" class="flex items-center justify-center gap-2 w-full py-2.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-rose-400 text-xs font-semibold transition-colors border border-zinc-800">
                <i data-lucide="log-out" class="w-4 h-4"></i>
                <span>Sign Out</span>
              </button>
            `;
            const mSignout = authArea.querySelector('#jb-mobile-signout-btn');
            if (mSignout) {
              mSignout.addEventListener('click', async () => {
                await JustBaddoState.logout();
                JustBaddoUI.toast("You've been signed out.", 'info');
                setTimeout(() => { window.location.href = '/'; }, 400);
              });
            }
          }
        }

      } else {
        // ================= GUEST VISITOR STATE =================
        // Do NOT expose account controls to guests
        if (userToggle) {
          userToggle.setAttribute('aria-label', 'Guest user options');
          userToggle.innerHTML = `
            <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-zinc-800/80 hover:bg-zinc-800 border border-zinc-700/80 text-zinc-300 flex items-center justify-center transition-colors">
              <i data-lucide="user" class="w-4 h-4"></i>
            </div>
          `;
        }

        const encodedCurrent = encodeURIComponent(currentPath);

        // Render guest action menu
        userMenu.innerHTML = `
          <div class="px-3 py-2.5 border-b border-zinc-800 mb-2">
            <h5 class="text-xs font-bold text-zinc-100">Guest Visitor</h5>
            <p class="text-[11px] text-zinc-400 mt-0.5">Explore freely or sign in to participate in the community.</p>
          </div>

          <div class="p-1 space-y-2">
            <a href="/pages/login.html?next=${encodedCurrent}" class="flex items-center justify-center gap-2 w-full py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black text-xs font-bold transition-colors shadow-sm shadow-amber-500/20">
              <i data-lucide="log-in" class="w-4 h-4"></i>
              <span>Sign In</span>
            </a>
            <a href="/pages/register.html?next=${encodedCurrent}" class="flex items-center justify-center gap-2 w-full py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold transition-colors border border-zinc-700">
              <i data-lucide="user-plus" class="w-4 h-4"></i>
              <span>Join JustBaddo</span>
            </a>
          </div>
        `;

        // Mobile drawer updates for guest
        if (mobileDrawer) {
          const authArea = mobileDrawer.querySelector('.jb-mobile-auth-area');
          if (authArea) {
            authArea.innerHTML = `
              <div class="flex flex-col gap-2 pt-4 border-t border-zinc-800">
                <a href="/pages/login.html?next=${encodedCurrent}" class="flex items-center justify-center gap-2 w-full py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black text-xs font-bold transition-colors shadow-sm shadow-amber-500/20">
                  <i data-lucide="log-in" class="w-4 h-4"></i>
                  <span>Sign In</span>
                </a>
                <a href="/pages/register.html?next=${encodedCurrent}" class="flex items-center justify-center gap-2 w-full py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold transition-colors border border-zinc-700">
                  <i data-lucide="user-plus" class="w-4 h-4"></i>
                  <span>Join JustBaddo</span>
                </a>
              </div>
            `;
          }
        }
      }

      JustBaddoUI.refreshIcons();
    };

    JustBaddoState.on('auth-changed', (user) => {
      renderAuthElements(user);
    });

    renderAuthElements(JustBaddoState.state.currentUser);
  },

  /**
   * Require authentication helper for interactive protected actions.
   * If visitor is guest, prompts contextual login modal.
   * If member hasn't accepted guidelines, prompts guidelines acceptance gate.
   */
  requireAuth(actionDescription = 'perform this action', returnUrl = null, onAuthenticatedCallback = null) {
    if (window.JustBaddoState && window.JustBaddoState.state.isAuthenticated) {
      const user = window.JustBaddoState.state.currentUser;
      if (user && user.accepted_community_guidelines === false) {
        this.showGuidelinesModal(() => {
          if (typeof onAuthenticatedCallback === 'function') onAuthenticatedCallback();
        });
        return false;
      }
      return true;
    }

    this.showAuthPromptModal(actionDescription, returnUrl);
    return false;
  },

  showAuthPromptModal(actionDescription, returnUrl = null) {
    let modal = document.getElementById('jb-contextual-auth-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'jb-contextual-auth-modal';
      modal.className = 'jb-modal fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4';
      document.body.appendChild(modal);
    }

    const target = encodeURIComponent(returnUrl || (window.location.pathname + window.location.search));

    modal.innerHTML = `
      <div class="jb-modal-backdrop fixed inset-0 bg-black/80 backdrop-blur-md" onclick="JustBaddoUI.closeContextualAuthModal()"></div>
      <div class="relative w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-3xl p-6 sm:p-8 shadow-2xl z-10 text-center animate-fadeIn">
        <div class="w-14 h-14 rounded-2xl bg-amber-500/10 text-amber-400 flex items-center justify-center mx-auto mb-4 border border-amber-500/20">
          <i data-lucide="lock" class="w-7 h-7"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-2">Member Authentication Required</h3>
        <p class="text-xs sm:text-sm text-zinc-400 leading-relaxed mb-6">
          You need an active JustBaddo member account to ${actionDescription}. Sign in to continue where you left off.
        </p>

        <div class="space-y-2.5 mb-4">
          <a href="/pages/login.html?next=${target}" class="flex items-center justify-center gap-2 w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs sm:text-sm transition-colors shadow-lg shadow-amber-500/20">
            <i data-lucide="log-in" class="w-4 h-4"></i>
            <span>Sign In to Continue</span>
          </a>
          <a href="/pages/register.html?next=${target}" class="flex items-center justify-center gap-2 w-full py-2.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 font-semibold text-xs transition-colors border border-zinc-700">
            <i data-lucide="user-plus" class="w-4 h-4"></i>
            <span>Join JustBaddo</span>
          </a>
        </div>

        <button onclick="JustBaddoUI.closeContextualAuthModal()" class="text-xs text-zinc-500 hover:text-zinc-300 transition-colors">
          Stay as Guest Visitor
        </button>
      </div>
    `;

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    this.refreshIcons();
  },

  closeContextualAuthModal() {
    const modal = document.getElementById('jb-contextual-auth-modal');
    if (modal) {
      modal.classList.add('hidden');
      document.body.style.overflow = '';
    }
  },

  showGuidelinesModal(onAccept) {
    let modal = document.getElementById('jb-guidelines-prompt-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'jb-guidelines-prompt-modal';
      modal.className = 'jb-modal fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4';
      document.body.appendChild(modal);
    }

    modal.innerHTML = `
      <div class="jb-modal-backdrop fixed inset-0 bg-black/80 backdrop-blur-md"></div>
      <div class="relative w-full max-w-lg bg-zinc-900 border border-zinc-800 rounded-3xl p-6 sm:p-8 shadow-2xl z-10 animate-fadeIn">
        <div class="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-400 flex items-center justify-center mb-4 border border-amber-500/20">
          <i data-lucide="shield-check" class="w-6 h-6"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-2">JustBaddo Community Guidelines</h3>
        <p class="text-xs text-zinc-400 leading-relaxed mb-4">
          Before contributing discussions or comments, please agree to our core community standards:
        </p>

        <ul class="space-y-2.5 text-xs text-zinc-300 mb-6 bg-zinc-950/60 p-4 rounded-2xl border border-zinc-850">
          <li class="flex items-start gap-2">
            <i data-lucide="check" class="w-4 h-4 text-amber-400 shrink-0 mt-0.5"></i>
            <span><strong>Respect fellow fans & creators:</strong> Treat all artists, fans, and eras with constructive respect. No harassment, hate speech, or abuse.</span>
          </li>
          <li class="flex items-start gap-2">
            <i data-lucide="check" class="w-4 h-4 text-amber-400 shrink-0 mt-0.5"></i>
            <span><strong>Zero Piracy / Commercial Streams:</strong> Never distribute direct copyrighted audio rips, commercial download links, or unauthorized streams.</span>
          </li>
          <li class="flex items-start gap-2">
            <i data-lucide="check" class="w-4 h-4 text-amber-400 shrink-0 mt-0.5"></i>
            <span><strong>No Spam or Vote Rigging:</strong> Keep discussions meaningful and avoid automated voting or repetitive low-effort spam.</span>
          </li>
        </ul>

        <button id="jb-accept-guidelines-btn" class="flex items-center justify-center gap-2 w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs sm:text-sm transition-colors shadow-lg shadow-amber-500/20">
          <i data-lucide="check-circle-2" class="w-4 h-4"></i>
          <span>I Accept Community Guidelines</span>
        </button>
      </div>
    `;

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    this.refreshIcons();

    const acceptBtn = document.getElementById('jb-accept-guidelines-btn');
    if (acceptBtn) {
      acceptBtn.addEventListener('click', async () => {
        acceptBtn.disabled = true;
        acceptBtn.textContent = 'Accepting...';
        try {
          if (window.JustBaddoApi?.auth?.acceptGuidelines) {
            await window.JustBaddoApi.auth.acceptGuidelines();
          }
          if (window.JustBaddoState?.state?.currentUser) {
            window.JustBaddoState.state.currentUser.accepted_community_guidelines = true;
          }
          modal.classList.add('hidden');
          document.body.style.overflow = '';
          JustBaddoUI.toast('Community guidelines accepted! First Steps badge unlocked.', 'success');
          if (typeof onAccept === 'function') onAccept();
        } catch (err) {
          JustBaddoUI.toast('Failed to record acceptance. Please try again.', 'error');
          acceptBtn.disabled = false;
          acceptBtn.textContent = 'I Accept Community Guidelines';
        }
      });
    }
  },

  refreshIcons() {
    if (typeof lucide !== 'undefined' && lucide.createIcons) {
      lucide.createIcons();
    }
  },

  setupToastsContainer() {
    if (!document.getElementById('jb-toast-container')) {
      const container = document.createElement('div');
      container.id = 'jb-toast-container';
      container.className = 'fixed bottom-24 right-6 z-50 flex flex-col gap-3 pointer-events-none';
      document.body.appendChild(container);
    }
  },

  toast(message, type = 'info', duration = 3500) {
    this.setupToastsContainer();
    const container = document.getElementById('jb-toast-container');
    const toast = document.createElement('div');

    const typeStyles = {
      info: 'bg-zinc-900/95 border-zinc-800 text-zinc-100',
      success: 'bg-zinc-900/95 border-emerald-500/50 text-emerald-300',
      warning: 'bg-zinc-900/95 border-amber-500/50 text-amber-300',
      error: 'bg-zinc-900/95 border-rose-500/50 text-rose-300'
    };

    const iconNames = {
      info: 'info',
      success: 'check-circle',
      warning: 'alert-triangle',
      error: 'alert-circle'
    };

    toast.className = `pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl border shadow-2xl backdrop-blur-md transition-all duration-300 transform translate-y-4 opacity-0 text-sm font-medium ${typeStyles[type] || typeStyles.info}`;
    toast.innerHTML = `
      <i data-lucide="${iconNames[type] || 'info'}" class="w-4 h-4 shrink-0"></i>
      <span>${message}</span>
    `;

    container.appendChild(toast);
    this.refreshIcons();

    // Trigger enter animation
    requestAnimationFrame(() => {
      toast.classList.remove('translate-y-4', 'opacity-0');
    });

    setTimeout(() => {
      toast.classList.add('opacity-0', 'translate-y-2');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },

  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    this.refreshIcons();
  },

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  },

  setupModalDismissListeners() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.jb-modal:not(.hidden)');
        openModals.forEach(m => m.classList.add('hidden'));
        document.body.style.overflow = '';
      }
    });

    document.addEventListener('click', (e) => {
      if (e.target.matches('.jb-modal-backdrop') || e.target.closest('[data-modal-close]')) {
        const modal = e.target.closest('.jb-modal');
        if (modal) {
          modal.classList.add('hidden');
          document.body.style.overflow = '';
        }
      }
    });
  },

  setupDropdownListeners() {
    // Click listener for toggling and dismissing dropdowns
    document.addEventListener('click', (e) => {
      const toggle = e.target.closest('[data-dropdown-toggle]');
      if (toggle) {
        e.stopPropagation();
        const targetId = toggle.getAttribute('data-dropdown-toggle');
        const menu = document.getElementById(targetId);
        if (menu) {
          const isHidden = menu.classList.contains('hidden');
          // Close all dropdowns
          document.querySelectorAll('.jb-dropdown-menu').forEach(m => {
            m.classList.add('hidden');
            const otherToggle = document.querySelector(`[data-dropdown-toggle="${m.id}"]`);
            if (otherToggle) otherToggle.setAttribute('aria-expanded', 'false');
          });

          if (isHidden) {
            menu.classList.remove('hidden');
            toggle.setAttribute('aria-expanded', 'true');
          } else {
            toggle.setAttribute('aria-expanded', 'false');
          }
        }
        return;
      }

      // Click outside dropdown closes all
      if (!e.target.closest('.jb-dropdown-menu')) {
        document.querySelectorAll('.jb-dropdown-menu').forEach(m => {
          m.classList.add('hidden');
          const t = document.querySelector(`[data-dropdown-toggle="${m.id}"]`);
          if (t) t.setAttribute('aria-expanded', 'false');
        });
      }
    });

    // Escape key closes open dropdowns
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const openMenus = document.querySelectorAll('.jb-dropdown-menu:not(.hidden)');
        openMenus.forEach(m => {
          m.classList.add('hidden');
          const t = document.querySelector(`[data-dropdown-toggle="${m.id}"]`);
          if (t) {
            t.setAttribute('aria-expanded', 'false');
            t.focus();
          }
        });
      }
    });
  },

  setupTabs(containerSelector = '.jb-tabs-container') {
    document.querySelectorAll(containerSelector).forEach(container => {
      const tabButtons = container.querySelectorAll('[data-tab-target]');
      tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          const targetSelector = btn.getAttribute('data-tab-target');
          tabButtons.forEach(b => {
            b.classList.remove('active', 'border-amber-500', 'text-amber-400');
            b.classList.add('border-transparent', 'text-zinc-400');
          });
          btn.classList.add('active', 'border-amber-500', 'text-amber-400');
          btn.classList.remove('border-transparent', 'text-zinc-400');

          container.querySelectorAll('.jb-tab-pane').forEach(pane => pane.classList.add('hidden'));
          const targetPane = container.querySelector(targetSelector);
          if (targetPane) {
            targetPane.classList.remove('hidden');
            this.refreshIcons();
          }
        });
      });
    });
  }
};
