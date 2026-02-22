# Loan Approval Prediction Using Machine Learning

## Overview

This project predicts **loan approval status** using machine learning classification models. Financial institutions can use such models to assist in automating eligibility decisions based on applicant demographics, income, credit history, and property information.

The full pipeline covers exploratory data analysis, data cleaning, feature engineering, model training with class balancing, multi-model comparison, and deployment as a live Flask web application backed by a persistent cloud database.

🔗 **Live Demo:** [LoanIQ — Loan Approval Predictor](#) *(add your Render URL here)*

---

## Dataset Description

- **Dataset name:** `loan.csv`
- **Total records (after cleaning):** 480
- **Target variable:** `Loan_Status`
  - 1 → Approved
  - 0 → Rejected

### Features

| Feature | Type | Description |
|---|---|---|
| `Gender` | Categorical | Male / Female |
| `Married` | Categorical | Yes / No |
| `Dependents` | Numerical | Number of dependents (0, 1, 2, 3+) |
| `Education` | Categorical | Graduate / Not Graduate |
| `Self_Employed` | Categorical | Yes / No |
| `ApplicantIncome` | Numerical | Primary applicant income |
| `CoapplicantIncome` | Numerical | Co-applicant income |
| `LoanAmount` | Numerical | Loan amount in thousands |
| `Loan_Amount_Term` | Numerical | Repayment term in months |
| `Credit_History` | Binary | 1 = Good, 0 = Bad |
| `Property_Area` | Categorical | Rural / Semiurban / Urban |

---

## Exploratory Data Analysis (EDA)

Key observations:

- Credit history is the single strongest indicator of loan approval
- Majority of approved loans belong to applicants with credit history = 1
- Loan approvals are more frequent for graduates and urban/semiurban properties
- Dataset is moderately imbalanced — 332 approved vs 148 rejected
- Missing values present in Gender, Married, Dependents, Self_Employed, LoanAmount, Loan_Amount_Term, Credit_History

---

## Data Cleaning and Preprocessing

### Handling Missing Values

Rows with missing values were dropped for simplicity — 614 records reduced to 480 after cleaning.

### Label Encoding

| Feature | Encoding |
|---|---|
| `Loan_Status` | Y → 1, N → 0 |
| `Gender` | Male → 1, Female → 0 |
| `Married` | Yes → 1, No → 0 |
| `Education` | Graduate → 1, Not Graduate → 0 |
| `Self_Employed` | Yes → 1, No → 0 |
| `Property_Area` | Rural → 0, Semiurban → 1, Urban → 2 |

### Feature Engineering

- `Dependents`: `3+` converted to `4` for numerical compatibility
- `Loan_ID` dropped — acts as identifier with no predictive value

---

## Train-Test Split

- Training set: **90%** (432 records)
- Test set: **10%** (48 records)
- Stratified split to preserve class distribution
- `random_state=2` fixed for reproducibility

---

## Class Imbalance Handling

All models trained with `class_weight='balanced'` to prevent bias toward the majority class (Approved). This improves recall for rejected loans — the more costly error in a real lending scenario.

---

## Models Trained

Four classifiers were compared:

- Logistic Regression
- Support Vector Machine (Linear Kernel)
- Decision Tree
- Random Forest

---

## Model Performance Comparison

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| **Logistic Regression** | **85.42%** | **0.8522** | **0.8542** | **0.8527** |
| Random Forest | 83.33% | 0.8317 | 0.8333 | 0.8253 |
| SVC | 81.25% | 0.8073 | 0.8125 | 0.8062 |
| Decision Tree | 77.08% | 0.7615 | 0.7708 | 0.7560 |

**Logistic Regression selected as final model** — highest accuracy, precision, recall, and F1 score across all metrics.

---

## Final Model — Logistic Regression

### Confusion Matrix

|  | Predicted Rejected | Predicted Approved |
|---|---:|---:|
| **Actual Rejected** | 11 | 4 |
| **Actual Approved** | 3 | 30 |

### Classification Report

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Rejected (0) | 0.79 | 0.73 | 0.76 | 15 |
| Approved (1) | 0.88 | 0.91 | 0.90 | 33 |
| **Weighted Avg** | **0.85** | **0.85** | **0.85** | **48** |

### Key Observations

- Model correctly identifies 91% of approved loans (high recall for class 1)
- Correctly identifies 73% of rejected loans — improved significantly over SVM baseline due to `class_weight='balanced'`
- Better balanced performance than SVM or Random Forest for the rejection class

---

## Example Prediction

**Input:**
```
Gender: Female, Married: No, Dependents: 0
Education: Graduate, Self Employed: No
Applicant Income: 3510, Co-applicant Income: 0
Loan Amount: 76k, Loan Term: 360 months
Credit History: 0 (Bad), Property Area: Urban
```

**Predicted Output:** Rejected (Credit history = 0 is the dominant factor)

---

## Deployment

The Logistic Regression model is deployed as a **Flask web application** with four pages:

### Home
- Hero section with model accuracy and stats
- How it works — feature explanation
- Model comparison table with full metrics
- Confusion matrix visualization
- CTA button to start prediction

### Predict
- Full input form with all 11 features
- Instant Approved / Rejected result
- Confidence score via `predict_proba()`
- Animated confidence bar in result modal
- Every prediction saved to database

### Dashboard
- All-time KPI cards: total predictions, approvals, rejections, avg confidence, avg income
- 4 ApexCharts visualizations: approval ratio donut, property area bar, credit history vs outcome grouped bar, education distribution donut

### History
- Last 30 predictions with all input features
- Approval/rejection badges, credit history badges
- Confidence score and timestamp per record

### Tech Stack

| Layer | Technology |
|---|---|
| Model | Logistic Regression (joblib serialized) |
| Backend | Flask + Gunicorn |
| Database | Supabase (PostgreSQL) |
| Charts | ApexCharts |
| Hosting | Render |

### Supabase Integration

Predictions are persisted in a **Supabase PostgreSQL** database. All 11 input features, prediction result, and confidence score are stored per record. Credentials stored in Render Environment Variables and never committed to the repository.

---

## Project Structure

```
Loan_Status_Prediction/
├── app.py                  # Flask application — all routes
├── loan_model.pkl          # Serialized Logistic Regression model
├── model_columns.pkl       # Feature column order
├── requirements.txt        # Python dependencies
├── Loan_Status.ipynb       # Training notebook
├── static/
│   ├── css/
│   │   └── style.css       # All page styles
│   └── js/
│       └── main.js         # Prediction form and modal logic
└── templates/
    ├── index.html          # Home / landing page
    ├── predict.html        # Prediction form
    ├── dashboard.html      # Analytics dashboard
    └── history.html        # Prediction history
```

---

## Requirements

```
flask
gunicorn
pandas
numpy
scikit-learn
joblib
supabase
```

Install with:

```bash
pip install flask gunicorn pandas numpy scikit-learn joblib supabase
```

---

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Python_Machine_Learning.git
cd Python_Machine_Learning/Loan_Status_Prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
# Create a .env file:
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_anon_key
pip install python-dotenv

# 4. Run the app
python app.py
```

---

## Key Takeaways

- Logistic Regression outperformed SVM, Random Forest, and Decision Tree on all metrics
- `class_weight='balanced'` significantly improved rejection recall — critical for real-world loan decisions
- Credit history is the most influential feature — bad credit history almost always leads to rejection
- Row deletion for missing values reduced dataset from 614 → 480 — imputation could recover these records in future work
- Confidence scores via `predict_proba()` add transparency to predictions — users see how certain the model is

---

## Conclusion

This project demonstrates a complete end-to-end classification pipeline for loan approval prediction. Logistic Regression with balanced class weighting delivered the best performance at 85.42% accuracy, correctly identifying 91% of approvals and 73% of rejections. The model is deployed as a production Flask application with persistent cloud storage, live analytics dashboard, and prediction history.
