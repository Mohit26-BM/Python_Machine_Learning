# Rainfall Prediction System 🌧️

This project predicts the likelihood of rainfall based on weather data using machine learning models. The system includes **Decision Tree, Random Forest, and XGBoost** models, with hyperparameter tuning and a predictive system for new inputs.

---

## **Dataset Features**

The dataset includes the following columns:

- `pressure`
- `dewpoint`
- `humidity`
- `cloud`
- `sunshine`
- `winddirection`
- `windspeed`
- `rainfall` (target variable)

---

## **Data Preprocessing**

- Removed highly correlated or redundant features (e.g., `maxtemp`, `mintemp`, `temparature`) based on correlation analysis.
- Handled imbalanced data using **downsampling**.

---

## **Models Used**

1. **Decision Tree**
2. **Random Forest**
3. **XGBoost**

- Hyperparameter tuning was performed using **GridSearchCV** with 5-fold cross-validation.
- **F1 score** was used as the main evaluation metric due to class imbalance.

---

## **Cross-Validation Performance (5 Folds)**

| Model           | CV F1 Score | CV Accuracy |
|-----------------|------------|-------------|
| Decision Tree   | 0.7902     | 0.6596      |
| Random Forest   | 0.8163     | 0.7447      |
| XGBoost         | 0.8249     | 0.7660      |

---

## **Test Set Performance**

| Model           | Accuracy (%) | F1 Score (%) | Precision (%) | Recall (%) |
|-----------------|--------------|--------------|---------------|------------|
| Decision Tree   | 65.96        | 65.22        | 65.22         | 65.22      |
| Random Forest   | 74.47        | 75.00        | 72.00         | 78.26      |
| XGBoost         | 76.60        | 76.60        | 75.00         | 78.26      |

---

## **Making Predictions**

Example usage for a new weather input:

```python
import pandas as pd
import joblib

# Load trained models
models = joblib.load("best_models.pkl")
rf_model = models["RandomForest"]

# New input data
input_data = (1015.9, 19.9, 95, 81, 40.0, 13.7, 7)
input_df = pd.DataFrame([input_data], columns=[
    "pressure","dewpoint","humidity","cloud","sunshine","winddirection","windspeed"
])

# Prediction
prediction = rf_model.predict(input_df)
probability = rf_model.predict_proba(input_df)

print("Prediction:", "Rainfall" if prediction[0]==1 else "No Rainfall")
print("Probability of No Rainfall:", round(probability[0][0]*100,2), "%")
print("Probability of Rainfall:", round(probability[0][1]*100,2), "%")

# Key Insights

- XGBoost achieved the highest cross-validated F1 score and test accuracy.

- Random Forest is a close second and slightly more stable across folds.

- Decision Tree is simple but less accurate compared to ensemble methods.
