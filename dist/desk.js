const previews = {
  'ai-review': ['AI 走查助手', '网页工具与 Figma 插件界面'],
  'ip-worldbook': ['IP 世界书', 'IP 世界书产品界面'],
  'dual-screen': ['直播双屏项目', '双屏直播引导 · 概念示意'],
  'ai-editor': ['AI 游戏编辑器', '人机协作与叙事节点 · 概念示意']
};
const work = document.querySelector('.work-split');
const workSection = work.closest('.studio-work');
const you = work.querySelector('.cursor-you');
const preview = work.querySelector('.work-preview');
const list = work.querySelector('.work-list');
const rows = [...list.querySelectorAll('.work-row')];
const artwork = [...preview.querySelectorAll('[data-art]')];
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');

function reveal(row) {
  const project = row.dataset.project;
  if (work.classList.contains('has-preview') && preview.dataset.mode === project) return;
  const [title, caption] = previews[project];
  for (const art of artwork) art.hidden = art.dataset.art !== project;
  for (const link of rows) link.classList.toggle('is-previewed', link === row);
  preview.querySelector('[data-preview-title]').textContent = title;
  preview.querySelector('[data-preview-caption]').textContent = caption;
  preview.dataset.mode = project;
  work.classList.add('has-preview');
  preview.setAttribute('aria-hidden', 'false');
}

function dismiss() {
  work.classList.remove('has-preview');
  for (const row of rows) row.classList.remove('is-previewed');
  preview.setAttribute('aria-hidden', 'true');
  preview.style.removeProperty('--float-x');
  preview.style.removeProperty('--float-y');
}

for (const row of rows) {
  row.addEventListener('pointerenter', (event) => {
    if (event.pointerType === 'mouse') reveal(row);
  });
  row.addEventListener('focus', (event) => {
    if (row.matches(':focus-visible') && (event.relatedTarget || location.hash !== '#' + row.id)) reveal(row);
  });
}
work.addEventListener('pointerleave', (event) => {
  if (event.pointerType === 'mouse' && !list.querySelector(':focus-visible')) dismiss();
});
work.addEventListener('focusout', (event) => {
  if (!work.contains(event.relatedTarget) && !work.matches(':hover')) dismiss();
});
work.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') dismiss();
});
work.addEventListener('pointermove', (event) => {
  if (event.pointerType !== 'mouse' || reduceMotion.matches || !work.classList.contains('has-preview')) return;
  const bounds = preview.getBoundingClientRect();
  const x = Math.max(0.06, Math.min(.92, (event.clientX - bounds.left) / bounds.width));
  const y = Math.max(.09, Math.min(.89, (event.clientY - bounds.top) / bounds.height));
  preview.style.setProperty('--float-x', `${(x - .5) * 24}px`);
  preview.style.setProperty('--float-y', `${(y - .5) * 18}px`);
});


function trackVisitor(event) {
  if (event.pointerType !== 'mouse') return;
  const bounds = workSection.getBoundingClientRect();
  const x = Math.max(0, Math.min(bounds.width - you.offsetWidth - 5, event.clientX - bounds.left));
  const y = Math.max(0, Math.min(bounds.height - you.offsetHeight - 5, event.clientY - bounds.top));
  you.style.setProperty('--you-x', `${x}px`);
  you.style.setProperty('--you-y', `${y}px`);
  workSection.classList.add('has-visitor');
}

function hideVisitor() {
  workSection.classList.remove('has-visitor');
}

workSection.addEventListener('pointerenter', trackVisitor);
workSection.addEventListener('pointermove', trackVisitor);
workSection.addEventListener('pointerleave', hideVisitor);
workSection.addEventListener('pointercancel', hideVisitor);
window.addEventListener('blur', hideVisitor);
