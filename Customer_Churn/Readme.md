# Customer Churn Prediction – ML Project

This project predicts telecom customer churn using a full machine learning pipeline with preprocessing, SMOTE, cross-validation, model tuning, and real-world evaluation.

---
## Live Demo:  
[Customer Churn Prediction](https://customer-churn-prediction-x9i2.onrender.com/)

---

## 1. Project Workflow

* Data cleaning and preprocessing  
* Label encoding of categorical variables  
* Train–test split  
* Baseline evaluation (Dummy Classifier)  
* Class imbalance correction using SMOTE  
* Model training (Decision Tree, Random Forest, XGBoost)  
* Hyperparameter tuning using RandomizedSearchCV  
* Final model evaluation  
* Model and encoder saving (Pickle)  
* New customer churn prediction  

---

## 2. Baseline Model

A dummy classifier predicting only “No Churn”.

| Metric         | Value      |
| -------------- | ---------- |
| Accuracy       | 73.53%     |
| Churn Recall   | 0%         |
| Churn F1-score | 0.00       |

Meaning:  
Baseline accuracy appears high due to class imbalance but completely fails to detect churn.

---

## 3. Default Model Performance

### Cross-Validation Accuracy (SMOTE data)

| Model         | CV Accuracy |
| ------------- | ----------- |
| Decision Tree | 78.09%      |
| Random Forest | 83.79%      |
| XGBoost       | 83.12%      |

---

### Test Set Performance (Real Data)

#### Random Forest (Default)

* Accuracy: 77.7%  
* Churn Recall: 0.58  
* Churn F1-score: 0.58  

#### XGBoost (Default)

* Accuracy: 78.2%  
* Churn Recall: 0.61  
* Churn F1-score: 0.60  

Best default model: XGBoost

---

## 4. Hyperparameter Tuning

### Tuned Random Forest

Best parameters:

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

* Accuracy: 77.9%  
* Churn Recall: 0.61  
* Churn F1-score: 0.59  

Slight improvement over the default Random Forest.

---

### Tuned XGBoost

Best parameters:

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

* Accuracy: 78.1%  
* Churn Recall: 0.57  
* Churn F1-score: 0.58  

Tuning did not outperform the default XGBoost.

---

## 5. Final Comparison

| Model                 | Accuracy | Churn Recall | Churn F1 | Notes              |
| --------------------- | -------- | ------------ | -------- | ------------------ |
| Baseline              | 73.5%    | 0%           | 0.00     | Predicts all non-churn |
| Decision Tree         | 78.1%    | ~0.57        | ~0.57    | Weak               |
| RF (Default)          | 77.7%    | 0.58         | 0.58     | Good               |
| RF (Tuned)            | 77.9%    | 0.61         | 0.59     | Slight improvement |
| XGBoost (Default)     | 78.2%    | 0.61         | 0.60     | Best overall       |
| XGB (Tuned)           | 78.1%    | 0.57         | 0.58     | Slight drop        |

Best model: Default XGBoost

* +6–7% improvement over baseline accuracy  
* Churn recall improved from 0% → 61%  

---

## 6. Model Deployment Components

* `customer_churn_model.pkl` – Tuned Random Forest with feature names  
* `xgb_churn.pkl` – Default XGBoost model  
* `encoders.pkl` – Label encoders for all categorical variables  
* Custom pipeline for new customer predictions  

Example prediction output:

```text
Prediction: Churn
Churn Probability: 72.79%
```
---

## 7. Key Takeaways

* Baseline accuracy is misleading without recall and F1.  
* SMOTE significantly improves minority class detection.  
* Default XGBoost outperformed all tuned models.  
* Churn recall (most business-critical metric) improved dramatically.  
* Pipeline is deployment-ready with saved models and encoders.  
