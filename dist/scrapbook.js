// Load nearby portfolio images after the first-screen photographs.
const deferredImages = document.querySelectorAll("img[data-deferred-src]");
function loadDeferredImage(image) {
  if (image.dataset.deferredSrcset) {
    image.srcset = image.dataset.deferredSrcset;
    delete image.dataset.deferredSrcset;
  }
  image.src = image.dataset.deferredSrc;
  delete image.dataset.deferredSrc;
}

if ("IntersectionObserver" in window) {
  const imageObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        loadDeferredImage(entry.target);
        imageObserver.unobserve(entry.target);
      }
    }
  }, { rootMargin: "320px 0px" });
  deferredImages.forEach((image) => imageObserver.observe(image));
} else {
  deferredImages.forEach(loadDeferredImage);
}

const navLinks = [...document.querySelectorAll(".main-nav a")];
const sections = ["work", "about", "contact"].map((id) => document.getElementById(id));
const header = document.querySelector(".site-header");

function updateNavigation() {
  let current = "#top";
  const threshold = header.offsetHeight + window.innerHeight * 0.26;

  for (const section of sections) {
    if (section.getBoundingClientRect().top <= threshold) current = `#${section.id}`;
  }

  if (window.scrollY > 0 && window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
    current = "#contact";
  }

  for (const link of navLinks) {
    if (link.hash === current) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  }
}

window.addEventListener("scroll", updateNavigation, { passive: true });
window.addEventListener("resize", updateNavigation);
updateNavigation();

function setupSelectionFrame(frame) {
  const state = { scaleX: 1, scaleY: 1, angle: 0 };
  let gesture;
  let resetTimer;

  function renderTransform() {
    frame.style.setProperty("--frame-scale-x", state.scaleX);
    frame.style.setProperty("--frame-scale-y", state.scaleY);
    frame.style.setProperty("--frame-angle", `${state.angle}deg`);
  }

  function scheduleReset() {
    clearTimeout(resetTimer);
    resetTimer = setTimeout(() => {
      Object.assign(state, { scaleX: 1, scaleY: 1, angle: 0 });
      renderTransform();
    }, 3000);
  }

  const clampScale = (scale) => Math.min(1.2, Math.max(.8, scale));
  const clampAngle = (angle) => Math.min(25, Math.max(-25, angle));

  frame.addEventListener("pointerdown", (event) => {
    const control = event.target.closest(".frame-handle, .frame-rotate");
    if (!control || !event.isPrimary || event.button !== 0 || gesture) return;

    event.preventDefault();
    clearTimeout(resetTimer);
    // Continue from the visible position, including a reset animation in progress.
    const matrix = new DOMMatrixReadOnly(getComputedStyle(frame).transform);
    Object.assign(state, {
      scaleX: Math.hypot(matrix.a, matrix.b),
      scaleY: Math.hypot(matrix.c, matrix.d),
      angle: Math.atan2(matrix.b, matrix.a) * 180 / Math.PI,
    });
    frame.setAttribute("data-dragging", "");
    renderTransform();
    const bounds = frame.getBoundingClientRect();
    const centerX = bounds.left + bounds.width / 2;
    const centerY = bounds.top + bounds.height / 2;
    gesture = {
      pointerId: event.pointerId,
      control,
      direction: control.dataset.resize,
      startX: event.clientX,
      startY: event.clientY,
      centerX,
      centerY,
      width: frame.offsetWidth,
      height: frame.offsetHeight,
      scaleX: state.scaleX,
      scaleY: state.scaleY,
      angle: state.angle,
      pointerAngle: Math.atan2(event.clientY - centerY, event.clientX - centerX),
    };
    control.setPointerCapture(event.pointerId);
  });

  frame.addEventListener("pointermove", (event) => {
    if (gesture?.pointerId !== event.pointerId) return;

    const { direction, angle, scaleX, scaleY, width, height } = gesture;
    if (!direction) {
      const pointerAngle = Math.atan2(event.clientY - gesture.centerY, event.clientX - gesture.centerX);
      const delta = pointerAngle - gesture.pointerAngle;
      state.angle = clampAngle(angle + Math.atan2(Math.sin(delta), Math.cos(delta)) * 180 / Math.PI);
    } else {
      // Measure resizing along the frame's local axes after rotation.
      const radians = angle * Math.PI / 180;
      const deltaX = event.clientX - gesture.startX;
      const deltaY = event.clientY - gesture.startY;
      const localX = deltaX * Math.cos(radians) + deltaY * Math.sin(radians);
      const localY = deltaY * Math.cos(radians) - deltaX * Math.sin(radians);
      const horizontal = Number(direction.includes("e")) - Number(direction.includes("w"));
      const vertical = Number(direction.includes("s")) - Number(direction.includes("n"));

      if (horizontal && vertical) {
        const scaledWidth = width * scaleX;
        const scaledHeight = height * scaleY;
        const factor = 1 + 2 * (localX * horizontal * scaledWidth + localY * vertical * scaledHeight)
          / (scaledWidth ** 2 + scaledHeight ** 2);
        const boundedFactor = Math.min(1.2 / Math.max(scaleX, scaleY), Math.max(.8 / Math.min(scaleX, scaleY), factor));
        state.scaleX = scaleX * boundedFactor;
        state.scaleY = scaleY * boundedFactor;
      } else {
        state.scaleX = clampScale(scaleX + 2 * localX * horizontal / width);
        state.scaleY = clampScale(scaleY + 2 * localY * vertical / height);
      }
    }
    renderTransform();
  });

  function finishGesture(event) {
    if (gesture?.pointerId !== event.pointerId) return;
    const { control, pointerId } = gesture;
    gesture = null;
    frame.removeAttribute("data-dragging");
    if (control.hasPointerCapture(pointerId)) control.releasePointerCapture(pointerId);
    scheduleReset();
  }

  frame.addEventListener("pointerup", finishGesture);
  frame.addEventListener("pointercancel", finishGesture);
  frame.addEventListener("lostpointercapture", finishGesture);
  frame.addEventListener("keydown", (event) => {
    const control = event.target.closest(".frame-handle, .frame-rotate");
    if (!control || !["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(event.key) || gesture) return;
    event.preventDefault();
    const step = ["ArrowRight", "ArrowUp"].includes(event.key) ? 1 : -1;
    if (control.hasAttribute("data-rotate")) {
      state.angle = clampAngle(state.angle + step * 2);
    } else {
      const direction = control.dataset.resize;
      if (direction !== "n" && direction !== "s") state.scaleX = clampScale(state.scaleX + step * .02);
      if (direction !== "w" && direction !== "e") state.scaleY = clampScale(state.scaleY + step * .02);
    }
    renderTransform();
    scheduleReset();
  });
}

document.querySelectorAll("[data-selection-frame]").forEach(setupSelectionFrame);

const workSlide = document.querySelector(".work-slide");
const slideHandle = workSlide.querySelector(".work-slide-handle");
let slideGesture;
let slideDragged = false;
let slideReset;

function positionHandle(offset, travel) {
  workSlide.style.setProperty("--slide-offset", `${offset}px`);
  workSlide.style.setProperty("--slide-progress", offset / travel);
}

slideHandle.addEventListener("pointerdown", (event) => {
  if (!event.isPrimary || event.button !== 0 || slideGesture) return;

  const travel = workSlide.clientWidth - slideHandle.offsetWidth - 2 * slideHandle.offsetLeft;
  if (travel <= 0) return;

  clearTimeout(slideReset);
  positionHandle(0, travel);
  slideGesture = { pointerId: event.pointerId, startX: event.clientX, travel };
  slideDragged = false;
  slideHandle.setPointerCapture(event.pointerId);
  workSlide.setAttribute("data-dragging", "");
});

slideHandle.addEventListener("pointermove", (event) => {
  if (slideGesture?.pointerId !== event.pointerId) return;

  const distance = event.clientX - slideGesture.startX;
  if (Math.abs(distance) > 6) slideDragged = true;
  positionHandle(Math.min(slideGesture.travel, Math.max(0, distance)), slideGesture.travel);
});

function finishSlide(event) {
  if (slideGesture?.pointerId !== event.pointerId) return;

  const { startX, travel } = slideGesture;
  slideGesture = null;
  workSlide.removeAttribute("data-dragging");

  if (event.type === "pointerup" && event.clientX - startX >= travel * 0.9) {
    slideDragged = true;
    positionHandle(travel, travel);
    slideHandle.click();
    slideReset = setTimeout(() => positionHandle(0, travel), 260);
  } else {
    positionHandle(0, travel);
  }
}

slideHandle.addEventListener("pointerup", finishSlide);
slideHandle.addEventListener("pointercancel", finishSlide);
slideHandle.addEventListener("lostpointercapture", finishSlide);
slideHandle.addEventListener("click", (event) => {
  if (event.detail > 0 && slideDragged) event.preventDefault();
});

const copy = document.querySelector("[data-copy-email]");
const status = document.querySelector(".copy-status");

if (navigator.clipboard?.writeText) {
  copy.hidden = false;
  copy.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(copy.dataset.copyEmail);
      status.textContent = "邮箱地址已复制";
    } catch {
      status.textContent = copy.dataset.copyEmail;
    }
  });
}
