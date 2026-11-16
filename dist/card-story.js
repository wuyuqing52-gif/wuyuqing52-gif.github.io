(() => {
  const story = document.querySelector('.card-story');
  if (!story) return;

  const thesis = story.querySelector('.card-thesis');
  const front = thesis.querySelector('.card-thesis-front');
  const back = thesis.querySelector('.card-thesis-back');
  let hintTimer = null;

  function clearHint() {
    clearTimeout(hintTimer);
    hintTimer = null;
    thesis.classList.remove('is-hint-ready');
  }

  function showAnswer(show) {
    clearHint();
    thesis.classList.toggle('is-showing-answer', show);
    thesis.setAttribute('aria-pressed', String(show));
    front.setAttribute('aria-hidden', String(show));
    back.setAttribute('aria-hidden', String(!show));
  }

  function scheduleHint() {
    if (
      hintTimer !== null ||
      thesis.classList.contains('is-showing-answer') ||
      thesis.classList.contains('is-hint-ready')
    ) return;
    hintTimer = setTimeout(() => {
      hintTimer = null;
      thesis.classList.add('is-hint-ready');
    }, 2000);
  }

  thesis.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse') showAnswer(true);
  });
  thesis.addEventListener('click', () => showAnswer(true));

  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window)) {
    scheduleHint();
    return;
  }

  if (!reduceMotion) story.classList.add('has-case-motion');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const outside = !entry.isIntersecting || entry.intersectionRatio === 0;
      if (entry.target === thesis) {
        if (outside) showAnswer(false);
        else scheduleHint();
      } else if (outside) {
        entry.target.classList.remove('is-entered');
      } else if (entry.intersectionRatio >= .995) {
        entry.target.classList.add('is-entered');
      }
    });
  }, {threshold: [0, .01, .995, 1]});

  observer.observe(thesis);
  story.querySelectorAll('[data-case-enter]').forEach(figure => observer.observe(figure));
})();
