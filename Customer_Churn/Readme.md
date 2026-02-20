# Customer Churn Prediction Using Machine Learning

## Overview

This project predicts telecom customer churn using a full end-to-end machine learning pipeline — covering data preprocessing, class imbalance correction with SMOTE, cross-validation, hyperparameter tuning, and deployment as a live Flask web application backed by a persistent cloud database.

🔗 **Live Demo:** [Customer Churn Prediction](https://customer-churn-prediction-x9i2.onrender.com/)

---

## Dataset

- **Source:** Telecom customer dataset
- **Target variable:** `Churn` (Yes / No)
- **Class imbalance:** ~73% No Churn, ~27% Churn — corrected using SMOTE

### Features

| Feature | Type | Description |
|---|---|---|
| `gender` | Categorical | Male / Female |
| `SeniorCitizen` | Binary | 0 or 1 |
| `Partner` | Categorical | Yes / No |
| `Dependents` | Categorical | Yes / No |
| `tenure` | Numerical | Months with company |
| `PhoneService` | Categorical | Yes / No |
| `MultipleLines` | Categorical | Yes / No / No phone service |
| `InternetService` | Categorical | DSL / Fiber optic / No |
| `OnlineSecurity` | Categorical | Yes / No / No internet service |
| `OnlineBackup` | Categorical | Yes / No / No internet service |
| `DeviceProtection` | Categorical | Yes / No / No internet service |
| `TechSupport` | Categorical | Yes / No / No internet service |
| `StreamingTV` | Categorical | Yes / No / No internet service |
| `StreamingMovies` | Categorical | Yes / No / No internet service |
| `Contract` | Categorical | Month-to-month / One year / Two year |
| `PaperlessBilling` | Categorical | Yes / No |
| `PaymentMethod` | Categorical | Electronic check / Mailed check / etc. |
| `MonthlyCharges` | Numerical | Monthly bill amount |
| `TotalCharges` | Numerical | Total amount charged |

---

## Project Workflow

1. Data cleaning and preprocessing
2. Label encoding of all categorical variables
3. Train–test split (stratified)
4. Baseline evaluation using Dummy Classifier
5. Class imbalance correction using **SMOTE**
6. Model training — Decision Tree, Random Forest, XGBoost
7. Cross-validation on SMOTE-balanced data
8. Hyperparameter tuning using **RandomizedSearchCV**
9. Final model evaluation on real (non-SMOTE) test data
10. Model and encoder serialization with Pickle
11. Deployment as Flask web app with Supabase persistence

---

## Baseline Model

A Dummy Classifier predicting only "No Churn" was used to establish the performance floor.

| Metric | Value |
|---|---|
| Accuracy | 73.53% |
| Churn Recall | 0% |
| Churn F1-score | 0.00 |

High accuracy is misleading here — the model completely fails to detect any churn due to class imbalance. This is why recall is the primary business metric.

---

## Cross-Validation Accuracy (SMOTE Data)

| Model | CV Accuracy |
|---|---|
| Decision Tree | 78.09% |
| Random Forest | 83.79% |
| XGBoost | 83.12% |

---

## Default Model Performance (Real Test Data)

| Model | Accuracy | Churn Recall | Churn F1 |
|---|---|---|---|
| Random Forest | 77.7% | 0.58 | 0.58 |
| XGBoost | **78.2%** | **0.61** | **0.60** |

**Best default model: XGBoost**

---

## Hyperparameter Tuning

`RandomizedSearchCV` was used to tune both top models.

### Random Forest — Best Parameters

```json
{
  "n_estimators": 100,
  "min_samples_split": 5,
  "min_samples_leaf": 1,
  "max_features": "log2",
  "max_depth": null,
  "class_weight": "balanced"
}
```

| Metric | Value |
|---|---|
| Accuracy | 77.9% |
| Churn Recall | 0.61 |
| Churn F1 | 0.59 |

Marginal improvement over default Random Forest.

---

### XGBoost — Best Parameters

```json
{
  "subsample": 0.6,
  "n_estimators": 200,
  "max_depth": 10,
  "learning_rate": 0.05,
  "gamma": 0,
  "colsample_bytree": 1.0
}
```

| Metric | Value |
|---|---|
| Accuracy | 78.1% |
| Churn Recall | 0.57 |
| Churn F1 | 0.58 |

Tuning slightly degraded XGBoost — the default configuration generalized better on this dataset.

---

## Final Model Comparison

| Model | Accuracy | Churn Recall | Churn F1 | Notes |
|---|---|---|---|---|
| Baseline (Dummy) | 73.5% | 0% | 0.00 | Predicts all non-churn |
| Decision Tree | 78.1% | ~0.57 | ~0.57 | Weakest ensemble |
| RF (Default) | 77.7% | 0.58 | 0.58 | Good baseline |
| RF (Tuned) | 77.9% | 0.61 | 0.59 | Slight improvement |
| XGBoost (Tuned) | 78.1% | 0.57 | 0.58 | Slight drop vs default |
| **XGBoost (Default)** | **78.2%** | **0.61** | **0.60** | **✅ Best overall** |

**Final model: Default XGBoost**
- +6–7% accuracy improvement over baseline
- Churn recall improved from 0% → 61%

---

## Deployment

The model is deployed as a **Flask web application** with three pages:

### Predict
- Input form for all 19 customer features
- Returns churn probability, prediction (Churn / No Churn), and risk level (Low / Medium / High / Critical)
- Every prediction is automatically saved to the database

### Dashboard
- Today's summary: total predictions, high risk customers, average churn risk
- Risk distribution donut chart (Low / Medium / High / Critical)

### History
- Last 20 predictions with probability, risk level, prediction, and timestamp

### Tech Stack

| Layer | Technology |
|---|---|
| Model | XGBoost (Pickle serialized) |
| Backend | Flask + Gunicorn |
| Database | Supabase (PostgreSQL) |
| Hosting | Render |

### Supabase Integration

Predictions are persisted in a **Supabase PostgreSQL** database, replacing ephemeral SQLite storage. SQLite on Render resets on every redeploy since Render's filesystem is ephemeral — Supabase persists permanently regardless of restarts or redeployments.

The `churn_predictions` table stores all 19 input features alongside the prediction result, enabling future analytics like churn rate by contract type, internet service, or tenure band.

Credentials are stored securely in **Render Environment Variables** and never committed to the repository.

---

## Project Structure

```
customer_churn/
├── app.py                      # Flask application
├── customer_churn_model.pkl    # Serialized XGBoost model
├── encoders.pkl                # Label encoders for categorical features
├── requirements.txt            # Python dependencies
├── static/
│   ├── css/
│   └── js/main.js
└── templates/
    ├── index.html
    ├── dashboard.html
    └── history.html
```

---

## Requirements

```
flask
gunicorn
pandas
numpy
scikit-learn
xgboost
supabase
```

Install with:

```bash
pip install flask gunicorn pandas numpy scikit-learn xgboost supabase
```

---

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/customer-churn.git
cd customer_churn

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_anon_key"

# 4. Run the app
python app.py
```

---

## Key Takeaways

- Baseline accuracy is misleading without recall and F1 — always evaluate on the minority class
- SMOTE significantly improves minority class detection during training
- Default XGBoost outperformed all tuned configurations on this dataset — tuning does not always help
- Churn recall (the most business-critical metric) improved from 0% → 61%
- SQLite is unsuitable for cloud deployments with ephemeral filesystems — Supabase provides reliable persistent storage
- The full pipeline is production-ready with saved models, encoders, and a live database backend
