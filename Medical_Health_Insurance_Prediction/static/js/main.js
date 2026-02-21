const modal = document.getElementById("resultModal");
const modalResult = document.getElementById("modalResult");

document.querySelector(".close-btn").onclick = () => {
  modal.style.display = "none";
};

window.onclick = (e) => {
  if (e.target === modal) {
    modal.style.display = "none";
  }
};

document
  .getElementById("insuranceForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const loading = document.getElementById("loading");
    const submitBtn = document.querySelector("#insuranceForm button");

    loading.style.display = "block";
    submitBtn.disabled = true;
    submitBtn.innerText = "Predicting...";

    const data = {
      age: parseInt(document.getElementById("age").value),
      sex: document.getElementById("sex").value,
      bmi: parseFloat(document.getElementById("bmi").value),
      children: parseInt(document.getElementById("children").value),
      smoker: document.getElementById("smoker").value,
      region: document.getElementById("region").value,
    };

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      loading.style.display = "none";
      submitBtn.disabled = false;
      submitBtn.innerText = "Predict Insurance Cost";

      if (result.error) {
        modalResult.innerHTML = `<h2>❌ Error</h2><p>${result.error}</p>`;
        modal.style.display = "flex";
        return;
      }

      const risk = result.risk_level;
      const charges = result.predicted_charges.toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });

      let riskEmoji = "";
      let riskClass = "";

      if (risk === "Very High") {
        riskEmoji = "🚨";
        riskClass = "risk-very-high";
      } else if (risk === "High") {
        riskEmoji = "⚠️";
        riskClass = "risk-high";
      } else if (risk === "Medium") {
        riskEmoji = "🟠";
        riskClass = "risk-medium";
      } else {
        riskEmoji = "✅";
        riskClass = "risk-low";
      }

      modalResult.innerHTML = `
      <h2 style="color:#1E3A8A; font-size:1.1rem; font-weight:700;">Estimated Insurance Cost</h2>
      <div class="result-amount">$${charges}</div>
      <span class="result-risk ${riskClass}">${riskEmoji} ${risk} Risk</span>
      <p style="margin-top:16px; font-size:0.85rem; color:#64748B;">
        Based on XGBoost model · R² = 0.864
      </p>
    `;

      modal.style.display = "flex";
    } catch (error) {
      loading.style.display = "none";
      submitBtn.disabled = false;
      submitBtn.innerText = "Predict Insurance Cost";

      modalResult.innerHTML = `<h2>❌ Error</h2><p>${error.message}</p>`;
      modal.style.display = "flex";
    }
  });

