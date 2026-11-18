/**
 * JUSTBADDO — Global UI Manager
 * Handles toast alerts, modal dialogs, tab switching, dropdowns, and icon hydration.
 */

window.JustBaddoUI = {
  init() {
    this.setupToastsContainer();
    this.setupDropdownListeners();
    this.setupModalDismissListeners();
    this.refreshIcons();
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
    document.addEventListener('click', (e) => {
      const toggle = e.target.closest('[data-dropdown-toggle]');
      if (toggle) {
        e.stopPropagation();
        const targetId = toggle.getAttribute('data-dropdown-toggle');
        const menu = document.getElementById(targetId);
        if (menu) {
          const isHidden = menu.classList.contains('hidden');
          document.querySelectorAll('.jb-dropdown-menu').forEach(m => m.classList.add('hidden'));
          if (isHidden) menu.classList.remove('hidden');
        }
        return;
      }

      // Click outside dropdown closes all
      if (!e.target.closest('.jb-dropdown-menu')) {
        document.querySelectorAll('.jb-dropdown-menu').forEach(m => m.classList.add('hidden'));
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
