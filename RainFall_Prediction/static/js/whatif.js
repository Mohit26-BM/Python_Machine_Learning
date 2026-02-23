/* ─── What-If Simulator · whatif.js ─── */

const sliders = {
  pressure: document.getElementById("sl-pressure"),
  dewpoint: document.getElementById("sl-dewpoint"),
  humidity: document.getElementById("sl-humidity"),
  cloud: document.getElementById("sl-cloud"),
  sunshine: document.getElementById("sl-sunshine"),
  winddirection: document.getElementById("sl-winddirection"),
  windspeed: document.getElementById("sl-windspeed"),
};

const displays = {
  pressure: document.getElementById("val-pressure"),
  dewpoint: document.getElementById("val-dewpoint"),
  humidity: document.getElementById("val-humidity"),
  cloud: document.getElementById("val-cloud"),
  sunshine: document.getElementById("val-sunshine"),
  winddirection: document.getElementById("val-winddirection"),
  windspeed: document.getElementById("val-windspeed"),
};

const liveCard = document.getElementById("liveCard");
const liveIcon = document.getElementById("liveIcon");
const iconSvg = document.getElementById("iconSvg");
const liveVerdict = document.getElementById("liveVerdict");
const livePct = document.getElementById("livePct");
const liveRing = document.getElementById("liveRing");
const circumference = 345.4;

const SUN_SVG = `
  <circle cx="12" cy="12" r="5" stroke="rgba(255,190,60,0.9)"/>
  <line x1="12" y1="1"  x2="12" y2="3"  stroke="rgba(255,190,60,0.9)"/>
  <line x1="12" y1="21" x2="12" y2="23" stroke="rgba(255,190,60,0.9)"/>
  <line x1="4.22" y1="4.22"   x2="5.64" y2="5.64"   stroke="rgba(255,190,60,0.9)"/>
  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="rgba(255,190,60,0.9)"/>
  <line x1="1"  y1="12" x2="3"  y2="12" stroke="rgba(255,190,60,0.9)"/>
  <line x1="21" y1="12" x2="23" y2="12" stroke="rgba(255,190,60,0.9)"/>
  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"   stroke="rgba(255,190,60,0.9)"/>
  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"   stroke="rgba(255,190,60,0.9)"/>`;

const RAIN_SVG = `
  <path d="M20 17.58A5 5 0 0 0 18 8h-1.26A8 8 0 1 0 4 16.25" stroke="rgba(0,180,255,0.9)"/>
  <line x1="8"  y1="19" x2="8"  y2="21" stroke="rgba(0,180,255,0.9)"/>
  <line x1="8"  y1="13" x2="8"  y2="15" stroke="rgba(0,180,255,0.9)"/>
  <line x1="12" y1="15" x2="12" y2="17" stroke="rgba(0,180,255,0.9)"/>
  <line x1="12" y1="21" x2="12" y2="23" stroke="rgba(0,180,255,0.9)"/>
  <line x1="16" y1="13" x2="16" y2="15" stroke="rgba(0,180,255,0.9)"/>
  <line x1="16" y1="19" x2="16" y2="21" stroke="rgba(0,180,255,0.9)"/>`;

/* ── Debounce ── */
let debounceTimer = null;
function debounce(fn, delay = 180) {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(fn, delay);
}

/* ── Sync slider display values ── */
Object.entries(sliders).forEach(([key, slider]) => {
  slider.addEventListener("input", () => {
    displays[key].textContent = slider.value;
    debounce(fetchPrediction);
  });
});

/* ── Fetch prediction from API ── */
async function fetchPrediction() {
  const payload = {};
  Object.entries(sliders).forEach(([key, el]) => {
    payload[key] = parseFloat(el.value);
  });

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    updateUI(data.prediction, data.probability);
  } catch (e) {
    console.error("Prediction error:", e);
  }
}

/* ── Update UI ── */
function updateUI(prediction, probability) {
  const isRain = prediction === "Rainfall Expected";

  liveCard.className = `live-card ${isRain ? "rain" : "no-rain"}`;
  liveIcon.className = `live-icon ${isRain ? "rain" : "no-rain"}`;
  liveVerdict.className = `live-verdict ${isRain ? "rain" : "no-rain"}`;

  iconSvg.innerHTML = isRain ? RAIN_SVG : SUN_SVG;
  liveVerdict.textContent = prediction;
  livePct.textContent = probability.toFixed(1) + "%";

  liveRing.setAttribute("stroke", isRain ? "var(--cyan)" : "var(--warning)");
  liveRing.style.strokeDashoffset =
    circumference - (probability / 100) * circumference;
}

/* ── Presets ── */
const presets = {
  dry: {
    pressure: 1025.9,
    dewpoint: 8.0,
    humidity: 35,
    cloud: 10,
    sunshine: 11.0,
    winddirection: 80,
    windspeed: 10,
  },
  rain: {
    pressure: 1008.0,
    dewpoint: 18.0,
    humidity: 92,
    cloud: 90,
    sunshine: 0.2,
    winddirection: 160,
    windspeed: 35,
  },
  humid: {
    pressure: 1012.0,
    dewpoint: 17.0,
    humidity: 82,
    cloud: 78,
    sunshine: 1.5,
    winddirection: 130,
    windspeed: 22,
  },
  avg: {
    pressure: 1017.0,
    dewpoint: 14.0,
    humidity: 65,
    cloud: 50,
    sunshine: 5.5,
    winddirection: 180,
    windspeed: 20,
  },
};

document.querySelectorAll(".preset-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const p = presets[btn.dataset.preset];
    Object.entries(p).forEach(([key, val]) => {
      sliders[key].value = val;
      displays[key].textContent = val;
    });
    fetchPrediction();
  });
});

/* ── Initial load ── */
fetchPrediction();