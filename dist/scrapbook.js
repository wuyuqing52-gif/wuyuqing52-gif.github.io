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
