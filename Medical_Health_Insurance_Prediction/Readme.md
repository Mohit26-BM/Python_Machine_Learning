# InsurePredict: Predict Your Medical Insurance Cost

## Overview

This project predicts **medical insurance charges** using machine learning regression models. The objective is to estimate insurance costs based on demographic and health-related attributes such as age, BMI, smoking status, and region.

The full pipeline covers exploratory data analysis (EDA), data preprocessing, model training, hyperparameter tuning, performance comparison, and deployment as a live Flask web application backed by a persistent cloud database.

🔗 **Live Demo:** [Medical Insurance Cost Predictor](https://insurance-predictor1.onrender.com)

---

## Dataset Description

- **Dataset name:** `insurance.csv`
- **Total records:** 1,338
- **Target variable:** `charges` (medical insurance cost in USD)

### Features

| Feature | Type | Description |
|---|---|---|
| `age` | Numerical | Age of the individual |
| `sex` | Categorical | Male / Female |
| `bmi` | Numerical | Body Mass Index |
| `children` | Numerical | Number of dependents |
| `smoker` | Categorical | Yes / No |
| `region` | Categorical | Southwest / Southeast / Northwest / Northeast |

### Data Quality Summary

- No missing values
- 1 duplicated row (removed)
- Balanced gender distribution
- Majority of customers are non-smokers
- Charges show high variance and positive skew — driven heavily by smoking status

---

## Exploratory Data Analysis (EDA)

Key observations:

- Smokers incur significantly higher insurance charges — the single most influential feature
- BMI and age show a positive correlation with charges
- Region has a smaller but noticeable influence on cost
- Insurance charges are highly right-skewed due to high-cost outliers (mostly smokers with high BMI)

---

## Data Preprocessing

### Encoding

Categorical variables converted to numerical using manual label encoding:

| Feature | Encoding |
|---|---|
| `sex` | male → 0, female → 1 |
| `smoker` | yes → 1, no → 0 |
| `region` | southeast → 0, southwest → 1, northeast → 2, northwest → 3 |

### Train–Test Split

- Training set: **80%**
- Test set: **20%**
- `random_state=2` fixed for reproducibility

---

## Models Trained

Four regression models were trained and evaluated:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- XGBoost Regressor

---

## Model Evaluation Metrics

Models were evaluated using RMSE, MAE, and R² Score:

- **RMSE** — average prediction error, penalizes large mistakes more heavily
- **MAE** — average absolute difference between predicted and actual charges
- **R²** — proportion of variance in charges explained by the model

---

## Baseline Model Performance

Initial results before hyperparameter tuning:

| Model | RMSE (USD) | MAE (USD) | R² Score |
|---|---:|---:|---:|
| Linear Regression | 6,191.69 | 4,267.21 | 0.7447 |
| Decision Tree | 6,870.84 | 3,367.69 | 0.6857 |
| Random Forest | 4,947.95 | 2,795.39 | 0.8370 |
| XGBoost | 5,279.09 | 3,105.36 | 0.8144 |

Random Forest leads before tuning. XGBoost trails slightly with default parameters.

---

## Hyperparameter Tuning

`RandomizedSearchCV` with 5-fold cross-validation and 30 iterations was used to tune both top models.

### XGBoost — Best Parameters

```json
{
  "subsample": 0.6,
  "n_estimators": 100,
  "max_depth": 5,
  "learning_rate": 0.05,
  "gamma": 0,
  "colsample_bytree": 1.0
}
```

### Random Forest — Best Parameters

```json
{
  "n_estimators": 200,
  "min_samples_split": 5,
  "min_samples_leaf": 2,
  "max_features": "sqrt",
  "max_depth": 10
}
```

---

## Final Model Performance (Post-Tuning)

| Model | R² Score | Notes |
|---|---|---|
| Linear Regression | 0.7447 | Baseline — no tuning |
| Decision Tree | 0.6857 | Overfits — dropped |
| Random Forest (default) | 0.8370 | Strong baseline |
| Random Forest (tuned) | 0.8489 | Marginal improvement |
| XGBoost (default) | 0.8144 | Below Random Forest |
| **XGBoost (tuned)** | **0.8639** | ✅ Best overall |

**Final model: Tuned XGBoost** — R² improved from 0.8144 → 0.8639 (+6.1%), overtaking all other models including tuned Random Forest.

---

## Prediction Accuracy Within Error Thresholds

Number of test predictions within a given absolute dollar error:

| Error Threshold | Linear Regression | Decision Tree | Random Forest | XGBoost (tuned) |
|---|---:|---:|---:|---:|
| ≤ $500 | 29 | 135 | 74 | 63 |
| ≤ $1,000 | 55 | 177 | 125 | 118 |
| ≤ $2,000 | 110 | 205 | 169 | **181** |
| ≤ $3,000 | 155 | 209 | 198 | **216** |
| ≤ $5,000 | 186 | 211 | 224 | **243** |

XGBoost tuned wins at ≥$2,000 thresholds and the gap grows at higher values — 243 vs 224 at ≤$5,000. For insurance cost estimation where charges range from $1,000 to $60,000+, accuracy at larger thresholds is what matters most.

---

## Example Prediction

**Input:**
```
Age: 31, Sex: Female, BMI: 25.74, Children: 0, Smoker: No, Region: Southeast
```

**Predicted Charges:**

| Model | Prediction |
|---|---|
| Linear Regression | ~$27,688 |
| Decision Tree | ~$19,720 |
| Random Forest (default) | ~$20,164 |
| XGBoost (default) | ~$18,876 |
| XGBoost (tuned) | ~$20,462 |
| Random Forest (tuned) | ~$20,993 |

Linear Regression significantly overestimates due to its inability to capture non-linear relationships. The four tree-based models cluster tightly between $18,876–$20,993, with XGBoost tuned ($20,462) being the most reliable.

---

## Deployment

The tuned XGBoost model is deployed as a **Flask web application** with three pages:

### Predict
- Input form for all 6 patient features
- Returns predicted insurance cost and risk level (Low / Medium / High / Very High)
- Every prediction is automatically saved to the database

### Dashboard
- Today's summary: total predictions, average cost, high cost customers, smoker count
- 4 visualizations: charges over time, risk distribution donut, predictions by age group, smoker vs non-smoker avg cost

### History
- Last 20 predictions with all input features, predicted cost, risk level, and timestamp

### Tech Stack

| Layer | Technology |
|---|---|
| Model | XGBoost (Pickle serialized) |
| Backend | Flask + Gunicorn |
| Database | Supabase (PostgreSQL) |
| Hosting | Render |

### Supabase Integration

Predictions are persisted in a **Supabase PostgreSQL** database replacing ephemeral SQLite storage. SQLite on Render resets on every redeploy since Render's filesystem is ephemeral — Supabase persists permanently regardless of restarts or redeployments.

The `insurance_predictions` table stores all 6 input features alongside the prediction result and risk level.

Credentials are stored securely in **Render Environment Variables** and never committed to the repository.

### Risk Classification

| Risk Level | Predicted Charge Range |
|---|---|
| Low | Under $12,000 |
| Medium | $12,000 – $25,000 |
| High | $25,000 – $40,000 |
| Very High | Above $40,000 |

---

## Project Structure

```
Medical_Health_Insurance_Prediction/
├── app.py                      # Flask application
├── insurance_model.pkl         # Serialized tuned XGBoost model
├── encoders.pkl                # Label encoders (if used)
├── requirements.txt            # Python dependencies
├── Medical_Insurance.ipynb     # Training notebook
├── static/
│   ├── css/
│   │   ├── style.css           # Main app styles
│   │   ├── dashboard.css       # Dashboard styles
│   │   └── history.css         # History styles
│   └── js/
│       └── main.js             # Prediction form logic
└── templates/
    ├── index.html              # Predict page
    ├── dashboard.html          # Dashboard page
    └── history.html            # History page
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
git clone https://github.com/yourusername/Python_Machine_Learning.git
cd Python_Machine_Learning/Medical_Health_Insurance_Prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_anon_key"

# 4. Run the app
python app.py
```

Or using a `.env` file locally:
```bash
pip install python-dotenv
# create .env with SUPABASE_URL and SUPABASE_KEY
python app.py
```

---

## Key Takeaways

- Tuned XGBoost outperformed all models including tuned Random Forest — R² = 0.864
- Smoking status is by far the most influential feature for insurance cost
- Decision Tree makes precise predictions on easy cases but fails badly on hard ones — good ≤$500 count but worst RMSE
- Hyperparameter tuning improved XGBoost R² by +6.1%, overtaking Random Forest which led before tuning
- SQLite is unsuitable for cloud deployments with ephemeral filesystems — Supabase provides reliable persistent storage

---

## Conclusion

This project demonstrates a complete end-to-end machine learning pipeline for insurance cost prediction. After tuning, XGBoost delivered the best performance at R² = 0.864, accurately predicting insurance charges for 243 out of 268 test cases within $5,000 of the actual value. The model is deployed as a production Flask application with persistent cloud storage and a live analytics dashboard.
