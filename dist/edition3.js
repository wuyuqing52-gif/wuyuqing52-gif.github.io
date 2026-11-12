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
    flower.addEventListener('pointerenter', event => {
      if (finePointer.matches && event.pointerType === 'mouse') turnFlower(flower, 280);
    });
    flower.addEventListener('focus', () => turnFlower(flower, 280));
    if (flower.tagName === 'BUTTON') {
      flower.addEventListener('click', () => {
        turnFlower(flower, 180);
        const status = document.querySelector('.flower-status');
        if (status) status.textContent = '手绘花朵转起来了。';
      });
    }
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
    const title = artworkDialog.querySelector('#art-lightbox-title');
    const viewport = artworkDialog.querySelector('.art-lightbox-scroll');
    document.addEventListener('click', event => {
      const link = event.target.closest('[data-image-preview]');
      if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      image.src = link.href;
      image.alt = link.dataset.imageTitle;
      title.textContent = link.dataset.imageTitle;
      artworkDialog.showModal();
      viewport.scrollTop = 0;
      viewport.scrollLeft = 0;
      document.body.classList.add('has-open-artwork');
    });
    artworkDialog.querySelector('[data-close-artwork]').addEventListener('click', () => artworkDialog.close());
    artworkDialog.addEventListener('click', event => {
      if (event.target === artworkDialog) artworkDialog.close();
    });
    artworkDialog.addEventListener('close', () => {
      document.body.classList.remove('has-open-artwork');
      image.removeAttribute('src');
    });
  }
})();
