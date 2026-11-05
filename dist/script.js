'use strict';
const filterButtons = document.querySelectorAll('[data-filter]');
const projectCards = document.querySelectorAll('.project[data-category]');
function readFilter() { try { return sessionStorage.getItem('yuki-work-filter') || 'all'; } catch { return 'all'; } }
function applyFilter(filter) {
  if (!['all', 'ai', 'live'].includes(filter)) filter = 'all';
  filterButtons.forEach(button => {
    const selected = button.dataset.filter === filter;
    button.classList.toggle('active', selected);
    button.setAttribute('aria-pressed', String(selected));
  });
  projectCards.forEach(card => { card.hidden = filter !== 'all' && card.dataset.category !== filter; });
  try { sessionStorage.setItem('yuki-work-filter', filter); } catch {}
}
filterButtons.forEach(button => button.addEventListener('click', () => applyFilter(button.dataset.filter)));
function restoreWorkAnchor() {
  if (!projectCards.length) return;
  const target = document.getElementById(location.hash.slice(1));
  let filter = readFilter();
  if (target?.matches('.project') && filter !== 'all' && target.dataset.category !== filter) filter = 'all';
  applyFilter(filter);
  if (target?.id.startsWith('project-')) requestAnimationFrame(() => target.scrollIntoView({behavior:'instant',block:'start'}));
}
restoreWorkAnchor();
window.addEventListener('pageshow', restoreWorkAnchor);
window.addEventListener('hashchange', restoreWorkAnchor);
document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    const status = button.parentElement.querySelector('.copy-result');
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      if (status) status.textContent = '邮箱已复制';
    } catch {
      if (status) status.textContent = '可选中上方邮箱复制';
    }
  });
});
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));

// Fragment navigation can focus links without a keyboard action. Keep that
// state visually neutral while preserving a visible ring for Tab navigation.
let keyboardNavigation = false;
function updateProjectFocus() {
  document.querySelectorAll('.project').forEach(card => {
    card.classList.toggle('keyboard-focus', keyboardNavigation && card === document.activeElement);
  });
}
document.addEventListener('keydown', event => {
  if (event.key === 'Tab' || event.key.startsWith('Arrow')) { keyboardNavigation = true; updateProjectFocus(); }
}, true);
document.addEventListener('pointerdown', () => { keyboardNavigation = false; updateProjectFocus(); }, true);
document.addEventListener('focusin', updateProjectFocus);
document.addEventListener('focusout', () => requestAnimationFrame(updateProjectFocus));
window.addEventListener('pageshow', updateProjectFocus);
window.addEventListener('hashchange', updateProjectFocus);
