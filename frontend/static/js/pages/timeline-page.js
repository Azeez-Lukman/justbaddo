/**
 * JUSTBADDO — Career Timeline Page Logic
 * Renders verified chronological milestones and category filters.
 */

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('jb-timeline-container');
  let activeCategory = 'ALL';

  function renderTimeline() {
    if (!container) return;
    let events = JUSTBADDO_TIMELINE;

    if (activeCategory === 'RELEASES') {
      events = events.filter(e => e.category.toLowerCase().includes('album') || e.category.toLowerCase().includes('breakthrough') || e.category.toLowerCase().includes('single'));
    } else if (activeCategory === 'INDUSTRY') {
      events = events.filter(e => e.category.toLowerCase().includes('label') || e.category.toLowerCase().includes('partnership') || e.category.toLowerCase().includes('concert'));
    }

    container.innerHTML = events.map((item, idx) => `
      <div class="relative pl-8 sm:pl-32 py-6 group">
        <!-- Year Tag on left for desktop -->
        <div class="sm:absolute sm:left-0 sm:top-6 sm:w-24 text-left sm:text-right mb-2 sm:mb-0">
          <span class="font-display font-black text-2xl sm:text-3xl text-amber-500">${item.year}</span>
        </div>

        <!-- Node Dot -->
        <div class="absolute left-0 sm:left-24 top-8 -translate-x-1/2 w-4 h-4 rounded-full bg-zinc-950 border-2 border-amber-500 group-hover:scale-125 transition-transform z-10 shadow-md shadow-amber-500/20"></div>

        <!-- Content Card -->
        <div class="p-6 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition-all">
          <div class="flex items-center gap-2 mb-2">
            <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">${item.category}</span>
          </div>
          <h3 class="text-lg font-bold text-zinc-100 mb-2">${item.title}</h3>
          <p class="text-xs sm:text-sm text-zinc-300 leading-relaxed mb-4">${item.description}</p>
          <div class="flex items-center gap-2 text-[11px] text-zinc-500 pt-3 border-t border-zinc-800/60">
            <span class="font-semibold text-zinc-400">Verified Source:</span>
            <span>${item.source}</span>
          </div>
        </div>
      </div>
    `).join('');

    JustBaddoUI.refreshIcons();
  }

  // Category buttons
  document.querySelectorAll('[data-timeline-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-timeline-filter]').forEach(b => {
        b.classList.remove('bg-amber-500', 'text-black', 'font-semibold');
        b.classList.add('bg-zinc-900', 'text-zinc-400', 'hover:text-white');
      });
      btn.classList.remove('bg-zinc-900', 'text-zinc-400', 'hover:text-white');
      btn.classList.add('bg-amber-500', 'text-black', 'font-semibold');
      activeCategory = btn.getAttribute('data-timeline-filter');
      renderTimeline();
    });
  });

  renderTimeline();
});
