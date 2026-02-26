async function submitPrediction() {
  const btn = document.getElementById("predictBtn");
  const btnText = document.getElementById("btnText");
  const btnLoader = document.getElementById("btnLoader");
  const errorMsg = document.getElementById("errorMsg");
  const resultBox = document.getElementById("resultBox");
  const resultValue = document.getElementById("resultValue");
  const resultNote = document.getElementById("resultNote");

  // Collect and cast values properly
  const fields = {
    Item_Weight: parseFloat(document.getElementById("Item_Weight").value),
    Item_Fat_Content: document.getElementById("Item_Fat_Content").value,
    Item_Visibility: parseFloat(
      document.getElementById("Item_Visibility").value,
    ),
    Item_Type: document.getElementById("Item_Type").value,
    Item_MRP: parseFloat(document.getElementById("Item_MRP").value),
    Outlet_Establishment_Year: parseInt(
      document.getElementById("Outlet_Establishment_Year").value,
    ),
    Outlet_Size: document.getElementById("Outlet_Size").value,
    Outlet_Location_Type: document.getElementById("Outlet_Location_Type").value,
    Outlet_Type: document.getElementById("Outlet_Type").value,
    Outlet_Identifier: document.getElementById("Outlet_Identifier").value,
  };

  // Validate — catch empty strings and NaN numerics
  const invalid = Object.entries(fields).filter(
    ([k, v]) =>
      v === "" ||
      v === null ||
      v === undefined ||
      (typeof v === "number" && isNaN(v)),
  );

  if (invalid.length > 0) {
    errorMsg.textContent = "Please fill in all fields before predicting.";
    errorMsg.classList.remove("hidden");
    return;
  }

  errorMsg.classList.add("hidden");
  btn.disabled = true;
  btnText.classList.add("hidden");
  btnLoader.classList.remove("hidden");
  resultBox.classList.add("updating");
  resultBox.classList.remove("has-result");

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(fields),
    });

    const data = await response.json();

    if (data.success) {
      const val = data.prediction;
      await new Promise((r) => setTimeout(r, 180));

      resultValue.textContent =
        "\u20B9" + val.toLocaleString("en-IN", { maximumFractionDigits: 2 });
      resultBox.classList.remove("updating");
      resultBox.classList.add("has-result");
      resultValue.classList.add("flash");
      setTimeout(() => resultValue.classList.remove("flash"), 700);

      const datasetAvg = 2181;
      const diff = (((val - datasetAvg) / datasetAvg) * 100).toFixed(1);
      const direction = parseFloat(diff) >= 0 ? "above" : "below";
      resultNote.textContent =
        Math.abs(diff) + "% " + direction + " dataset average";
    } else {
      throw new Error(data.error || "Prediction failed");
    }
  } catch (err) {
    resultBox.classList.remove("updating");
    errorMsg.textContent = "Error: " + err.message;
    errorMsg.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    btnText.classList.remove("hidden");
    btnLoader.classList.add("hidden");
  }
}