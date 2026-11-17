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

const archive = document.querySelector(".work-archive");

function openArchiveForAnchor() {
  const target = document.getElementById(window.location.hash.slice(1));
  if (!target || !archive.contains(target)) return;
  archive.open = true;
  target.scrollIntoView();
}

document.querySelector('a[href="#all-work"]').addEventListener("click", () => {
  archive.open = true;
});
window.addEventListener("hashchange", openArchiveForAnchor);
openArchiveForAnchor();

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
