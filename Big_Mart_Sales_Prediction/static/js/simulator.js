const DATASET_AVG = 2181;
const ACCENT = "#6366f1";

const history = [];
const MAX_HISTORY = 20;
let sparkChart = null;
let debounceTimer = null;
let lastPrediction = null;

// ── DOM refs ──
const liveDot = document.getElementById("liveDot");
const resultMain = document.getElementById("resultMain");
const resultValue = document.getElementById("resultValue");
const resultVsAvg = document.getElementById("resultVsAvg");
const resultDelta = document.getElementById("resultDelta");
const impactOutlet = document.getElementById("impactOutlet");
const impactMRP = document.getElementById("impactMRP");
const impactYear = document.getElementById("impactYear");
const impactLoc = document.getElementById("impactLoc");
const impactItemType = document.getElementById("impactItemType");
const impactVis = document.getElementById("impactVis");

// ── Slider display bindings ──
function bindSlider(sliderId, displayId, formatter) {
  const slider = document.getElementById(sliderId);
  const display = document.getElementById(displayId);
  display.textContent = formatter(slider.value);
  slider.addEventListener("input", () => {
    display.textContent = formatter(slider.value);
    schedulePrediction();
  });
}

bindSlider("sliderMRP", "valMRP", (v) => "₹" + parseFloat(v).toFixed(2));
bindSlider(
  "sliderWeight",
  "valWeight",
  (v) => parseFloat(v).toFixed(1) + " kg",
);
bindSlider("sliderVisibility", "valVisibility", (v) =>
  parseFloat(v).toFixed(3),
);

// ── Select bindings ──
[
  "selFatContent",
  "selItemType",
  "selOutletSize",
  "selLocation",
  "selOutletType",
  "sliderYear",
  "selOutletIdentifier",
].forEach((id) =>
  document.getElementById(id).addEventListener("change", schedulePrediction),
);

// ── Debounce ──
function schedulePrediction() {
  liveDot.classList.remove("active");
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(runPrediction, 120);
}

// ── Collect inputs ──
function getInputs() {
  return {
    Item_Weight: parseFloat(document.getElementById("sliderWeight").value),
    Item_Fat_Content: document.getElementById("selFatContent").value,
    Item_Visibility: parseFloat(
      document.getElementById("sliderVisibility").value,
    ),
    Item_Type: document.getElementById("selItemType").value,
    Item_MRP: parseFloat(document.getElementById("sliderMRP").value),
    Outlet_Establishment_Year: parseInt(
      document.getElementById("sliderYear").value,
    ),
    Outlet_Size: document.getElementById("selOutletSize").value,
    Outlet_Location_Type: document.getElementById("selLocation").value,
    Outlet_Type: document.getElementById("selOutletType").value,
    Outlet_Identifier: document.getElementById("selOutletIdentifier").value,
  };
}

// ── Fire prediction ──
async function runPrediction() {
  const inputs = getInputs();
  resultMain.classList.add("updating");

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(inputs),
    });
    const data = await res.json();
    if (!data.success) throw new Error(data.error);

    const val = data.prediction;

    // Main display
    resultMain.classList.remove("updating");
    resultMain.classList.add("has-result");
    resultValue.textContent =
      "₹" + val.toLocaleString("en-IN", { maximumFractionDigits: 0 });
    resultValue.classList.add("flash");
    setTimeout(() => resultValue.classList.remove("flash"), 400);

    // vs average badge
    const diff = (((val - DATASET_AVG) / DATASET_AVG) * 100).toFixed(1);
    const isUp = parseFloat(diff) >= 0;
    resultVsAvg.textContent = (isUp ? "+" : "") + diff + "% vs avg";
    resultVsAvg.className = "result-vs-avg " + (isUp ? "up" : "down");

    // Delta from last prediction
    if (lastPrediction !== null) {
      const delta = val - lastPrediction;
      if (Math.abs(delta) >= 1) {
        const sign = delta > 0 ? "+" : "";
        resultDelta.textContent =
          sign + "₹" + Math.round(delta).toLocaleString("en-IN") + " from last";
        resultDelta.className = "result-delta " + (delta > 0 ? "up" : "down");
        resultDelta.style.display = "block";
      } else {
        resultDelta.style.display = "none";
      }
    }
    lastPrediction = val;

    // Live dot
    liveDot.classList.add("active");

    // Sparkline
    history.push(val);
    if (history.length > MAX_HISTORY) history.shift();
    updateSparkline();

    // Impact panel
    updateImpact(inputs);
  } catch (err) {
    resultMain.classList.remove("updating");
    console.error("Prediction error:", err.message);
  }
}

// ── Sparkline ──
function updateSparkline() {
  const ctx = document.getElementById("sparklineChart");
  if (!ctx) return;

  if (sparkChart) {
    sparkChart.data.labels = history.map((_, i) => i + 1);
    sparkChart.data.datasets[0].data = history;
    sparkChart.update("none");
  } else {
    sparkChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: history.map((_, i) => i + 1),
        datasets: [
          {
            data: history,
            borderColor: ACCENT,
            backgroundColor: "rgba(99,102,241,0.08)",
            borderWidth: 1.5,
            fill: true,
            tension: 0.4,
            pointRadius: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        plugins: { legend: { display: false }, tooltip: { enabled: false } },
        scales: {
          x: { display: false },
          y: {
            display: true,
            grid: { color: "rgba(255,255,255,0.04)" },
            ticks: {
              callback: (v) => "₹" + (v / 1000).toFixed(0) + "k",
              maxTicksLimit: 3,
              font: { size: 10 },
            },
          },
        },
      },
    });
  }
}

// ── Impact panel ──
function updateImpact(inputs) {
  impactOutlet.textContent = inputs.Outlet_Type;
  impactMRP.textContent = "₹" + inputs.Item_MRP.toFixed(0);
  impactYear.textContent = inputs.Outlet_Establishment_Year;
  impactLoc.textContent = inputs.Outlet_Location_Type;
  impactItemType.textContent = inputs.Item_Type;
  impactVis.textContent = inputs.Item_Visibility.toFixed(3);
}

// ── Run on load ──
runPrediction();