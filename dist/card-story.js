(() => {
  const story = document.querySelector('.card-story');
  if (!story) return;

  const reveals = new Map();
  story.querySelectorAll('[data-card-reveal]').forEach(canvas => {
    const question = canvas.querySelector('.card-thesis-front, .card-reveal-question, .card-style-front');
    const answer = canvas.querySelector('.card-thesis-back, .card-reveal-answer, .card-style-answer');
    let hintTimer = null;

    function clearHint() {
      clearTimeout(hintTimer);
      hintTimer = null;
      canvas.classList.remove('is-hint-ready');
    }

    function showAnswer(show) {
      clearHint();
      canvas.classList.toggle('is-showing-answer', show);
      canvas.setAttribute('aria-pressed', String(show));
      question.setAttribute('aria-hidden', String(show));
      answer.setAttribute('aria-hidden', String(!show));
    }

    function scheduleHint() {
      if (
        hintTimer !== null ||
        canvas.classList.contains('is-showing-answer') ||
        canvas.classList.contains('is-hint-ready')
      ) return;
      hintTimer = setTimeout(() => {
        hintTimer = null;
        canvas.classList.add('is-hint-ready');
      }, 2000);
    }

    canvas.addEventListener('pointerenter', event => {
      if (event.pointerType === 'mouse') showAnswer(true);
    });
    canvas.addEventListener('click', () => showAnswer(true));
    reveals.set(canvas, {showAnswer, scheduleHint});
  });

  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window)) {
    reveals.forEach(reveal => reveal.scheduleHint());
    return;
  }

  if (!reduceMotion) story.classList.add('has-case-motion');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const outside = !entry.isIntersecting || entry.intersectionRatio === 0;
      const reveal = reveals.get(entry.target);
      if (reveal) {
        if (outside) reveal.showAnswer(false);
        else reveal.scheduleHint();
      } else if (outside) {
        entry.target.classList.remove('is-entered');
      } else if (entry.intersectionRatio >= .995) {
        entry.target.classList.add('is-entered');
      }
    });
  }, {threshold: [0, .01, .995, 1]});

  reveals.forEach((reveal, canvas) => observer.observe(canvas));
  story.querySelectorAll('[data-case-enter]').forEach(figure => observer.observe(figure));
})();
