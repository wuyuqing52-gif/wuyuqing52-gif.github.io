(() => {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const flowers = [...document.querySelectorAll('[data-flower]')];
  const rotations = new WeakMap();

  function turnFlower(flower, amount) {
    if (reducedMotion.matches) return;
    const angle = rotations.get(flower) + amount;
    rotations.set(flower, angle);
    flower.querySelector('.flower-art').style.transform = `rotate(${angle}deg)`;
  }

  flowers.forEach(flower => {
    rotations.set(flower, Number(flower.dataset.start || 0));
    const frames = [...flower.querySelectorAll('.flower-frame')];
    if (!frames.length) {
      flower.addEventListener('pointerenter', event => {
        if (finePointer.matches && event.pointerType === 'mouse') turnFlower(flower, 280);
      });
      flower.addEventListener('focus', () => turnFlower(flower, 280));
      return;
    }

    const artwork = flower.querySelector('.flower-art');
    let cycle;
    let frame = 0;

    function showFrame(index) {
      frame = index;
      flower.dataset.frame = frames[index].classList[1].replace('flower-frame-', '');
    }

    function stopCycle() {
      clearInterval(cycle);
      cycle = undefined;
      showFrame(0);
    }

    function startCycle(amount) {
      if (reducedMotion.matches || cycle !== undefined) return;
      turnFlower(flower, amount);
      showFrame(1);
      cycle = setInterval(() => showFrame((frame + 1) % frames.length), 320);
    }

    function handleRotationEnd(event) {
      if (event.target === artwork && event.propertyName === 'transform') stopCycle();
    }

    artwork.addEventListener('transitionend', handleRotationEnd);
    artwork.addEventListener('transitioncancel', handleRotationEnd);
    reducedMotion.addEventListener('change', stopCycle);
    flower.addEventListener('pointerenter', event => {
      if (finePointer.matches && event.pointerType === 'mouse') startCycle(280);
    });
    flower.addEventListener('focus', () => {
      if (flower.matches(':focus-visible')) startCycle(280);
    });
    flower.addEventListener('click', () => startCycle(180));
  });

  const copyButton = document.querySelector('[data-copy-email]');
  copyButton?.addEventListener('click', async () => {
    const status = document.querySelector('[data-copy-status]');
    try {
      await navigator.clipboard.writeText('435456341@qq.com');
      status.textContent = '邮箱已复制';
      copyButton.textContent = '已复制';
    } catch {
      status.textContent = '请长按或选中邮箱复制';
      copyButton.textContent = '复制邮箱';
    }
  });

  const artworkDialog = document.querySelector('#art-lightbox');
  if (artworkDialog) {
    const image = artworkDialog.querySelector('img');
    const viewport = artworkDialog.querySelector('.art-lightbox-scroll');
    image.addEventListener('load', () => {
      image.classList.toggle('is-long', image.naturalHeight > image.naturalWidth * 3.3);
    });
    document.addEventListener('click', event => {
      const link = event.target.closest('[data-image-preview]');
      if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      image.classList.remove('is-long');
      image.src = link.href;
      image.alt = link.dataset.imageTitle;
      artworkDialog.showModal();
      viewport.scrollTop = 0;
      viewport.scrollLeft = 0;
      document.body.classList.add('has-open-artwork');
    });
    artworkDialog.querySelector('[data-close-artwork]').addEventListener('click', () => artworkDialog.close());
    artworkDialog.addEventListener('click', event => {
      if (event.target === artworkDialog || event.target === viewport) artworkDialog.close();
    });
    artworkDialog.addEventListener('close', () => {
      document.body.classList.remove('has-open-artwork');
      image.removeAttribute('src');
    });
  }
})();
