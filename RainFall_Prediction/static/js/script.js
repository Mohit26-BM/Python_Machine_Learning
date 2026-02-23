/* ─────────────────────────────────────────────
   RainCast · script.js
   Effects:
   1. Scroll-triggered section reveal
   2. Count-up animation for stat values & table numbers
   3. Influence bar animate-in on scroll
   4. Table row hover full-row highlight
───────────────────────────────────────────── */

/* ── 1. SCROLL-TRIGGERED SECTION REVEAL ──────
   Adds .visible to .section elements as they
   enter the viewport. CSS handles the fade/slide. */

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        revealObserver.unobserve(entry.target); // fire once only
      }
    });
  },
  { threshold: 0.1 },
);

document.querySelectorAll(".section").forEach((el) => {
  el.classList.add("reveal");
  revealObserver.observe(el);
});

/* ── 2. COUNT-UP ANIMATION ───────────────────
   Targets .stat-value and .tnum elements.
   Parses their text, animates from 0 to the
   final value over ~1.2s when scrolled into view. */

function parseNumber(text) {
  const clean = text.trim().replace("%", "");
  return parseFloat(clean);
}

function formatNumber(val, original) {
  const isPercent = original.includes("%");
  const decimals = original.includes(".")
    ? original.split(".")[1].replace("%", "").length
    : 0;
  const formatted = val.toFixed(decimals);
  return isPercent ? formatted + "%" : formatted;
}

function animateCountUp(el) {
  const original = el.textContent.trim();
  const target = parseNumber(original);

  // Skip non-numeric cells (e.g. "—")
  if (isNaN(target)) return;

  const duration = 1200;
  const start = performance.now();

  function step(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = formatNumber(target * eased, original);
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = original; // snap to exact final value
  }

  requestAnimationFrame(step);
}

const countObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // Stat cards in hero panel
        entry.target.querySelectorAll(".stat-value").forEach(animateCountUp);
        // Table numbers
        entry.target.querySelectorAll(".tnum").forEach(animateCountUp);
        // Dataset strip numbers
        entry.target.querySelectorAll(".ds-num").forEach(animateCountUp);
        countObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.2 },
);

// Observe hero panel and each section separately
document.querySelectorAll(".stats-panel, .section").forEach((el) => {
  countObserver.observe(el);
});

/* ── 3. INFLUENCE BAR ANIMATE-IN ─────────────
   Bars start at width:0 in CSS via a class,
   then animate to their actual width when the
   features section scrolls into view. */

const barObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.querySelectorAll(".influence-bar-fill").forEach((bar) => {
          // Read the target width set inline, reset to 0, then animate
          const targetWidth = bar.style.width;
          bar.style.width = "0%";
          // Small delay so the reset is painted before we animate
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              bar.style.transition = "width 1s cubic-bezier(0.4, 0, 0.2, 1)";
              bar.style.width = targetWidth;
            });
          });
        });
        barObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 },
);

document
  .querySelectorAll(".features-grid")
  .forEach((el) => barObserver.observe(el));

/* ── 4. TABLE ROW HOVER HIGHLIGHT ────────────
   When hovering any cell in a .trow, highlights
   the whole row with a subtle background tint. */

document.querySelectorAll(".trow").forEach((row) => {
  row.addEventListener("mouseenter", () => {
    row.querySelectorAll("td").forEach((td) => {
      td.style.background = "rgba(0, 210, 255, 0.04)";
    });
    // Keep the featured column slightly brighter
    row.querySelectorAll(".tcol-featured").forEach((td) => {
      td.style.background = "rgba(0, 210, 255, 0.08)";
    });
  });

  row.addEventListener("mouseleave", () => {
    row.querySelectorAll("td").forEach((td) => {
      td.style.background = "";
    });
    row.querySelectorAll(".tcol-featured").forEach((td) => {
      td.style.background = "rgba(0, 210, 255, 0.03)";
    });
  });
});
