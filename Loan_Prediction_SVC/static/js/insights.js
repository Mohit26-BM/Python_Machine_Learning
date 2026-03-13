/*
  insights.js — Coefficient Diverging Bar Chart
  ===============================================
  Renders one ApexCharts horizontal bar chart using data injected
  by Flask via window.COEFFICIENTS (set in insights.html script block).

  Chart is horizontal bar — positive values go right (green),
  negative go left (red). ApexCharts handles this automatically
  when values are negative.

  Colors are assigned per-bar using the colors array trick:
  map each coefficient to green/red/grey based on sign.
*/

const COEFFICIENTS = window.COEFFICIENTS;

const FEATURE_LABELS = {
  Credit_History: "Credit History",
  Married: "Married",
  Education: "Education",
  Gender: "Gender",
  Property_Area: "Property Area",
  Dependents: "Dependents",
  Self_Employed: "Self Employed",
  LoanAmount: "Loan Amount",
  Loan_Amount_Term: "Loan Term",
  ApplicantIncome: "Applicant Income",
  CoapplicantIncome: "Co-applicant Income",
};

const POS_COLOR = "#22c55e";
const NEG_COLOR = "#ef4444";
const NEU_COLOR = "#a0d8e6";

function getColor(val) {
  if (val > 0.01) return POS_COLOR;
  if (val < -0.01) return NEG_COLOR;
  return NEU_COLOR;
}

function renderChart() {
  // Sort by absolute value descending
  const sorted = Object.entries(COEFFICIENTS).sort(
    (a, b) => Math.abs(b[1]) - Math.abs(a[1]),
  );

  const labels = sorted.map(([k]) => FEATURE_LABELS[k] || k);
  const values = sorted.map(([, v]) => v);
  const colors = values.map(getColor);

  new ApexCharts(document.getElementById("coeffChart"), {
    chart: {
      type: "bar",
      height: 420,
      fontFamily: "'DM Sans', sans-serif",
      toolbar: { show: false },
      animations: { enabled: true, speed: 600 },
    },
    plotOptions: {
      bar: {
        horizontal: true,
        borderRadius: 4,
        distributed: true,
        dataLabels: { position: "top" },
      },
    },
    series: [{ name: "Coefficient", data: values }],
    xaxis: {
      categories: labels,
      labels: {
        style: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px" },
        formatter: (v) => v.toFixed(2),
      },
      axisBorder: { show: true, color: "#dde4f0" },
      crosshairs: { show: false },
    },
    yaxis: {
      labels: {
        style: {
          fontFamily: "'DM Sans', sans-serif",
          fontSize: "13px",
          fontWeight: 500,
          colors: "#2d3a52",
        },
      },
    },
    colors,
    legend: { show: false },
    dataLabels: {
      enabled: true,
      formatter: (v) => (v === 0 || Math.abs(v) < 0.001 ? "~0" : v.toFixed(4)),
      style: {
        fontFamily: "'DM Sans', sans-serif",
        fontSize: "11px",
        fontWeight: 600,
        colors: ["#2d3a52"],
      },
      offsetX: 4,
    },
    grid: {
      borderColor: "#dde4f0",
      xaxis: { lines: { show: true } },
      yaxis: { lines: { show: false } },
    },
    tooltip: {
      y: {
        formatter: (v, { dataPointIndex }) => {
          const feat = sorted[dataPointIndex][0];
          const coef = v.toFixed(4);
          const dir =
            v > 0.01
              ? "→ Pushes toward Approved"
              : v < -0.01
                ? "→ Pushes toward Rejected"
                : "→ Negligible effect";
          return `${coef} ${dir}`;
        },
      },
      style: { fontFamily: "'DM Sans', sans-serif" },
    },
  }).render();
}

renderChart();