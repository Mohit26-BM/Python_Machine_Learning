const modal = document.getElementById("resultModal");
const modalClose = document.querySelector(".modal-close");

if (modal && modalClose) {
  modalClose.onclick = () => (modal.style.display = "none");
  window.onclick = (e) => {
    if (e.target === modal) modal.style.display = "none";
  };
}

const loanForm = document.getElementById("loanForm");
if (loanForm) {
  loanForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const errorMsg = document.getElementById("errorMsg");
  const loading = document.getElementById("loading");
  const submitBtn = document.querySelector(".btn-submit");

  errorMsg.style.display = "none";

  const data = {
    gender: document.getElementById("gender").value,
    married: document.getElementById("married").value,
    dependents: document.getElementById("dependents").value,
    education: document.getElementById("education").value,
    self_employed: document.getElementById("self_employed").value,
    applicant_income: document.getElementById("applicant_income").value,
    coapplicant_income: document.getElementById("coapplicant_income").value,
    loan_amount: document.getElementById("loan_amount").value,
    loan_term: document.getElementById("loan_term").value,
    credit_history: document.getElementById("credit_history").value,
    property_area: document.getElementById("property_area").value,
  };

  // Client-side validation
  for (const [key, val] of Object.entries(data)) {
    if (!val) {
      errorMsg.textContent = "Please fill in all fields before submitting.";
      errorMsg.style.display = "block";
      return;
    }
  }

  if (parseFloat(data.applicant_income) <= 0) {
    errorMsg.textContent = "Applicant income must be greater than 0.";
    errorMsg.style.display = "block";
    return;
  }

  if (parseFloat(data.loan_amount) <= 0) {
    errorMsg.textContent = "Loan amount must be greater than 0.";
    errorMsg.style.display = "block";
    return;
  }

  loading.style.display = "block";
  submitBtn.disabled = true;
  submitBtn.textContent = "Analysing...";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    loading.style.display = "none";
    submitBtn.disabled = false;
    submitBtn.textContent = "Check Loan Eligibility →";

    if (result.error) {
      errorMsg.textContent = result.error;
      errorMsg.style.display = "block";
      return;
    }

    const approved = result.prediction === "Approved";
    const confidence = result.confidence;

    modalContent.innerHTML = `
      <div class="result-icon">
        ${
          approved
            ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M8 12.5l2.5 2.5L16 9.5"></path></svg>`
            : `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M9 9l6 6"></path><path d="M15 9l-6 6"></path></svg>`
        }
      </div>
      <div class="result-title ${approved ? "result-approved" : "result-rejected"}">
        ${result.prediction}
      </div>
      <div class="result-confidence">
        Model confidence: <strong>${confidence}%</strong>
      </div>
      <div class="confidence-bar-wrapper">
        <div class="confidence-bar ${approved ? "bar-approved" : "bar-rejected"}"
             style="width: 0%"
             id="confBar">
        </div>
      </div>
      <p style="font-size:0.85rem; color:#64748b; line-height:1.6;">
        ${
          approved
            ? "Based on your profile, your loan application is likely to be <strong>approved</strong>. A bank officer will make the final decision."
            : "Based on your profile, your loan application may be <strong>rejected</strong>. Consider improving your credit history or reducing the loan amount."
        }
      </p>
    `;

    modal.style.display = "flex";

    // Animate confidence bar
    setTimeout(() => {
      document.getElementById("confBar").style.width = confidence + "%";
    }, 100);
  } catch (error) {
    loading.style.display = "none";
    submitBtn.disabled = false;
    submitBtn.textContent = "Check Loan Eligibility →";
    errorMsg.textContent = "Something went wrong. Please try again.";
    errorMsg.style.display = "block";
  }
  });
}

function animateCounter(el, target, duration = 1500, suffix = "") {
  const start = performance.now();
  const isDecimal = target % 1 !== 0;

  const tick = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = eased * target;
    el.textContent =
      (isDecimal ? current.toFixed(2) : Math.floor(current)) + suffix;
    if (progress < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

// Trigger when stat cards scroll into view
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);

      const el = entry.target.querySelector(".stat-value");
      const raw = el.dataset.target;
      const suffix = el.dataset.suffix || "";
      animateCounter(el, parseFloat(raw), 1500, suffix);
    });
  },
  { threshold: 0.3 },
);

document
  .querySelectorAll(".stat-card")
  .forEach((card) => observer.observe(card));
