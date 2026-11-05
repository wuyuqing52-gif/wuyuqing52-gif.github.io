(()=>{
const viewer = document.querySelector("#cardViewer");
const gallery = document.querySelector("#cardGallery");
const cardTemplate = document.querySelector("#cardTemplate");
const levelTabs = document.querySelectorAll(".level-tab");
const closeButton = document.querySelector(".viewer-close");
const motionArea = document.querySelector("#motionArea");
const interactiveCard = document.querySelector("#interactiveCard");
const viewerUnderlay = document.querySelector("#viewerUnderlay");
const viewerBackground = document.querySelector("#viewerBackground");
const viewerCharacter = document.querySelector("#viewerCharacter");
const viewerEffect = document.querySelector("#viewerEffect");
const viewerUi = document.querySelector("#viewerUi");

let animationFrame = 0;
let pointerX = 0;
let pointerY = 0;
let activeTrigger = null;
let restoreVisibleFocus = false;

const cardFace = {
  left: 247 / 1200,
  top: 244 / 1600,
  width: 706 / 1200,
  height: 1112 / 1600
};

const levelNames = {
  base: "基础",
  lv2: "Lv2",
  lv3: "Lv3"
};

const placeholderAssets = {
  background: "/demos/card-effects/assets/preview-card-background.webp",
  character: "/demos/card-effects/assets/preview-card-character.webp",
  ui: "/demos/card-effects/assets/preview-card-ui.webp",
  shineMask: "/demos/card-effects/assets/preview-card-background.webp"
};

const baseCardAssets = {
  "0:1": {
    type: "base-plan1-normal",
    label: "基础方案一普通卡牌",
    composite: "/demos/card-effects/assets/base-plan1-normal.webp",
    shineMask: "/demos/card-effects/assets/base-plan1-normal.webp"
  },
  "0:2": {
    type: "base-plan1-rare",
    label: "基础方案一稀有卡牌",
    composite: "/demos/card-effects/assets/base-plan1-rare.webp",
    shineMask: "/demos/card-effects/assets/base-plan1-rare.webp"
  },
  "1:1": {
    type: "base-plan2-normal",
    label: "基础方案二普通卡牌",
    composite: "/demos/card-effects/assets/base-plan2-normal.webp",
    shineMask: "/demos/card-effects/assets/base-plan2-normal.webp"
  },
  "1:2": {
    type: "base-plan2-rare",
    label: "基础方案二稀有卡牌",
    composite: "/demos/card-effects/assets/base-plan2-rare.webp",
    shineMask: "/demos/card-effects/assets/base-plan2-rare.webp"
  },
  "1:3": {
    type: "base-plan2-super",
    label: "基础方案二超稀有卡牌",
    background: "/demos/card-effects/assets/base-plan2-super-background.webp",
    character: "/demos/card-effects/assets/base-plan2-super-character.webp",
    ui: "/demos/card-effects/assets/base-plan2-super-ui.webp",
    shineMask: "/demos/card-effects/assets/base-plan2-super-background.webp"
  },
  "1:4": {
    type: "base-plan2-legend",
    label: "基础方案二典藏动态卡牌",
    background: "/demos/card-effects/assets/base-plan2-legend-background.webp",
    character: "/demos/card-effects/assets/lv3-gold-character.webp",
    ui: "/demos/card-effects/assets/base-plan2-legend-ui.webp",
    shineMask: "/demos/card-effects/assets/base-plan2-legend-background.webp",
    animatedCharacter: true
  },
  "0:4": {
    type: "base-plan1-legend",
    label: "基础方案一典藏动态卡牌",
    background: "/demos/card-effects/assets/lv3-gold-static-background.webp",
    character: "/demos/card-effects/assets/lv3-gold-character.webp",
    ui: "/demos/card-effects/assets/lv3-gold-ui.webp",
    shineMask: "/demos/card-effects/assets/lv3-gold-static-background.webp",
    animatedCharacter: true
  }
};

const lv3SuperAssets = {
  background: "/demos/card-effects/assets/lv3-super-background.webp",
  character: "/demos/card-effects/assets/preview-card-character.webp",
  effect: "/demos/card-effects/assets/lv3-legend-effect.webp",
  ui: "/demos/card-effects/assets/preview-card-ui.webp",
  shineMask: "/demos/card-effects/assets/preview-card-background.webp",
  animatedBackground: true
};

const lv3NormalAssets = {
  composite: "/demos/card-effects/assets/lv3-plan1-normal.webp",
  shineMask: "/demos/card-effects/assets/base-plan1-normal.webp"
};

const lv3RareAssets = {
  composite: "/demos/card-effects/assets/lv3-plan1-rare.webp",
  shineMask: "/demos/card-effects/assets/base-plan1-rare.webp"
};

const lv2NormalAssets = {
  composite: "/demos/card-effects/assets/lv2-plan1-normal.webp",
  shineMask: "/demos/card-effects/assets/base-plan1-normal.webp"
};

const lv2RareAssets = {
  composite: "/demos/card-effects/assets/lv2-plan1-rare.webp",
  shineMask: "/demos/card-effects/assets/base-plan1-rare.webp"
};

const lv2SuperAssets = {
  underlay: "/demos/card-effects/assets/lv2-plan1-super-underlay.webp",
  background: "/demos/card-effects/assets/zhouwang-bg.webp",
  character: "/demos/card-effects/assets/preview-card-character.webp",
  effect: "/demos/card-effects/assets/lv2-plan1-super-effect.webp",
  ui: "/demos/card-effects/assets/preview-card-ui.webp",
  shineMask: "/demos/card-effects/assets/zhouwang-bg.webp",
  animatedUnderlay: true
};

const lv2LegendAssets = {
  background: "/demos/card-effects/assets/lv2-gold-background.webp",
  character: "/demos/card-effects/assets/lv3-gold-character.webp",
  effect: "/demos/card-effects/assets/lv2-gold-effect.webp",
  ui: "/demos/card-effects/assets/lv2-gold-ui.webp",
  shineMask: "/demos/card-effects/assets/lv3-gold-static-background.webp",
  animatedBackground: true,
  animatedCharacter: true
};

const lv2Plan2NormalAssets = {
  underlay: lv2RareAssets.composite,
  background: baseCardAssets["1:1"].composite,
  effect: lv2SuperAssets.effect,
  shineMask: baseCardAssets["1:1"].shineMask,
  animatedUnderlay: true
};

const lv2Plan2RareAssets = {
  underlay: lv2SuperAssets.underlay,
  background: baseCardAssets["1:2"].composite,
  effect: lv2SuperAssets.effect,
  shineMask: baseCardAssets["1:2"].shineMask,
  animatedUnderlay: true
};

const lv2Plan2SuperAssets = {
  underlay: lv2SuperAssets.underlay,
  background: baseCardAssets["1:3"].background,
  character: baseCardAssets["1:3"].character,
  effect: lv2SuperAssets.effect,
  ui: baseCardAssets["1:3"].ui,
  shineMask: baseCardAssets["1:3"].shineMask,
  animatedUnderlay: true
};

const lv2Plan2LegendAssets = {
  underlay: lv2LegendAssets.background,
  background: baseCardAssets["1:4"].background,
  character: baseCardAssets["1:4"].character,
  effect: lv2SuperAssets.effect,
  ui: baseCardAssets["1:4"].ui,
  shineMask: baseCardAssets["1:4"].shineMask,
  animatedUnderlay: true,
  animatedCharacter: true
};

const lv3Plan2NormalAssets = {
  underlay: "/demos/card-effects/assets/lv3-plan1-rare.webp",
  background: "/demos/card-effects/assets/base-plan2-normal.webp",
  effect: "/demos/card-effects/assets/lv3-legend-effect.webp",
  shineMask: "/demos/card-effects/assets/base-plan2-normal.webp",
  animatedUnderlay: true
};

const lv3Plan2RareAssets = {
  underlay: "/demos/card-effects/assets/lv3-super-background.webp",
  background: "/demos/card-effects/assets/base-plan2-rare.webp",
  effect: "/demos/card-effects/assets/lv3-legend-effect.webp",
  shineMask: "/demos/card-effects/assets/base-plan2-rare.webp",
  animatedUnderlay: true
};

const lv3Plan2SuperAssets = {
  underlaySequence: {
    directory: "/demos/card-effects/assets/lv3-plan2-super-underlay-frames",
    prefix: "frame-",
    start: 0,
    count: 74,
    pad: 5,
    extension: "webp",
    frameMs: 50
  },
  character: "/demos/card-effects/assets/base-plan2-super-character.webp",
  effect: "/demos/card-effects/assets/lv3-gold-effect.webp",
  ui: "/demos/card-effects/assets/base-plan2-super-ui.webp",
  shineMask: "/demos/card-effects/assets/base-plan2-super-background.webp",
  animatedUnderlay: true
};

const lv3LegendAssets = {
  underlay: "/demos/card-effects/assets/lv3-gold-underlay.webp",
  background: "/demos/card-effects/assets/lv3-gold-static-background.webp",
  character: "/demos/card-effects/assets/lv3-gold-character.webp",
  effect: "/demos/card-effects/assets/lv3-gold-effect.webp",
  ui: "/demos/card-effects/assets/lv3-gold-ui.webp",
  shineMask: "/demos/card-effects/assets/lv3-gold-static-background.webp",
  animatedUnderlay: true,
  animatedCharacter: true
};

const lv3Plan2LegendAssets = {
  underlay: lv3LegendAssets.underlay,
  background: baseCardAssets["1:4"].background,
  character: lv3LegendAssets.character,
  effect: lv3LegendAssets.effect,
  ui: baseCardAssets["1:4"].ui,
  shineMask: baseCardAssets["1:4"].shineMask,
  animatedUnderlay: true,
  animatedCharacter: true
};

function getSequenceFrameSrc(sequence, frameOffset = 0) {
  const frame = sequence.start + (frameOffset % sequence.count);
  const name = `${sequence.prefix}${String(frame).padStart(sequence.pad, "0")}.${sequence.extension}`;
  return `${sequence.directory}/${name}`;
}

function setFrameSequence(layer, sequence) {
  if (!sequence) {
    delete layer.dataset.sequenceDirectory;
    delete layer.dataset.sequencePrefix;
    delete layer.dataset.sequenceStart;
    delete layer.dataset.sequenceCount;
    delete layer.dataset.sequencePad;
    delete layer.dataset.sequenceExtension;
    delete layer.dataset.sequenceFrameMs;
    return;
  }

  layer.dataset.sequenceDirectory = sequence.directory;
  layer.dataset.sequencePrefix = sequence.prefix;
  layer.dataset.sequenceStart = String(sequence.start);
  layer.dataset.sequenceCount = String(sequence.count);
  layer.dataset.sequencePad = String(sequence.pad);
  layer.dataset.sequenceExtension = sequence.extension;
  layer.dataset.sequenceFrameMs = String(sequence.frameMs);
  layer.src = getSequenceFrameSrc(sequence);
}

function animateFrameSequences(timestamp) {
  if (document.hidden || (!viewer.open && (gallery.getBoundingClientRect().bottom < 0 || gallery.getBoundingClientRect().top > innerHeight))) { requestAnimationFrame(animateFrameSequences); return; }
  document.querySelectorAll("[data-sequence-directory]").forEach((layer) => {
    const sequence = {
      directory: layer.dataset.sequenceDirectory,
      prefix: layer.dataset.sequencePrefix,
      start: Number(layer.dataset.sequenceStart),
      count: Number(layer.dataset.sequenceCount),
      pad: Number(layer.dataset.sequencePad),
      extension: layer.dataset.sequenceExtension,
      frameMs: Number(layer.dataset.sequenceFrameMs)
    };
    const frameOffset = Math.floor(timestamp / sequence.frameMs);
    const nextSrc = getSequenceFrameSrc(sequence, frameOffset);
    if (layer.getAttribute("src") !== nextSrc) {
      layer.src = nextSrc;
    }
  });
  requestAnimationFrame(animateFrameSequences);
}

function renderCards(level) {
  const fragment = document.createDocumentFragment();
  const rarityGuide = document.createElement("div");
  const rarityLabels = document.createElement("div");

  rarityGuide.className = "rarity-guide";
  rarityLabels.className = "rarity-labels";
  rarityGuide.append(document.createElement("span"), rarityLabels);
  ["普通", "稀有", "超稀有", "典藏"].forEach((rarity) => {
    const label = document.createElement("span");
    label.className = "rarity-label";
    label.textContent = rarity;
    rarityLabels.appendChild(label);
  });
  fragment.appendChild(rarityGuide);

  ["方案一", "方案二"].forEach((solutionName, solutionIndex) => {
    const section = document.createElement("section");
    const title = document.createElement("h2");
    const cards = document.createElement("div");

    section.className = "solution-row";
    title.className = "solution-label";
    title.textContent = solutionName;
    cards.className = "solution-cards";

    for (let cardIndex = 1; cardIndex <= 4; cardIndex += 1) {
      const absoluteIndex = solutionIndex * 4 + cardIndex;
      const cardFragment = cardTemplate.content.cloneNode(true);
      const trigger = cardFragment.querySelector("[data-preview-card]");
      const baseAsset = level === "base" ? baseCardAssets[`${solutionIndex}:${cardIndex}`] : null;
      const isRealLv2Normal = level === "lv2" && solutionIndex === 0 && cardIndex === 1;
      const isRealLv2Rare = level === "lv2" && solutionIndex === 0 && cardIndex === 2;
      const isRealLv2Super = level === "lv2" && solutionIndex === 0 && cardIndex === 3;
      const isRealLv2Legend = level === "lv2" && solutionIndex === 0 && cardIndex === 4;
      const isRealLv2Plan2Normal = level === "lv2" && solutionIndex === 1 && cardIndex === 1;
      const isRealLv2Plan2Rare = level === "lv2" && solutionIndex === 1 && cardIndex === 2;
      const isRealLv2Plan2Super = level === "lv2" && solutionIndex === 1 && cardIndex === 3;
      const isRealLv2Plan2Legend = level === "lv2" && solutionIndex === 1 && cardIndex === 4;
      const isRealLv3Normal = level === "lv3" && solutionIndex === 0 && cardIndex === 1;
      const isRealLv3Rare = level === "lv3" && solutionIndex === 0 && cardIndex === 2;
      const isRealLv3Super = level === "lv3" && solutionIndex === 0 && cardIndex === 3;
      const isRealLv3Legend = level === "lv3" && solutionIndex === 0 && cardIndex === 4;
      const isRealLv3Plan2Normal = level === "lv3" && solutionIndex === 1 && cardIndex === 1;
      const isRealLv3Plan2Rare = level === "lv3" && solutionIndex === 1 && cardIndex === 2;
      const isRealLv3Plan2Super = level === "lv3" && solutionIndex === 1 && cardIndex === 3;
      const isRealLv3Plan2Legend = level === "lv3" && solutionIndex === 1 && cardIndex === 4;

      trigger.setAttribute("aria-label", `${levelNames[level]}${solutionName}卡牌 ${cardIndex}，点击放大预览`);
      trigger.dataset.level = level;
      trigger.dataset.cardIndex = String(absoluteIndex);

      if (baseAsset) {
        trigger.classList.add("is-real-card");
        trigger.dataset.cardType = baseAsset.type;
        trigger.setAttribute("aria-label", `${baseAsset.label}，点击放大预览`);
        trigger.querySelector(".card-layer--background").src = baseAsset.composite || baseAsset.background;
        if (baseAsset.composite) {
          trigger.querySelector(".card-layer--character").hidden = true;
          trigger.querySelector(".card-layer--ui").hidden = true;
        } else {
          trigger.querySelector(".card-layer--character").src = baseAsset.character;
          trigger.querySelector(".card-layer--ui").src = baseAsset.ui;
          trigger.classList.toggle("has-animated-character", Boolean(baseAsset.animatedCharacter));
        }
      }

      if (isRealLv2Normal || isRealLv2Rare) {
        const assets = isRealLv2Normal ? lv2NormalAssets : lv2RareAssets;
        const rarity = isRealLv2Normal ? "普通" : "稀有";
        trigger.classList.add("is-real-card");
        trigger.dataset.cardType = isRealLv2Normal ? "lv2-normal" : "lv2-rare";
        trigger.setAttribute("aria-label", `Lv2 方案一${rarity}动态卡牌，点击放大预览`);
        trigger.querySelector(".card-layer--background").src = assets.composite;
        trigger.querySelector(".card-layer--character").hidden = true;
        trigger.querySelector(".card-layer--ui").hidden = true;
      }

      if (isRealLv2Super) {
        const underlayLayer = trigger.querySelector(".card-layer--underlay");
        const effectLayer = trigger.querySelector(".card-layer--effect");
        trigger.classList.add("is-real-card", "has-animated-underlay");
        trigger.dataset.cardType = "lv2-super";
        trigger.setAttribute("aria-label", "Lv2 方案一超稀有动态卡牌，点击放大预览");
        setFrameSequence(underlayLayer);
        underlayLayer.src = lv2SuperAssets.underlay;
        underlayLayer.hidden = false;
        trigger.querySelector(".card-layer--background").src = lv2SuperAssets.background;
        trigger.querySelector(".card-layer--character").src = lv2SuperAssets.character;
        effectLayer.src = lv2SuperAssets.effect;
        effectLayer.hidden = false;
        trigger.querySelector(".card-layer--ui").src = lv2SuperAssets.ui;
      }

      if (isRealLv2Legend) {
        const effectLayer = trigger.querySelector(".card-layer--effect");
        trigger.classList.add("is-real-card", "has-animated-background", "has-animated-character");
        trigger.dataset.cardType = "lv2-legend";
        trigger.setAttribute("aria-label", "Lv2 方案一典藏金色动态卡牌，点击放大预览");
        trigger.querySelector(".card-layer--background").src = lv2LegendAssets.background;
        trigger.querySelector(".card-layer--character").src = lv2LegendAssets.character;
        effectLayer.src = lv2LegendAssets.effect;
        effectLayer.hidden = false;
        trigger.querySelector(".card-layer--ui").src = lv2LegendAssets.ui;
      }

      if (isRealLv2Plan2Normal || isRealLv2Plan2Rare) {
        const assets = isRealLv2Plan2Normal ? lv2Plan2NormalAssets : lv2Plan2RareAssets;
        const rarity = isRealLv2Plan2Normal ? "普通" : "稀有";
        const underlayLayer = trigger.querySelector(".card-layer--underlay");
        const effectLayer = trigger.querySelector(".card-layer--effect");
        trigger.classList.add("is-real-card", "has-animated-underlay");
        trigger.dataset.cardType = isRealLv2Plan2Normal ? "lv2-plan2-normal" : "lv2-plan2-rare";
        trigger.setAttribute("aria-label", `Lv2 方案二${rarity}特效卡牌，点击放大预览`);
        setFrameSequence(underlayLayer);
        underlayLayer.src = assets.underlay;
        underlayLayer.hidden = false;
        trigger.querySelector(".card-layer--background").src = assets.background;
        trigger.querySelector(".card-layer--character").hidden = true;
        effectLayer.src = assets.effect;
        effectLayer.hidden = false;
        trigger.querySelector(".card-layer--ui").hidden = true;
      }

      if (isRealLv2Plan2Super || isRealLv2Plan2Legend) {
        const assets = isRealLv2Plan2Super ? lv2Plan2SuperAssets : lv2Plan2LegendAssets;
        const rarity = isRealLv2Plan2Super ? "超稀有" : "典藏";
        const underlayLayer = trigger.querySelector(".card-layer--underlay");
        const effectLayer = trigger.querySelector(".card-layer--effect");
        trigger.classList.add("is-real-card", "has-animated-underlay");
        trigger.classList.toggle("has-animated-character", Boolean(assets.animatedCharacter));
        trigger.dataset.cardType = isRealLv2Plan2Super ? "lv2-plan2-super" : "lv2-plan2-legend";
        trigger.setAttribute("aria-label", `Lv2 方案二${rarity}特效卡牌，点击放大预览`);
        setFrameSequence(underlayLayer);
        underlayLayer.src = assets.underlay;
        underlayLayer.hidden = false;
        trigger.querySelector(".card-layer--background").src = assets.background;
        trigger.querySelector(".card-layer--character").src = assets.character;
        effectLayer.src = assets.effect;
        effectLayer.hidden = false;
        trigger.querySelector(".card-layer--ui").src = assets.ui;
      }

      if (isRealLv3Normal || isRealLv3Rare) {
        const assets = isRealLv3Normal ? lv3NormalAssets : lv3RareAssets;
        const rarity = isRealLv3Normal ? "普通" : "稀有";
        trigger.classList.add("is-real-card");
        trigger.dataset.cardType = isRealLv3Normal ? "lv3-normal" : "lv3-rare";
        trigger.setAttribute("aria-label", `Lv3 方案一${rarity}动态卡牌，点击放大预览`);
        trigger.querySelector(".card-layer--background").src = assets.composite;
        trigger.querySelector(".card-layer--character").hidden = true;
        trigger.querySelector(".card-layer--ui").hidden = true;
      }

      if (isRealLv3Super) {
        const effectLayer = trigger.querySelector(".card-layer--effect");
        trigger.classList.add("is-real-card", "has-animated-background");
        trigger.dataset.cardType = "lv3-super";
        trigger.setAttribute("aria-label", "Lv3 方案一超稀有动态卡牌，点击放大预览");
        trigger.querySelector(".card-layer--background").src = lv3SuperAssets.background;
        trigger.querySelector(".card-layer--character").src = lv3SuperAssets.character;
        effectLayer.src = lv3SuperAssets.effect;
        effectLayer.hidden = false;
        trigger.querySelector(".card-layer--ui").src = lv3SuperAssets.ui;
      }

      if (isRealLv3Plan2Normal || isRealLv3Plan2Rare) {
        const assets = isRealLv3Plan2Normal ? lv3Plan2NormalAssets : lv3Plan2RareAssets;
        const rarity = isRealLv3Plan2Normal ? "普通" : "稀有";
        const underlayLayer = trigger.querySelector(".card-layer--underlay");
        const effectLayer = trigger.querySelector(".card-layer--effect");
        trigger.classList.add("is-real-card", "has-animated-underlay");
        trigger.dataset.cardType = isRealLv3Plan2Normal ? "lv3-plan2-normal" : "lv3-plan2-rare";
        trigger.setAttribute("aria-label", `Lv3 方案二${rarity}特效卡牌，点击放大预览`);
        setFrameSequence(underlayLayer);
        underlayLayer.src = assets.underlay;
        underlayLayer.hidden = false;
        trigger.querySelector(".card-layer--background").src = assets.background;
        trigger.querySelector(".card-layer--character").hidden = true;
        effectLayer.src = assets.effect;
        effectLayer.hidden = false;
        trigger.querySelector(".card-layer--ui").hidden = true;
      }

      if (isRealLv3Plan2Super) {
        const underlayLayer = trigger.querySelector(".card-layer--underlay");
        const effectLayer = trigger.querySelector(".card-layer--effect");
        const backgroundLayer = trigger.querySelector(".card-layer--background");
        trigger.classList.add("is-real-card", "has-animated-underlay");
        trigger.dataset.cardType = "lv3-plan2-super";
        trigger.setAttribute("aria-label", "Lv3 方案二超稀有序列动态卡牌，点击放大预览");
        setFrameSequence(underlayLayer, lv3Plan2SuperAssets.underlaySequence);
        underlayLayer.hidden = false;
        backgroundLayer.hidden = true;
        trigger.querySelector(".card-layer--character").src = lv3Plan2SuperAssets.character;
        effectLayer.src = lv3Plan2SuperAssets.effect;
        effectLayer.hidden = false;
        trigger.querySelector(".card-layer--ui").src = lv3Plan2SuperAssets.ui;
      }

      if (isRealLv3Plan2Legend) {
        const underlayLayer = trigger.querySelector(".card-layer--underlay");
        const effectLayer = trigger.querySelector(".card-layer--effect");
        trigger.classList.add("is-real-card", "has-animated-underlay", "has-animated-character");
        trigger.dataset.cardType = "lv3-plan2-legend";
        trigger.setAttribute("aria-label", "Lv3 方案二典藏动态卡牌，点击放大预览");
        setFrameSequence(underlayLayer);
        underlayLayer.src = lv3Plan2LegendAssets.underlay;
        underlayLayer.hidden = false;
        trigger.querySelector(".card-layer--background").src = lv3Plan2LegendAssets.background;
        trigger.querySelector(".card-layer--character").src = lv3Plan2LegendAssets.character;
        effectLayer.src = lv3Plan2LegendAssets.effect;
        effectLayer.hidden = false;
        trigger.querySelector(".card-layer--ui").src = lv3Plan2LegendAssets.ui;
      }

      if (isRealLv3Legend) {
        const underlayLayer = trigger.querySelector(".card-layer--underlay");
        const effectLayer = trigger.querySelector(".card-layer--effect");
        trigger.classList.add("is-real-card", "has-animated-underlay", "has-animated-character");
        trigger.dataset.cardType = "lv3-legend";
        trigger.setAttribute("aria-label", "Lv3 方案一典藏金色动态卡牌，点击放大预览");
        setFrameSequence(underlayLayer);
        underlayLayer.src = lv3LegendAssets.underlay;
        underlayLayer.hidden = false;
        trigger.querySelector(".card-layer--background").src = lv3LegendAssets.background;
        trigger.querySelector(".card-layer--character").src = lv3LegendAssets.character;
        effectLayer.src = lv3LegendAssets.effect;
        effectLayer.hidden = false;
        trigger.querySelector(".card-layer--ui").src = lv3LegendAssets.ui;
      }

      trigger.addEventListener("click", openViewer);
      cards.appendChild(cardFragment);
    }

    section.append(title, cards);
    fragment.appendChild(section);

    if (solutionIndex === 0) {
      const divider = document.createElement("div");
      divider.className = "solution-divider";
      divider.setAttribute("aria-hidden", "true");
      fragment.appendChild(divider);
    }
  });

  gallery.replaceChildren(fragment);
  gallery.dataset.level = level;
  gallery.setAttribute("aria-label", `${levelNames[level]}卡牌列表`);
}

function resetMotion() {
  motionArea.style.setProperty("--rotate-x", "0deg");
  motionArea.style.setProperty("--rotate-y", "0deg");
  motionArea.style.setProperty("--move-x", "0px");
  motionArea.style.setProperty("--move-y", "0px");
  motionArea.style.setProperty("--bg-x", "0px");
  motionArea.style.setProperty("--bg-y", "0px");
  motionArea.style.setProperty("--underlay-x", "0px");
  motionArea.style.setProperty("--underlay-y", "0px");
  motionArea.style.setProperty("--character-x", "0px");
  motionArea.style.setProperty("--character-y", "0px");
  motionArea.style.setProperty("--effect-x", "0px");
  motionArea.style.setProperty("--effect-y", "0px");
  motionArea.style.setProperty("--ui-x", "0px");
  motionArea.style.setProperty("--ui-y", "0px");
  motionArea.style.setProperty("--pointer-x", "50%");
  motionArea.style.setProperty("--pointer-y", "50%");
}

function renderMotion() {
  animationFrame = 0;
  const rect = motionArea.getBoundingClientRect();
  const x = Math.max(0, Math.min(1, (pointerX - rect.left) / rect.width));
  const y = Math.max(0, Math.min(1, (pointerY - rect.top) / rect.height));
  const shineX = Math.max(0, Math.min(1, (x - cardFace.left) / cardFace.width));
  const shineY = Math.max(0, Math.min(1, (y - cardFace.top) / cardFace.height));
  const moveX = (x - 0.5) * 42;
  const moveY = (y - 0.5) * 34;

  motionArea.style.setProperty("--rotate-x", `${((0.5 - y) * 32).toFixed(2)}deg`);
  motionArea.style.setProperty("--rotate-y", `${((x - 0.5) * 42).toFixed(2)}deg`);
  motionArea.style.setProperty("--move-x", `${moveX.toFixed(1)}px`);
  motionArea.style.setProperty("--move-y", `${moveY.toFixed(1)}px`);
  motionArea.style.setProperty("--bg-x", `${(moveX * -0.16).toFixed(1)}px`);
  motionArea.style.setProperty("--bg-y", `${(moveY * -0.12).toFixed(1)}px`);
  motionArea.style.setProperty("--underlay-x", `${(moveX * -0.06).toFixed(1)}px`);
  motionArea.style.setProperty("--underlay-y", `${(moveY * -0.045).toFixed(1)}px`);
  motionArea.style.setProperty("--character-x", `${(moveX * 0.5).toFixed(1)}px`);
  motionArea.style.setProperty("--character-y", `${(moveY * 0.4).toFixed(1)}px`);
  motionArea.style.setProperty("--effect-x", `${(moveX * 0.28).toFixed(1)}px`);
  motionArea.style.setProperty("--effect-y", `${(moveY * 0.22).toFixed(1)}px`);
  motionArea.style.setProperty("--ui-x", `${(moveX * 0.13).toFixed(1)}px`);
  motionArea.style.setProperty("--ui-y", `${(moveY * 0.1).toFixed(1)}px`);
  motionArea.style.setProperty("--pointer-x", `${(shineX * 100).toFixed(1)}%`);
  motionArea.style.setProperty("--pointer-y", `${(shineY * 100).toFixed(1)}%`);
}

function queueMotion(event) {
  pointerX = event.clientX;
  pointerY = event.clientY;
  if (!animationFrame) {
    animationFrame = requestAnimationFrame(renderMotion);
  }
}

function openViewer(event) {
  activeTrigger = event.currentTarget;
  restoreVisibleFocus = event.detail === 0;
  const cardType = activeTrigger.dataset.cardType || "placeholder";
  const assetsByType = {
    "base-plan1-normal": baseCardAssets["0:1"],
    "base-plan1-rare": baseCardAssets["0:2"],
    "base-plan2-normal": baseCardAssets["1:1"],
    "base-plan2-rare": baseCardAssets["1:2"],
    "base-plan2-super": baseCardAssets["1:3"],
    "base-plan2-legend": baseCardAssets["1:4"],
    "base-plan1-legend": baseCardAssets["0:4"],
    "lv2-normal": lv2NormalAssets,
    "lv2-rare": lv2RareAssets,
    "lv2-super": lv2SuperAssets,
    "lv2-legend": lv2LegendAssets,
    "lv2-plan2-normal": lv2Plan2NormalAssets,
    "lv2-plan2-rare": lv2Plan2RareAssets,
    "lv2-plan2-super": lv2Plan2SuperAssets,
    "lv2-plan2-legend": lv2Plan2LegendAssets,
    "lv3-normal": lv3NormalAssets,
    "lv3-rare": lv3RareAssets,
    "lv3-super": lv3SuperAssets,
    "lv3-legend": lv3LegendAssets,
    "lv3-plan2-normal": lv3Plan2NormalAssets,
    "lv3-plan2-rare": lv3Plan2RareAssets,
    "lv3-plan2-super": lv3Plan2SuperAssets,
    "lv3-plan2-legend": lv3Plan2LegendAssets,
    placeholder: placeholderAssets
  };
  const assets = assetsByType[cardType] || placeholderAssets;
  const isComposite = Boolean(assets.composite);
  const hasAnimatedBackground = Boolean(assets.animatedBackground);
  const shineMask = assets.shineMask || assets.composite || assets.background;

  interactiveCard.style.setProperty("--shine-mask", `url("${shineMask}")`);
  interactiveCard.dataset.cardType = cardType;
  viewerUnderlay.hidden = !assets.underlay && !assets.underlaySequence;
  setFrameSequence(viewerUnderlay, assets.underlaySequence);
  if (assets.underlay) {
    viewerUnderlay.src = assets.underlay;
  } else if (!assets.underlaySequence) {
    viewerUnderlay.removeAttribute("src");
  }
  viewerBackground.hidden = !assets.composite && !assets.background;
  if (assets.composite || assets.background) {
    viewerBackground.src = assets.composite || assets.background;
  } else {
    viewerBackground.removeAttribute("src");
  }
  viewerCharacter.hidden = isComposite || !assets.character;
  if (!isComposite && assets.character) {
    viewerCharacter.src = assets.character;
  } else if (!assets.character) {
    viewerCharacter.removeAttribute("src");
  }
  viewerEffect.hidden = !assets.effect;
  if (assets.effect) {
    viewerEffect.src = assets.effect;
  } else {
    viewerEffect.removeAttribute("src");
  }
  viewerUi.hidden = isComposite || !assets.ui;
  if (!isComposite && assets.ui) {
    viewerUi.src = assets.ui;
  } else if (!assets.ui) {
    viewerUi.removeAttribute("src");
  }
  interactiveCard.classList.toggle("is-real-card", cardType !== "placeholder");
  interactiveCard.classList.toggle("is-lv2-legend", cardType === "lv2-legend");
  interactiveCard.classList.toggle("has-animated-background", hasAnimatedBackground);
  interactiveCard.classList.toggle("has-animated-underlay", Boolean(assets.animatedUnderlay));
  interactiveCard.classList.toggle("has-animated-character", Boolean(assets.animatedCharacter));
  interactiveCard.setAttribute(
    "aria-label",
    {
      "base-plan1-normal": "基础方案一普通卡牌",
      "base-plan1-rare": "基础方案一稀有卡牌",
      "base-plan2-normal": "基础方案二普通卡牌",
      "base-plan2-rare": "基础方案二稀有卡牌",
      "base-plan2-super": "基础方案二超稀有卡牌",
      "base-plan2-legend": "基础方案二典藏动态卡牌",
      "base-plan1-legend": "基础方案一典藏动态卡牌",
      "lv2-normal": "Lv2 方案一普通动态卡牌",
      "lv2-rare": "Lv2 方案一稀有动态卡牌",
      "lv2-super": "Lv2 方案一超稀有动态卡牌",
      "lv2-legend": "Lv2 方案一典藏金色动态卡牌",
      "lv2-plan2-normal": "Lv2 方案二普通特效卡牌",
      "lv2-plan2-rare": "Lv2 方案二稀有特效卡牌",
      "lv2-plan2-super": "Lv2 方案二超稀有特效卡牌",
      "lv2-plan2-legend": "Lv2 方案二典藏特效卡牌",
      "lv3-normal": "Lv3 方案一普通动态卡牌",
      "lv3-rare": "Lv3 方案一稀有动态卡牌",
      "lv3-super": "Lv3 方案一超稀有动态卡牌",
      "lv3-legend": "Lv3 方案一典藏金色动态卡牌",
      "lv3-plan2-normal": "Lv3 方案二普通特效卡牌",
      "lv3-plan2-rare": "Lv3 方案二稀有特效卡牌",
      "lv3-plan2-super": "Lv3 方案二超稀有序列动态卡牌",
      "lv3-plan2-legend": "Lv3 方案二典藏动态卡牌",
      placeholder: "卡牌放大预览"
    }[cardType] || "卡牌放大预览"
  );

  resetMotion();
  viewer.showModal();
  document.body.classList.add("has-open-viewer");
  closeButton.focus({ preventScroll: true });
  document.querySelector(".viewer-guide").textContent = matchMedia("(pointer: coarse)").matches ? "拖动卡牌查看立体效果" : "移动鼠标查看立体效果";
}

function closeViewer() {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame);
    animationFrame = 0;
  }
  resetMotion();
  viewer.close();
  document.body.classList.remove("has-open-viewer");
  if (restoreVisibleFocus) {
    activeTrigger?.focus({ preventScroll: true });
  } else {
    activeTrigger?.blur();
  }
}

closeButton.addEventListener("click", closeViewer);

levelTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    levelTabs.forEach((item) => {
      const isActive = item === tab;
      item.classList.toggle("is-active", isActive);
      item.setAttribute("aria-pressed", String(isActive));
    });
    renderCards(tab.dataset.level);
  });
});

motionArea.addEventListener("pointermove", queueMotion);
motionArea.addEventListener("pointerleave", resetMotion);
motionArea.addEventListener("pointercancel", resetMotion);

viewer.addEventListener("click", (event) => {
  if (event.target === viewer || event.target === document.querySelector(".viewer-stage")) {
    closeViewer();
  }
});

viewer.addEventListener("cancel", (event) => {
  event.preventDefault();
  closeViewer();
});

viewer.addEventListener("close", () => {
  document.body.classList.remove("has-open-viewer");
});

document.querySelectorAll('[data-solution]').forEach(button => {
  if (button.tagName !== 'BUTTON') return;
  button.addEventListener('click', () => {
    gallery.dataset.solution = button.dataset.solution;
    document.querySelectorAll('.solution-tabs button').forEach(item => {
      const active = item === button;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-pressed', String(active));
    });
  });
});
renderCards("lv3");
requestAnimationFrame(animateFrameSequences);

})();
