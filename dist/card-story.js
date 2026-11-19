(() => {
  const story = document.querySelector('.card-story');
  if (!story) return;

  const header = document.querySelector('.site-header');

  function viewportTop() {
    return Math.max(0, header?.getBoundingClientRect().bottom || 0);
  }

  function isFullyVisible(canvas) {
    const bounds = canvas.getBoundingClientRect();
    const frame = canvas.closest('.card-story-figure').getBoundingClientRect();
    return bounds.width > 0 && bounds.height > 0 &&
      bounds.top >= Math.max(viewportTop(), frame.top) &&
      bounds.bottom <= Math.min(innerHeight, frame.bottom) &&
      bounds.left >= Math.max(0, frame.left) &&
      bounds.right <= Math.min(innerWidth, frame.right);
  }

  function centerReveal(figure) {
    figure.scrollLeft = Math.max(0, (figure.scrollWidth - figure.clientWidth) / 2);
  }

  const revealFigures = story.querySelectorAll('.card-reveal-scroll');
  revealFigures.forEach(centerReveal);
  if ('ResizeObserver' in window) {
    const resizeObserver = new ResizeObserver(entries => {
      entries.forEach(entry => centerReveal(entry.target));
    });
    revealFigures.forEach(figure => resizeObserver.observe(figure));
  }

  const reveals = new Map();
  story.querySelectorAll('[data-card-reveal]').forEach(canvas => {
    const question = canvas.querySelector('.card-thesis-front, .card-reveal-question');
    const answer = canvas.querySelector('.card-thesis-back, .card-reveal-answer');
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
        !isFullyVisible(canvas) ||
        hintTimer !== null ||
        canvas.classList.contains('is-showing-answer') ||
        canvas.classList.contains('is-hint-ready')
      ) return;
      hintTimer = setTimeout(() => {
        hintTimer = null;
        if (isFullyVisible(canvas)) canvas.classList.add('is-hint-ready');
      }, 2000);
    }

    canvas.addEventListener('pointerenter', event => {
      if (event.pointerType === 'mouse' && isFullyVisible(canvas)) showAnswer(true);
    });
    canvas.addEventListener('click', () => showAnswer(true));
    canvas.addEventListener('focus', () => centerReveal(canvas.closest('.card-story-figure')));
    reveals.set(canvas, {showAnswer, scheduleHint, clearHint});
  });

  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window)) {
    reveals.forEach(reveal => reveal.scheduleHint());
    return;
  }

  if (!reduceMotion) story.classList.add('has-case-motion');
  const motionCanvases = new Map();
  story.querySelectorAll('[data-case-enter]').forEach(figure => {
    motionCanvases.set(figure.querySelector('.card-story-canvas'), figure);
  });
  const mouseHover = matchMedia('(hover: hover) and (pointer: fine)');
  let observer;

  function observeCanvases() {
    observer?.disconnect();
    const top = viewportTop();
    motionCanvases.forEach((figure, canvas) => {
      const bounds = canvas.getBoundingClientRect();
      const frame = figure.getBoundingClientRect();
      const fits = bounds.width <= Math.min(innerWidth, frame.width) &&
        bounds.height <= innerHeight - top;
      figure.classList.toggle('is-static', !fits);
      if (!fits) figure.classList.remove('is-entered');
    });

    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        const outside = !entry.isIntersecting || entry.intersectionRatio === 0;
        const fullyVisible = entry.isIntersecting && isFullyVisible(entry.target);
        const reveal = reveals.get(entry.target);
        if (reveal) {
          if (outside) reveal.showAnswer(false);
          else if (!fullyVisible) reveal.clearHint();
          else if (mouseHover.matches && entry.target.matches(':hover')) reveal.showAnswer(true);
          else reveal.scheduleHint();
        } else {
          const figure = motionCanvases.get(entry.target);
          if (outside) figure.classList.remove('is-entered');
          else if (fullyVisible && !figure.classList.contains('is-static')) figure.classList.add('is-entered');
        }
      });
    }, {rootMargin: `-${top}px 0px 0px 0px`, threshold: [0, 1]});

    reveals.forEach((reveal, canvas) => observer.observe(canvas));
    motionCanvases.forEach((figure, canvas) => observer.observe(canvas));
  }

  observeCanvases();
  window.addEventListener('resize', observeCanvases, {passive: true});
})();
