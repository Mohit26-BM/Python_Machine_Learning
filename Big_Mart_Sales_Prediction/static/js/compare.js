/*
  compare.js — Scenario Comparison Logic
  =======================================

  FLOW:
  1. User fills shared item fields + two outlet columns
  2. Clicks Compare → both scenarios sent to /api/compare in one request
  3. Results revealed: scores, bar chart, % diff, input diff table, recommendation

  SHARED vs SCENARIO FIELDS:
  - Item_Weight, Item_Fat_Content, Item_Visibility, Item_Type, Item_MRP
    are shared — collected once, copied into both payloads before sending
  - Outlet_Type, Outlet_Size, Outlet_Location_Type, Outlet_Establishment_Year
    are per-scenario — each panel has its own selects

  RECOMMENDATION LOGIC:
  - Generated from the actual difference and which outlet fields differ
  - Not a hardcoded string — built dynamically from the result values
  - Keeps it grounded in the actual comparison rather than generic text

  IMPORTANT:
  - Do NOT send to /api/predict twice — use /api/compare which batches both
  - Bar chart widths are CSS-animated, not Chart.js — keep it that way
  - Only show diff table rows where A value !== B value
  - If predictions are within ₹10 of each other, show a "negligible difference"
    message instead of a winner badge
*/

const DATASET_AVG = 2181;

const fmt = (v) =>
  "₹" + Number(v).toLocaleString("en-IN", { maximumFractionDigits: 0 });

// ── Collect shared item fields ──
function getSharedFields() {
  return {
    Item_Weight: parseFloat(document.getElementById("sharedWeight").value),
    Item_Fat_Content: document.getElementById("sharedFatContent").value,
    Item_Visibility: parseFloat(
      document.getElementById("sharedVisibility").value,
    ),
    Item_Type: document.getElementById("sharedItemType").value,
    Item_MRP: parseFloat(document.getElementById("sharedMRP").value),
  };
}

// ── Collect per-scenario outlet fields ──
function getScenario(prefix) {
  return {
    Outlet_Type: document.getElementById(prefix + "OutletType").value,
    Outlet_Size: document.getElementById(prefix + "OutletSize").value,
    Outlet_Location_Type: document.getElementById(prefix + "Location").value,
    Outlet_Establishment_Year: parseInt(
      document.getElementById(prefix + "Year").value,
    ),
    Outlet_Identifier: document.getElementById(prefix + "OutletIdentifier")
      .value,
  };
}

// ── Validate ──
function validate(shared, a, b) {
  const sharedVals = Object.values(shared);
  const allVals = [...sharedVals, ...Object.values(a), ...Object.values(b)];

  return allVals.every(
    (v) =>
      v !== "" &&
      v !== null &&
      v !== undefined &&
      !(typeof v === "number" && isNaN(v)),
  );
}

// ── Main compare handler ──
async function runCompare() {
  const btn = document.getElementById("compareBtn");
  const errorEl = document.getElementById("compareError");

  const shared = getSharedFields();
  const scenA = getScenario("a");
  const scenB = getScenario("b");

  if (!validate(shared, scenA, scenB)) {
    errorEl.textContent = "Please fill in all fields before comparing.";
    errorEl.classList.remove("hidden");
    return;
  }

  errorEl.classList.add("hidden");
  btn.disabled = true;
  btn.textContent = "Comparing...";

  try {
    const res = await fetch("/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        a: { ...shared, ...scenA },
        b: { ...shared, ...scenB },
      }),
    });

    const data = await res.json();
    if (!data.success) throw new Error(data.error);

    renderResults(data.a, data.b, shared, scenA, scenB);
  } catch (err) {
    errorEl.textContent = "Error: " + err.message;
    errorEl.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    btn.textContent = "Compare Scenarios";
  }
}

// ── Render all result sections ──
function renderResults(valA, valB, shared, scenA, scenB) {
  const section = document.getElementById("resultsSection");
  const higher = valA >= valB ? "a" : "b";
  const lower = higher === "a" ? "b" : "a";
  const diff = Math.abs(valA - valB);
  const diffPct = ((diff / Math.min(valA, valB)) * 100).toFixed(1);
  const negligible = diff < 10;

  renderScoreCards(valA, valB, higher, negligible);
  renderBarChart(valA, valB);
  renderDiff(diff, diffPct, higher, negligible);
  renderInputsDiff(shared, scenA, scenB);
  renderRecommendation(
    valA,
    valB,
    higher,
    diffPct,
    shared,
    scenA,
    scenB,
    negligible,
  );

  section.classList.add("visible");
  section.scrollIntoView({ behavior: "smooth", block: "start" });
}

// ── Score cards ──
function renderScoreCards(valA, valB, higher, negligible) {
  document.getElementById("scoreValueA").textContent = fmt(valA);
  document.getElementById("scoreValueB").textContent = fmt(valB);

  const pctA = (((valA - DATASET_AVG) / DATASET_AVG) * 100).toFixed(1);
  const pctB = (((valB - DATASET_AVG) / DATASET_AVG) * 100).toFixed(1);
  document.getElementById("scoreSubA").textContent =
    (pctA >= 0 ? "+" : "") + pctA + "% vs dataset avg";
  document.getElementById("scoreSubB").textContent =
    (pctB >= 0 ? "+" : "") + pctB + "% vs dataset avg";

  const cardA = document.getElementById("scoreCardA");
  const cardB = document.getElementById("scoreCardB");
  const badgeA = document.getElementById("winnerBadgeA");
  const badgeB = document.getElementById("winnerBadgeB");

  cardA.className = "score-card score-a";
  cardB.className = "score-card score-b";
  badgeA.style.display = "none";
  badgeB.style.display = "none";

  if (!negligible) {
    if (higher === "a") {
      cardA.classList.add("winner-a");
      badgeA.style.display = "block";
    } else {
      cardB.classList.add("winner-b");
      badgeB.style.display = "block";
    }
  }
}

// ── Bar chart (CSS animated) ──
function renderBarChart(valA, valB) {
  const max = Math.max(valA, valB);
  const wA = ((valA / max) * 100).toFixed(1);
  const wB = ((valB / max) * 100).toFixed(1);

  const fillA = document.getElementById("barFillA");
  const fillB = document.getElementById("barFillB");
  const valElA = document.getElementById("barValA");
  const valElB = document.getElementById("barValB");

  // Reset first so transition fires
  fillA.style.width = "0%";
  fillB.style.width = "0%";

  requestAnimationFrame(() => {
    setTimeout(() => {
      fillA.style.width = wA + "%";
      fillB.style.width = wB + "%";
    }, 60);
  });

  valElA.textContent = fmt(valA);
  valElB.textContent = fmt(valB);
  document.getElementById("barLabelA").textContent = "A";
  document.getElementById("barLabelB").textContent = "B";
}

// ── Diff card ──
function renderDiff(diff, diffPct, higher, negligible) {
  const diffValue = document.getElementById("diffValue");
  const diffSub = document.getElementById("diffSub");

  if (negligible) {
    diffValue.textContent = "~₹0";
    diffValue.style.color = "var(--text-dim)";
    diffSub.textContent = "Negligible difference";
  } else {
    diffValue.textContent = fmt(diff);
    diffValue.style.color = "";
    diffSub.textContent =
      diffPct + "% more in Scenario " + higher.toUpperCase();
  }
}

// ── Inputs diff table — only rows where A !== B ──
function renderInputsDiff(shared, scenA, scenB) {
  const LABELS = {
    Outlet_Type: "Outlet Type",
    Outlet_Size: "Outlet Size",
    Outlet_Location_Type: "Location",
    Outlet_Establishment_Year: "Outlet Year",
    Outlet_Identifier: "Outlet ID",
  };

  const rows = Object.entries(LABELS)
    .filter(([key]) => String(scenA[key]) !== String(scenB[key]))
    .map(
      ([key, label]) => `
      <tr>
        <td class="field-name">${label}</td>
        <td class="val-a">${scenA[key]}</td>
        <td class="val-b">${scenB[key]}</td>
      </tr>`,
    )
    .join("");

  const card = document.getElementById("diffInputsCard");

  if (!rows) {
    card.style.display = "none";
    return;
  }

  card.style.display = "block";
  document.getElementById("diffTableBody").innerHTML = rows;
}

// ── Recommendation — built dynamically ──
function renderRecommendation(
  valA,
  valB,
  higher,
  diffPct,
  shared,
  scenA,
  scenB,
  negligible,
) {
  const winnerScen = higher === "a" ? scenA : scenB;
  const winnerLabel = higher === "a" ? "Scenario A" : "Scenario B";
  const winnerVal = higher === "a" ? valA : valB;
  const loserVal = higher === "a" ? valB : valA;
  const el = document.getElementById("recommendationText");

  if (negligible) {
    el.innerHTML = `Both scenarios produce nearly identical predicted sales (<strong>${fmt(valA)}</strong> vs <strong>${fmt(valB)}</strong>). The outlet differences between them — ${getDiffSummary(scenA, scenB)} — have minimal impact on this model's prediction. Consider other business factors such as operating cost or foot traffic when choosing between these outlets.`;
    return;
  }

  const outletDiff =
    scenA.Outlet_Type !== scenB.Outlet_Type
      ? `The largest driver is outlet type — <strong>${winnerScen.Outlet_Type}</strong> significantly outperforms <strong>${(higher === "a" ? scenB : scenA).Outlet_Type}</strong> in this model. `
      : "";

  const locDiff =
    scenA.Outlet_Location_Type !== scenB.Outlet_Location_Type
      ? `Location tier also contributes — <strong>${winnerScen.Outlet_Location_Type}</strong> shows higher predicted performance. `
      : "";

  el.innerHTML = `<strong>${winnerLabel}</strong> is the stronger outlet for this item, with predicted sales of <strong>${fmt(winnerVal)}</strong> compared to <strong>${fmt(loserVal)}</strong> — a difference of <strong>${diffPct}%</strong>. ${outletDiff}${locDiff}Based on this model, stocking <strong>${shared.Item_Type}</strong> at MRP <strong>${fmt(shared.Item_MRP)}</strong> in a <strong>${winnerScen.Outlet_Type}</strong> outlet would yield the better return.`;
}

function getDiffSummary(scenA, scenB) {
  const diffs = [];
  if (scenA.Outlet_Type !== scenB.Outlet_Type) diffs.push("outlet type");
  if (scenA.Outlet_Size !== scenB.Outlet_Size) diffs.push("outlet size");
  if (scenA.Outlet_Location_Type !== scenB.Outlet_Location_Type)
    diffs.push("location");
  if (scenA.Outlet_Establishment_Year !== scenB.Outlet_Establishment_Year)
    diffs.push("outlet year");
  return diffs.join(", ") || "the selected fields";
}
