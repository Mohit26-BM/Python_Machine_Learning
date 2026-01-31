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

document.getElementById("churnForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const loading = document.querySelector(".loading");
  const submitBtn = document.querySelector("#churnForm button");

  loading.style.display = "block";
  submitBtn.disabled = true;
  submitBtn.innerText = "Predicting...";

  const data = {
    gender: document.getElementById("gender").value,
    SeniorCitizen: parseInt(document.getElementById("SeniorCitizen").value),
    Partner: document.getElementById("Partner").value,
    Dependents: document.getElementById("Dependents").value,
    tenure: parseInt(document.getElementById("tenure").value),
    PhoneService: document.getElementById("PhoneService").value,
    MultipleLines: document.getElementById("MultipleLines").value,
    InternetService: document.getElementById("InternetService").value,
    OnlineSecurity: document.getElementById("OnlineSecurity").value,
    OnlineBackup: document.getElementById("OnlineBackup").value,
    DeviceProtection: document.getElementById("DeviceProtection").value,
    TechSupport: document.getElementById("TechSupport").value,
    StreamingTV: document.getElementById("StreamingTV").value,
    StreamingMovies: document.getElementById("StreamingMovies").value,
    Contract: document.getElementById("Contract").value,
    PaperlessBilling: document.getElementById("PaperlessBilling").value,
    PaymentMethod: document.getElementById("PaymentMethod").value,
    MonthlyCharges: parseFloat(document.getElementById("MonthlyCharges").value),
    TotalCharges: parseFloat(document.getElementById("TotalCharges").value),
  };

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const prediction = await response.json();

    loading.style.display = "none";
    submitBtn.disabled = false;
    submitBtn.innerText = "Predict Churn";

    const prob = prediction.churn_probability;

    let riskLabel = "";
    let riskEmoji = "";

    if (prob >= 80) {
      riskLabel = "Critical Churn Risk";
      riskEmoji = "🚨";
    } else if (prob >= 60) {
      riskLabel = "High Churn Risk";
      riskEmoji = "⚠️";
    } else if (prob >= 40) {
      riskLabel = "Medium Churn Risk";
      riskEmoji = "🟠";
    } else {
      riskLabel = "Low Churn Risk";
      riskEmoji = "✅";
    }
    modalResult.innerHTML = `
  <h2>${riskEmoji} ${riskLabel}</h2>

  <p style="margin-top: 10px;">
    Churn Probability: <strong>${prob}%</strong>
  </p>

  <p style="margin-top: 8px; font-size: 14px; color: #555;">
    Model Decision: <strong>${prediction.prediction}</strong>
  </p>
`;

    modal.style.display = "flex";
  } catch (error) {
    loading.style.display = "none";
    submitBtn.disabled = false;
    submitBtn.innerText = "Predict Churn";

    modalResult.innerHTML = `
      <h2>❌ Error</h2>
      <p>${error.message}</p>
    `;
    modal.style.display = "flex";
  }
});
