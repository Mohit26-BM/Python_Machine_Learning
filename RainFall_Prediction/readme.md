# Rainfall Prediction System

A machine learning web application that predicts the likelihood of rainfall from atmospheric measurements, built with Flask and deployed on Render.


## Live Demo
[RainCast Rainfall Prediction](https://raincast-rainfall-predictor.onrender.com)

---

## System Overview

The system implements:

* **Decision Tree**
* **Random Forest**
* **XGBoost**

Class imbalance is handled using class weighting. Hyperparameter tuning is performed using GridSearchCV with 5-fold cross-validation.

---

## Application Pages

| Page | Route | Description |
| ---- | ----- | ----------- |
| Overview | `/` | Model metrics, dataset summary, feature influence guide |
| Predict | `/predict` | Form-based single prediction |
| Result | `/result` | Prediction outcome with probability ring |
| What-If Simulator | `/whatif` | Live slider-based interactive prediction |

---

## Dataset Overview

The dataset contains **366 daily weather observations**.

### Features Used

| Feature Name  | Description                             |
| ------------- | --------------------------------------- |
| pressure      | Atmospheric pressure                    |
| dewpoint      | Dew point temperature                   |
| humidity      | Relative humidity (%)                   |
| cloud         | Cloud coverage                          |
| sunshine      | Sunshine duration                       |
| winddirection | Wind direction (degrees)                |
| windspeed     | Wind speed                              |
| rainfall      | Target variable (1 = Rain, 0 = No Rain) |

---

## Data Preprocessing

### Feature Selection

Highly correlated temperature variables (`maxtemp`, `temparature`, `mintemp`) were removed after correlation analysis.

`dewpoint` was retained due to stronger correlation with rainfall and physical relevance.

### Train-Test Split

* 80% Training
* 20% Testing
* Stratified split used to preserve class distribution

### Class Imbalance Handling

* `class_weight="balanced"` for Decision Tree and Random Forest
* `scale_pos_weight` for XGBoost

This prevents data loss and avoids leakage.

---

## Data Distribution After Stratified Split

| Dataset  | Rain (1) | No Rain (0) | Total |
| -------- | -------- | ----------- | ----- |
| Training | 199      | 93          | 292   |
| Test     | 50       | 24          | 74    |

---

## Models Implemented

1. Decision Tree
2. Random Forest
3. XGBoost

Primary evaluation metric: **F1 Score**

---

## Cross-Validation Performance (5-Fold)

| Model         | Mean F1 Score | Mean Accuracy |
| ------------- | ------------- | ------------- |
| Decision Tree | 0.7471        | 0.6611        |
| Random Forest | 0.8458        | 0.7840        |
| XGBoost       | 0.8064        | 0.7430        |

---

## Test Set Performance

### Decision Tree

| Metric    | Class 0 (No Rain) | Class 1 (Rain) |
| --------- | ----------------- | -------------- |
| Precision | 0.57              | 0.78           |
| Recall    | 0.54              | 0.80           |
| F1        | 0.55              | 0.79           |

| Metric   | Value  |
| -------- | ------ |
| Accuracy | 71.62% |

Confusion Matrix:

|          | Pred 0 | Pred 1 |
| -------- | ------ | ------ |
| Actual 0 | 13     | 11     |
| Actual 1 | 10     | 40     |

---

### Random Forest (Base)

| Metric    | Class 0 (No Rain) | Class 1 (Rain) |
| --------- | ----------------- | -------------- |
| Precision | 0.75              | 0.83           |
| Recall    | 0.62              | 0.90           |
| F1        | 0.68              | 0.87           |

| Metric   | Value  |
| -------- | ------ |
| Accuracy | 81.08% |

Confusion Matrix:

|          | Pred 0 | Pred 1 |
| -------- | ------ | ------ |
| Actual 0 | 15     | 9      |
| Actual 1 | 5      | 45     |

---

### XGBoost

| Metric    | Class 0 (No Rain) | Class 1 (Rain) |
| --------- | ----------------- | -------------- |
| Precision | 0.57              | 0.78           |
| Recall    | 0.54              | 0.80           |
| F1        | 0.55              | 0.79           |

| Metric   | Value  |
| -------- | ------ |
| Accuracy | 71.62% |

Confusion Matrix:

|          | Pred 0 | Pred 1 |
| -------- | ------ | ------ |
| Actual 0 | 13     | 11     |
| Actual 1 | 10     | 40     |

---

## Hyperparameter Tuning (Random Forest)

GridSearchCV (5-Fold, scoring = F1)

### Best Parameters

```python
{
 'max_depth': 10,
 'max_features': 'sqrt',
 'min_samples_leaf': 1,
 'min_samples_split': 5,
 'n_estimators': 100
}
```

### Tuned Model Performance

| Metric        | Value  |
| ------------- | ------ |
| Best CV F1    | 0.8729 |
| CV Accuracy   | 0.8184 |
| Test Accuracy | 81.08% |
| Test F1       | 86.27% |

### Per-Class Metrics (Test Set)

| Metric    | Class 0 (No Rain) | Class 1 (Rain) |
| --------- | ----------------- | -------------- |
| Precision | 0.73              | 0.85           |
| Recall    | 0.67              | 0.88           |
| F1        | 0.70              | 0.86           |

---

## Final Model Selection

Random Forest (Tuned) was selected because:

* Highest cross-validated F1 score (0.8729)
* Most stable across folds
* Strong precision-recall balance on the minority class
* Minimal overfitting
* Best CV Accuracy (0.8184)

---

## Key Insights

* Ensemble methods outperform a single Decision Tree.
* Random Forest provides the most stable performance.
* Class weighting outperforms downsampling.
* Cross-validation aligns with test performance.
* Dataset size limits performance ceiling.

---

## Tech Stack

| Layer | Technology |
| ----- | ---------- |
| Backend | Flask, Python |
| ML | scikit-learn, XGBoost |
| Database | Supabase (PostgreSQL) — stores all predictions |
| Frontend | HTML, CSS, Vanilla JS |
| Deployment | Render |

---

## Environment Variables

```makefile
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-service-role-key
```

---

## Project Status

* Data cleaned
* No leakage
* Class imbalance handled
* Cross-validation completed
* Hyperparameter tuning completed
* Model saved
* Web application built
* Supabase integration complete
* Deployed to Render



