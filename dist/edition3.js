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
})();
