/*
  simulate.js — LoanIQ Live Simulator
  =====================================
  - Every input change fires schedulePrediction() debounced 150ms
  - POST /api/simulate → { prediction: "Approved"|"Rejected", confidence: 83.4 }
  - NO Supabase save — simulator is exploration only, keeps dashboard clean
  - Input IDs match predict.html exactly (gender, married, dependents, etc.)
    EXCEPT credit_history which is a radio toggle here, not a select
  - ApexCharts sparkline with sparkline:true — matches rest of project
  - Sparkline color updates to green/red based on last prediction
*/

let debounceTimer = null;
let sparkSeries = [];
let sparkChart = null;

const APPROVED_COLOR = "#22c55e";
const REJECTED_COLOR = "#ef4444";
const DIM_COLOR = "#dde4f0";

// ── DOM refs ──
const liveDot = document.getElementById("liveDot");
const resultVerdict = document.getElementById("resultVerdict");
const verdictBadge = document.getElementById("verdictBadge");
const confValue = document.getElementById("confValue");
const confFill = document.getElementById("confFill");
const summCredit = document.getElementById("summCredit");
const summIncome = document.getElementById("summIncome");
const summLoan = document.getElementById("summLoan");
const summArea = document.getElementById("summArea");

// ── Collect inputs ──
function getInputs() {
  return {
    gender: document.getElementById("gender").value,
    married: document.getElementById("married").value,
    dependents: document.getElementById("dependents").value,
    education: document.getElementById("education").value,
    self_employed: document.getElementById("self_employed").value,
    applicant_income: document.getElementById("applicant_income").value || "0",
    coapplicant_income:
      document.getElementById("coapplicant_income").value || "0",
    loan_amount: document.getElementById("loan_amount").value || "0",
    loan_term: document.getElementById("loan_term").value,
    credit_history:
      document.querySelector('input[name="creditHistory"]:checked')?.value ??
      "1",
    property_area: document.getElementById("property_area").value,
  };
}

// ── Bind all inputs ──
function bindEvents() {
  [
    "gender",
    "married",
    "dependents",
    "education",
    "self_employed",
    "loan_term",
    "property_area",
  ].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", schedulePrediction);
  });

  ["applicant_income", "coapplicant_income", "loan_amount"].forEach((id) => {
    document.getElementById(id)?.addEventListener("input", schedulePrediction);
  });

  document
    .querySelectorAll('input[name="creditHistory"]')
    .forEach((r) => r.addEventListener("change", schedulePrediction));
}

// ── Debounce 150ms ──
function schedulePrediction() {
  liveDot.classList.remove("active");
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(runPrediction, 150);
}

// ── Fire prediction ──
async function runPrediction() {
  const inputs = getInputs();
  if (parseFloat(inputs.applicant_income) <= 0) return;
  if (parseFloat(inputs.loan_amount) <= 0) return;

  try {
    const res = await fetch("/api/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(inputs),
    });
    const data = await res.json();
    if (data.error) throw new Error(data.error);

    updateResult(data.prediction, data.confidence, inputs);
    liveDot.classList.add("active");
  } catch (err) {
    console.error("Simulate error:", err.message);
  }
}

// ── Update result panel ──
function updateResult(prediction, confidence, inputs) {
  const isApproved = prediction === "Approved";

  resultVerdict.className =
    "result-verdict " + (isApproved ? "approved" : "rejected");
  verdictBadge.textContent = isApproved ? "✓ Approved" : "✗ Rejected";
  verdictBadge.classList.add("flash");
  setTimeout(() => verdictBadge.classList.remove("flash"), 350);

  confValue.textContent = confidence + "%";
  confFill.style.width = confidence + "%";

  // Summary panel
  summCredit.textContent = inputs.credit_history === "1" ? "Good" : "Bad";
  summCredit.className =
    "summary-val " + (inputs.credit_history === "1" ? "good" : "bad");
  summIncome.textContent =
    "₹" + Number(inputs.applicant_income).toLocaleString("en-IN");
  summLoan.textContent =
    "₹" + Number(inputs.loan_amount).toLocaleString("en-IN") + "k";
  summArea.textContent = inputs.property_area;

  // Sparkline
  sparkSeries.push({ y: confidence, approved: isApproved });
  if (sparkSeries.length > 20) sparkSeries.shift();
  updateSparkline(isApproved);
}

// ── Sparkline ──
function initSparkline() {
  sparkChart = new ApexCharts(document.getElementById("sparklineChart"), {
    chart: {
      type: "line",
      height: 75,
      sparkline: { enabled: true },
      animations: { enabled: false },
    },
    series: [{ data: [] }],
    stroke: { curve: "smooth", width: 2 },
    colors: [DIM_COLOR],
    tooltip: {
      fixed: { enabled: false },
      x: { show: false },
      y: { formatter: (v) => v + "% confidence" },
      marker: { show: false },
    },
  });
  sparkChart.render();
}

function updateSparkline(isApproved) {
  if (!sparkChart) return;
  sparkChart.updateOptions(
    {
      colors: [isApproved ? APPROVED_COLOR : REJECTED_COLOR],
      series: [{ data: sparkSeries.map((p) => p.y) }],
    },
    false,
    false,
  );
}

// ── Init ──
bindEvents();
initSparkline();
runPrediction();
