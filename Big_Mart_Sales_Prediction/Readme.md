# BigMart Sales Prediction Using Machine Learning

## Overview

This project aims to predict **item outlet sales** for a retail chain using machine learning regression models.
Accurate sales prediction helps businesses improve inventory planning, pricing strategies, and outlet performance analysis.

The workflow includes data cleaning, handling missing values, feature encoding, model training, and performance comparison using multiple regression algorithms.

---

## Dataset Description

* **Dataset file:** `train.csv`
* **Total records:** 8,523
* **Target variable:** `Item_Outlet_Sales`

### Key Features

* `Item_Weight`
* `Item_Fat_Content`
* `Item_Visibility`
* `Item_Type`
* `Item_MRP`
* `Outlet_Identifier`
* `Outlet_Establishment_Year`
* `Outlet_Size`
* `Outlet_Location_Type`
* `Outlet_Type`

### Data Quality Notes

* Missing values present in:

  * `Item_Weight`
  * `Outlet_Size`
* No duplicate records
* Mix of numerical and categorical variables

---

## Data Preprocessing

### Handling Missing Values

* `Item_Weight` filled using **mean imputation**
* `Outlet_Size` filled using **mode based on Outlet_Type**

### Feature Cleaning

* Standardized inconsistent values in `Item_Fat_Content`

  * `LF`, `low fat` → `Low Fat`
  * `reg` → `Regular`

### Encoding

* Label Encoding applied to all categorical features
* `Item_Identifier` removed from modeling due to low predictive value

---

## Train–Test Split

* Training set: 80%
* Test set: 20%
* Random state fixed for reproducibility

---

## Models Trained

The following regression models were trained and evaluated:

* XGBoost Regressor
* Random Forest Regressor
* Decision Tree Regressor

---

## Model Performance Comparison

| Model                   |  MAE (↓) |      MSE (↓) | R² Score (↑) |
| ----------------------- | -------: | -----------: | -----------: |
| XGBoost Regressor       |   858.95 | 1,495,063.46 |       0.5157 |
| Random Forest Regressor |   827.20 | 1,397,686.45 |       0.5472 |
| Decision Tree Regressor | 1,078.39 | 2,303,799.63 |       0.2537 |

### What These Numbers Mean

* **MAE:** Average absolute error in predicted sales
* **MSE:** Penalizes larger prediction errors more heavily
* **R² Score:** Proportion of variance in sales explained by the model

Higher R² and lower MAE/MSE indicate better performance.

---

## Key Insights

* **Random Forest performs best overall**, achieving the lowest MAE and highest R² score
* **XGBoost provides competitive performance** with slightly higher error
* **Decision Tree significantly overfits**, resulting in poor generalization
* Ensemble models capture nonlinear relationships better than a single tree

---

## Requirements

Install required dependencies:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost
```

---

## How to Run the Project

1. Clone the repository
2. Place `train.csv` in the project directory
3. Run the Python script or notebook
4. Review evaluation metrics and compare model performance

---

## Future Improvements

* Feature scaling and normalization
* Hyperparameter tuning for ensemble models
* Cross-validation for robustness
* Try LightGBM or CatBoost
* Deploy as a sales forecasting API or dashboard

---

## Conclusion

This project demonstrates how machine learning models can predict retail sales using historical product and outlet data. Among the tested models, **Random Forest Regressor** delivers the best balance of accuracy and generalization, making it suitable for real-world sales forecasting tasks.
