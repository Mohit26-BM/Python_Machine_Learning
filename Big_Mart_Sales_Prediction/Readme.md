# BigMart Sales Prediction Using Machine Learning

## Overview

This project predicts **item outlet sales** for a retail chain using machine learning regression models. Accurate sales prediction helps businesses improve inventory planning, pricing strategies, and outlet performance analysis.

The full pipeline covers data cleaning, missing value imputation, feature encoding, model training, hyperparameter tuning, performance comparison, and deployment as an interactive web application backed by a persistent cloud database.

---

## Dataset Description

- **Dataset file:** `train.csv`
- **Total records:** 8,523
- **Target variable:** `Item_Outlet_Sales`

### Key Features

| Feature | Type | Description |
|---|---|---|
| `Item_Weight` | Numerical | Weight of the product |
| `Item_Fat_Content` | Categorical | Low Fat / Regular |
| `Item_Visibility` | Numerical | Display area percentage in store |
| `Item_Type` | Categorical | Product category |
| `Item_MRP` | Numerical | Maximum retail price |
| `Outlet_Identifier` | Categorical | Unique outlet ID |
| `Outlet_Establishment_Year` | Numerical | Year outlet was established |
| `Outlet_Size` | Categorical | Small / Medium / High |
| `Outlet_Location_Type` | Categorical | Tier 1 / Tier 2 / Tier 3 |
| `Outlet_Type` | Categorical | Grocery Store / Supermarket Type 1–3 |

### Data Quality Notes

- Missing values in `Item_Weight` (1,463 records) and `Outlet_Size` (2,410 records)
- No duplicate records
- Inconsistent labels in `Item_Fat_Content`

---

## Data Preprocessing

### Handling Missing Values

- `Item_Weight` — filled using **mean imputation** (distribution was approximately symmetric, skew ≈ 0)
- `Outlet_Size` — filled using **mode per Outlet_Type** via pivot table mapping

### Feature Cleaning

Standardized inconsistent labels in `Item_Fat_Content`:

| Original | Standardized |
|---|---|
| `LF`, `low fat` | `Low Fat` |
| `reg` | `Regular` |

### Encoding

- **Label Encoding** applied to ordinal columns: `Outlet_Size`, `Outlet_Location_Type`
- **Label Encoding** applied to nominal columns: `Item_Fat_Content`, `Item_Type`, `Outlet_Identifier`, `Outlet_Type`
- `Item_Identifier` dropped — acts as a product ID with no predictive value

---

## Train–Test Split

- Training set: **80%**
- Test set: **20%**
- `random_state=2` fixed for reproducibility

---

## Models Trained

Three regression models were trained and evaluated:

- XGBoost Regressor
- Random Forest Regressor
- Decision Tree Regressor

---

## Baseline Model Performance

Initial results before hyperparameter tuning:

| Model | MAE (↓) | MSE (↓) | R² Score (↑) |
|---|---:|---:|---:|
| XGBoost Regressor | 858.95 | 1,495,063.46 | 0.5157 |
| Random Forest Regressor | 827.20 | 1,397,686.45 | 0.5472 |
| Decision Tree Regressor | 1,078.39 | 2,303,799.63 | 0.2537 |

---

## Hyperparameter Tuning

`RandomizedSearchCV` with 5-fold cross-validation and 30 iterations was used to tune both top-performing models.

### XGBoost — Search Space

```python
xgb_params = {
    'n_estimators':      [100, 200, 300],
    'learning_rate':     [0.01, 0.05, 0.1, 0.2],
    'max_depth':         [3, 5, 7, 9],
    'subsample':         [0.6, 0.8, 1.0],
    'colsample_bytree':  [0.6, 0.8, 1.0]
}
```

### XGBoost — Best Parameters

```
n_estimators=100, learning_rate=0.05, max_depth=3,
subsample=0.8, colsample_bytree=1.0
```

### Random Forest — Search Space

```python
rf_params = {
    'n_estimators':      [100, 200, 300, 500],
    'max_depth':         [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf':  [1, 2, 4],
    'max_features':      ['sqrt', 'log2']
}
```

### Random Forest — Best Parameters

```
n_estimators=500, max_depth=10, min_samples_split=10,
min_samples_leaf=2, max_features='log2'
```

---

## Final Model Performance (Post-Tuning)

| Model | MAE (↓) | MSE (↓) | R² Score (↑) | Improvement |
|---|---:|---:|---:|---:|
| XGBoost Regressor | 787.76 | 1,269,865.49 | **0.5887** | +7.3% |
| Random Forest Regressor | 794.22 | 1,288,989.49 | 0.5825 | +3.5% |

**XGBoost was selected as the final model** — it achieved the best R², lowest MAE, and lowest MSE after tuning. The shallow tree depth (`max_depth=3`) combined with a low learning rate (`0.05`) indicates a well-regularized model that generalizes rather than memorizing training data.

---

## Key Insights

- Hyperparameter tuning improved XGBoost R² from 0.5157 → 0.5887 (+7.3%)
- Shallow XGBoost trees with slow learning outperformed deeper configurations
- Random Forest required 500 estimators to reach peak performance
- Decision Tree significantly overfits and was dropped from the final pipeline
- ~0.59 R² is close to the ceiling for this dataset — sales data contains inherent noise from factors like promotions and seasonality not captured in the features

---

## Deployment

The final XGBoost model is deployed as a **Streamlit web application** with three pages:

### Predict
- Input form for item and outlet details
- Instant sales prediction with comparison to dataset average
- Every prediction is automatically saved to the database

### Dashboard
- KPI cards: total predictions, average sales, highest prediction
- 6 visualizations: sales over time, by outlet type, by item type, by location tier, MRP vs sales scatter, by fat content

### History
- Full prediction log with filter controls (Outlet ID, Outlet Type, Sales Range)
- Download filtered results as CSV

### Tech Stack

| Layer | Technology |
|---|---|
| Model | XGBoost (joblib serialized) |
| Frontend | Streamlit |
| Database | Supabase (PostgreSQL) |
| Hosting | Streamlit Community Cloud |

### Supabase Integration

Predictions are persisted in a **Supabase PostgreSQL** database, replacing ephemeral CSV storage. This ensures prediction history survives app restarts, redeployments, and Streamlit's sleep cycles.

The `bigmart_predictions` table schema:

```
id                  int8        primary key, auto-increment
created_at          timestamptz default now()
item_weight         float8
item_fat_content    text
item_visibility     float8
item_type           text
item_mrp            float8
outlet_identifier   text
outlet_year         int8
outlet_size         text
outlet_location     text
outlet_type         text
predicted_sales     float8
```

Credentials are stored securely in **Streamlit Secrets** and never committed to the repository.

---

## Project Structure

```
Big_Mart_Sales_Prediction/
├── app.py                  # Main app — config, CSS, tabs, routing
├── best_model.pkl          # Serialized XGBoost model
├── model_columns.pkl       # Feature column order
├── requirements.txt        # Python dependencies
├── BigMart_Sales.ipynb     # Training notebook
├── utils/
│   ├── __init__.py
│   ├── model.py            # Model loading and feature mappings
│   └── database.py         # Supabase client and fetch helper
└── pages/
    ├── __init__.py
    ├── predict.py          # Predict page
    ├── dashboard.py        # Dashboard page
    └── history.py          # History page
```

---

## Requirements

```
streamlit
pandas
numpy
scikit-learn
xgboost
joblib
supabase
```

Install with:

```bash
pip install streamlit pandas numpy scikit-learn xgboost joblib supabase
```

---

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/python_machine_learning.git
cd python_machine_learning/Big_Mart_Sales_Prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add Streamlit secrets
mkdir .streamlit
echo '[secrets]
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_anon_key"' > .streamlit/secrets.toml

# 4. Run the app
streamlit run app.py
```

---

## Conclusion

This project demonstrates an end-to-end machine learning pipeline — from raw data preprocessing through model selection, hyperparameter tuning, and production deployment. XGBoost with tuned shallow trees delivered the best performance at R² = 0.589, and the application persists all predictions in a cloud database for ongoing analytics via the built-in dashboard.
