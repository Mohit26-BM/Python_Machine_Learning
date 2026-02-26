// ── Replace with your Supabase project credentials ──
const SUPABASE_URL = "https://yuqvbrllnbtqcdhevdto.supabase.co";
const SUPABASE_ANON_KEY ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1cXZicmxsbmJ0cWNkaGV2ZHRvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTE2NzMsImV4cCI6MjA4NzE2NzY3M30.97JCdF07Fc-YQ2z2RXv3V-9o2C66WLMzydKBY_VGktU";


const { createClient } = supabase;
const sb = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

Chart.defaults.color = "#6b6b7e";
Chart.defaults.font.family = "Inter, sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.borderColor = "rgba(255,255,255,0.05)";

const ACCENT = "#6366f1";
const GREEN = "#34d399";
const PALETTE = [
  "#6366f1",
  "#34d399",
  "#f59e0b",
  "#ec4899",
  "#22d3ee",
  "#a78bfa",
];

const fmt = (v) =>
  "\u20B9" + Number(v).toLocaleString("en-IN", { maximumFractionDigits: 0 });
const groupBy = (arr, key) =>
  arr.reduce((acc, r) => {
    const k = r[key] || "Unknown";
    (acc[k] = acc[k] || []).push(r);
    return acc;
  }, {});
const avgOf = (arr, key) =>
  arr.reduce((s, r) => s + (parseFloat(r[key]) || 0), 0) / arr.length;

async function loadData() {
  try {
    const { data, error } = await sb
      .from("bigmart_predictions")
      .select("*")
      .order("created_at", { ascending: false });

    if (error) throw error;
    if (!data || data.length === 0) {
      showEmpty();
      return;
    }

    renderKPIs(data);
    renderTimeline(data);
    renderOutletType(data);
    renderHistogram(data);
    renderLocation(data);
    renderScatter(data);
    renderTable(data.slice(0, 10));
  } catch (err) {
    document.getElementById("tableWrap").innerHTML =
      `<div class="state-box"><strong>Could not connect to Supabase</strong>${err.message}<br><br>Set your SUPABASE_URL and SUPABASE_ANON_KEY in dashboard.js</div>`;
  }
}

function showEmpty() {
  document.getElementById("tableWrap").innerHTML =
    '<div class="state-box"><strong>No predictions yet</strong>Use the Predictor to make your first prediction, then come back here.</div>';
}

/* ── KPIs ── */
function renderKPIs(data) {
  const sales = data.map((r) => parseFloat(r.predicted_sales) || 0);
  const avg = sales.reduce((a, b) => a + b, 0) / sales.length;
  const max = Math.max(...sales);
  const DATASET_AVG = 2181;
  const diff = (((avg - DATASET_AVG) / DATASET_AVG) * 100).toFixed(1);

  document.getElementById("kpiTotal").textContent =
    data.length.toLocaleString();
  document.getElementById("kpiTotalSub").textContent = "all time";

  document.getElementById("kpiAvg").textContent = fmt(avg);
  const diffEl = document.getElementById("kpiAvgSub");
  diffEl.textContent =
    (parseFloat(diff) >= 0 ? "+" : "") + diff + "% vs \u20B92,181 avg";
  diffEl.className =
    "kpi-sub " + (parseFloat(diff) >= 0 ? "kpi-up" : "kpi-down");

  document.getElementById("kpiMax").textContent = fmt(max);
  document.getElementById("kpiMaxSub").textContent = "single prediction";

  const byOutlet = groupBy(data, "outlet_type");
  const topOutlet = Object.entries(byOutlet).sort(
    (a, b) => b[1].length - a[1].length,
  )[0];
  if (topOutlet) {
    document.getElementById("kpiOutlet").textContent = topOutlet[0];
    document.getElementById("kpiOutletSub").textContent =
      topOutlet[1].length + " of " + data.length + " predictions";
  }
}

/* ── Timeline ── */
function renderTimeline(data) {
  const byDate = {};
  data.forEach((r) => {
    const d = (r.created_at || "").slice(0, 10);
    if (d) byDate[d] = (byDate[d] || 0) + 1;
  });
  const sorted = Object.entries(byDate).sort((a, b) =>
    a[0].localeCompare(b[0]),
  );

  new Chart(document.getElementById("chartTimeline"), {
    type: "line",
    data: {
      labels: sorted.map(([d]) => d),
      datasets: [
        {
          data: sorted.map(([, c]) => c),
          borderColor: ACCENT,
          backgroundColor: "rgba(99,102,241,0.08)",
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 3,
          pointBackgroundColor: ACCENT,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          grid: { color: "rgba(255,255,255,0.04)" },
          ticks: { maxTicksLimit: 7 },
        },
        y: {
          grid: { color: "rgba(255,255,255,0.04)" },
          beginAtZero: true,
          ticks: { precision: 0 },
        },
      },
    },
  });
}

/* ── Outlet Type bar ── */
function renderOutletType(data) {
  const groups = groupBy(data, "outlet_type");
  const labels = Object.keys(groups);
  const avgs = labels.map((k) => avgOf(groups[k], "predicted_sales"));

  new Chart(document.getElementById("chartOutletType"), {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          data: avgs,
          backgroundColor: PALETTE.slice(0, labels.length),
          borderRadius: 5,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { maxRotation: 20 } },
        y: {
          grid: { color: "rgba(255,255,255,0.04)" },
          ticks: { callback: (v) => "\u20B9" + (v / 1000).toFixed(1) + "k" },
        },
      },
    },
  });
}

/* ── Histogram ── */
function renderHistogram(data) {
  const vals = data
    .map((r) => parseFloat(r.predicted_sales) || 0)
    .filter(Boolean);
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  const BIN_N = 10;
  const binSize = (max - min) / BIN_N;
  const bins = Array(BIN_N).fill(0);
  const labels = Array.from(
    { length: BIN_N },
    (_, i) => "\u20B9" + Math.round((min + i * binSize) / 1000) + "k",
  );

  vals.forEach((v) => {
    const idx = Math.min(Math.floor((v - min) / binSize), BIN_N - 1);
    bins[idx]++;
  });

  new Chart(document.getElementById("chartHistogram"), {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          data: bins,
          backgroundColor: "rgba(99,102,241,0.55)",
          borderColor: ACCENT,
          borderWidth: 1,
          borderRadius: 3,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        y: {
          grid: { color: "rgba(255,255,255,0.04)" },
          beginAtZero: true,
          ticks: { precision: 0 },
        },
      },
    },
  });
}

/* ── Location doughnut ── */
function renderLocation(data) {
  const groups = groupBy(data, "outlet_location");
  const labels = Object.keys(groups);
  const counts = labels.map((k) => groups[k].length);

  new Chart(document.getElementById("chartLocation"), {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          data: counts,
          backgroundColor: PALETTE.slice(0, labels.length),
          borderWidth: 0,
          hoverOffset: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "65%",
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            padding: 14,
            usePointStyle: true,
            pointStyleWidth: 8,
            font: { size: 11 },
          },
        },
      },
    },
  });
}

/* ── MRP vs Sales scatter ── */
function renderScatter(data) {
  const points = data
    .filter((r) => r.item_mrp && r.predicted_sales)
    .map((r) => ({
      x: parseFloat(r.item_mrp),
      y: parseFloat(r.predicted_sales),
    }));

  new Chart(document.getElementById("chartScatter"), {
    type: "scatter",
    data: {
      datasets: [
        {
          data: points,
          backgroundColor: "rgba(99,102,241,0.45)",
          borderColor: "rgba(99,102,241,0.7)",
          borderWidth: 1,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          grid: { color: "rgba(255,255,255,0.04)" },
          title: {
            display: true,
            text: "Item MRP (\u20B9)",
            color: "#6b6b7e",
            font: { size: 11 },
          },
        },
        y: {
          grid: { color: "rgba(255,255,255,0.04)" },
          title: {
            display: true,
            text: "Predicted Sales (\u20B9)",
            color: "#6b6b7e",
            font: { size: 11 },
          },
          ticks: { callback: (v) => "\u20B9" + (v / 1000).toFixed(1) + "k" },
        },
      },
    },
  });
}

/* ── Recent predictions table ── */
function renderTable(rows) {
  const thead = `<thead><tr>
    <th>#</th>
    <th>Outlet Type</th>
    <th>Location</th>
    <th>Item Type</th>
    <th>Fat Content</th>
    <th>Item MRP</th>
    <th>Outlet Size</th>
    <th>Predicted Sales</th>
    <th>Date</th>
  </tr></thead>`;

  const tbody = rows
    .map(
      (r, i) => `<tr>
    <td>${i + 1}</td>
    <td>${r.outlet_type || "—"}</td>
    <td>${r.outlet_location || "—"}</td>
    <td>${r.item_type || "—"}</td>
    <td>${r.item_fat_content || "—"}</td>
    <td>${r.item_mrp ? fmt(r.item_mrp) : "—"}</td>
    <td>${r.outlet_size || "—"}</td>
    <td class="td-primary">${r.predicted_sales ? fmt(r.predicted_sales) : "—"}</td>
    <td>${(r.created_at || "").slice(0, 10) || "—"}</td>
  </tr>`,
    )
    .join("");

  document.getElementById("tableWrap").innerHTML =
    `<div style="overflow-x:auto"><table class="dash-table">${thead}<tbody>${tbody}</tbody></table></div>`;
}

loadData();