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

// The top guide previews a stage; the complete case remains visible below.
document.querySelectorAll('[data-project-guide]').forEach(guide => {
  const tabs = [...guide.querySelectorAll('[role="tab"]')];
  function selectTab(tab) {
    tabs.forEach(item => {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
      const panel = document.getElementById(item.getAttribute('aria-controls'));
      if (panel) panel.hidden = !active;
    });
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowDown' || event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); selectTab(tabs[next]); tabs[next].focus(); }
    });
  });
});
const caseChapters = document.querySelectorAll('[data-case-chapter]');
if (caseChapters.length) {
  let chapterUpdateFrame = 0;
  function updateCaseChapter() {
    chapterUpdateFrame = 0;
    let active = caseChapters[0];
    const readingLine = parseFloat(getComputedStyle(caseChapters[0]).scrollMarginTop)
      + parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) + 1;
    for (const chapter of caseChapters) {
      if (chapter.getBoundingClientRect().top <= readingLine) active = chapter;
    }
    if (scrollY + innerHeight >= document.documentElement.scrollHeight - 2) {
      active = caseChapters[caseChapters.length - 1];
    }
    document.querySelectorAll('.case-contents a').forEach(link => {
      if (link.hash === '#' + active.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  function scheduleChapterUpdate() {
    if (!chapterUpdateFrame) chapterUpdateFrame = requestAnimationFrame(updateCaseChapter);
  }
  addEventListener('scroll', scheduleChapterUpdate, {passive: true});
  addEventListener('resize', scheduleChapterUpdate);
  document.fonts.ready.then(scheduleChapterUpdate);
  updateCaseChapter();
}
// Re-drawn report illustration: reveal the correspondence between each issue
// and its marked region without uploading or analysing visitor data.
document.querySelectorAll('.rv-report').forEach(figure => {
  figure.querySelectorAll('[data-issue-filter]').forEach(button => {
    button.addEventListener('click', () => {
      const filter = button.dataset.issueFilter;
      figure.querySelectorAll('[data-issue-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      figure.querySelectorAll('[data-visual-issue]').forEach(item => { item.hidden = filter !== 'all' && item.dataset.visualIssue !== filter; });
      figure.querySelectorAll('[data-visual-mark]').forEach(item => { item.classList.toggle('rv-mark-muted', filter !== 'all' && item.dataset.visualMark !== filter); });
    });
  });
});
