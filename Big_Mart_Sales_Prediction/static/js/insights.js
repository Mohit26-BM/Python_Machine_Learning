Chart.defaults.color = "#6b6b7e";
Chart.defaults.font.family = "Inter, sans-serif";
Chart.defaults.font.size = 11;

const ACCENT = "#6366f1";
const PALETTE = [
  "#6366f1",
  "#818cf8",
  "#a5b4fc",
  "#c7d2fe",
  "#34d399",
  "#6ee7b7",
  "#d1fae5",
  "#f59e0b",
  "#fbbf24",
];

const DESCRIPTIONS = {
  "Item MRP":
    "The maximum retail price of the item. Higher-priced items consistently drive higher sales revenue.",
  "Outlet Type":
    "The category of outlet — supermarkets vs grocery stores differ substantially in sales volume.",
  "Item Visibility":
    "How prominently the item is displayed in the store. Lower visibility can suppress sales.",
  "Outlet Location Type":
    "Whether the outlet is in a Tier 1, 2, or 3 city affects foot traffic and purchasing power.",
  "Item Weight":
    "Physical weight of the item, a proxy for item size and category.",
  "Outlet Size":
    "Small, Medium, or High — larger outlets tend to move more volume.",
  "Item Type":
    "The product category. Some categories like Dairy and Snack Foods outperform others.",
  "Item Fat Content": "Low Fat vs Regular classification of the item.",
  "Outlet Identifier":
    "The specific outlet ID — captures outlet-level fixed effects.",
  "Outlet Year":
    "Establishment year. Older outlets may have a more loyal, established customer base.",
};

const TAKEAWAYS = {
  "Item MRP":
    "Pricing is the single strongest lever for sales. Items with higher MRP generate more revenue, suggesting premium pricing drives BigMart's sales.",
  "Outlet Type":
    "Supermarket Type3 outlets significantly outperform grocery stores. Outlet format matters as much as product choice.",
  "Item Visibility":
    "Shelf placement has a measurable impact. Items with lower visibility scores tend to underperform even when priced well.",
  "Outlet Location Type":
    "Tier 1 city outlets perform differently from Tier 3. Urban market size and consumer income both factor in.",
};

async function loadInsights() {
  try {
    const res = await fetch("/api/feature-importance");
    const json = await res.json();

    if (!json.success) throw new Error(json.error);

    const data = json.data;

    renderChart(data);
    renderTopFeature(data[0]);
    renderRankList(data);
    renderTakeaways(data);
  } catch (err) {
    document.getElementById("loadingState").textContent =
      "Error: " + err.message;
  }
}

function renderChart(data) {
  document.getElementById("loadingState").style.display = "none";
  document.getElementById("chartImportance").style.display = "block";

  new Chart(document.getElementById("chartImportance"), {
    type: "bar",
    data: {
      labels: data.map((d) => d.feature),
      datasets: [
        {
          data: data.map((d) => d.pct),
          backgroundColor: data.map((_, i) => PALETTE[i] || "#4a4a58"),
          borderRadius: 4,
          borderSkipped: false,
        },
      ],
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => " " + ctx.parsed.x.toFixed(1) + "% importance",
          },
        },
      },
      scales: {
        x: {
          grid: { color: "rgba(255,255,255,0.04)" },
          ticks: { callback: (v) => v + "%" },
        },
        y: {
          grid: { display: false },
          ticks: { font: { size: 11, weight: "500" } },
        },
      },
    },
  });
}

function renderTopFeature(top) {
  document.getElementById("topFeatureLoading").style.display = "none";
  document.getElementById("topFeatureContent").style.display = "block";

  document.getElementById("topFeatureName").textContent = top.feature;
  document.getElementById("topFeaturePct").textContent = top.pct + "%";
  document.getElementById("topFeatureDesc").textContent =
    DESCRIPTIONS[top.feature] ||
    "This feature has the highest contribution to the model's predictions.";
}

function renderRankList(data) {
  const list = document.getElementById("rankList");
  list.innerHTML = data
    .map((d, i) => {
      const tierClass = i === 0 ? "top" : i < 3 ? "mid" : "low";
      return `
      <div class="rank-row">
        <div class="rank-row-header">
          <span class="rank-name">${i + 1}. ${d.feature}</span>
          <span class="rank-pct">${d.pct}%</span>
        </div>
        <div class="rank-bar-bg">
          <div class="rank-bar-fill ${tierClass}" style="width:${d.pct}%"></div>
        </div>
      </div>`;
    })
    .join("");
}

function renderTakeaways(data) {
  const items = data.filter((d) => TAKEAWAYS[d.feature]).slice(0, 3);

  if (items.length === 0) return;

  const box = document.getElementById("takeawayBox");
  const list = document.getElementById("takeawayList");

  list.innerHTML = items
    .map(
      (d, i) => `
    <div class="takeaway-item">
      <span class="takeaway-num">0${i + 1}</span>
      <span><strong>${d.feature}</strong> — ${TAKEAWAYS[d.feature]}</span>
    </div>`,
    )
    .join("");

  box.style.display = "block";
}

loadInsights();