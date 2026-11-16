(() => {
  const story = document.querySelector('.card-story');
  if (!story) return;

  const thesis = story.querySelector('.card-thesis');
  const front = thesis.querySelector('.card-thesis-front');
  const back = thesis.querySelector('.card-thesis-back');
  let pinned = false;

  function showAnswer(show) {
    thesis.classList.toggle('is-showing-answer', show);
    thesis.setAttribute('aria-pressed', String(show));
    front.setAttribute('aria-hidden', String(show));
    back.setAttribute('aria-hidden', String(!show));
  }

  thesis.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse') showAnswer(true);
  });
  thesis.addEventListener('pointerleave', () => {
    if (!pinned) showAnswer(false);
  });
  thesis.addEventListener('click', () => {
    pinned = !pinned;
    showAnswer(pinned);
  });
  thesis.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      pinned = false;
      showAnswer(false);
    }
  });

  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion || !('IntersectionObserver' in window)) return;

  story.classList.add('has-case-motion');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) {
        entry.target.classList.remove('is-entered');
      } else if (entry.intersectionRatio >= .995) {
        entry.target.classList.add('is-entered');
      }
    });
  }, {threshold: [0, .995, 1]});

  story.querySelectorAll('[data-case-enter]').forEach(figure => observer.observe(figure));
})();
