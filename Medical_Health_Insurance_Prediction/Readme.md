# Insurance Cost Prediction Using Machine Learning

## Overview

This project focuses on predicting **medical insurance charges** using machine learning regression models. The objective is to estimate insurance costs based on demographic and health-related attributes such as age, BMI, smoking status, and region.

The project demonstrates a complete end-to-end machine learning workflow including exploratory data analysis (EDA), data preprocessing, model training, evaluation, and real-world prediction.

---

## Dataset Description

* **Dataset name:** `insurance.csv`
* **Total records:** 1,338
* **Features:**

  * `age`: Age of the individual
  * `sex`: Gender (male/female)
  * `bmi`: Body Mass Index
  * `children`: Number of dependents
  * `smoker`: Smoking status
  * `region`: Residential area
  * `charges`: Medical insurance cost (target variable)

### Data Quality Summary

* No missing values
* 1 duplicated row
* Balanced gender distribution
* Majority of customers are non-smokers
* Charges show high variance and positive skew

---

## Exploratory Data Analysis (EDA)

Key observations from EDA:

* Smokers incur significantly higher insurance charges
* BMI and age show a positive correlation with charges
* Region has a smaller but noticeable influence on cost
* Insurance charges are highly skewed, indicating outliers

---

## Data Preprocessing

* Categorical variables converted to numerical values using label encoding:

  * `sex`: male → 0, female → 1
  * `smoker`: yes → 0, no → 1
  * `region`: Encoded into numeric categories
* Features and target variable separated
* Dataset split into training (80%) and testing (20%) sets

---

## Models Implemented

The following regression models were trained and evaluated:

* Linear Regression
* Decision Tree Regressor
* Random Forest Regressor

---

## Model Evaluation Metrics

Models were evaluated using:

* Mean Squared Error (MSE)
* Root Mean Squared Error (RMSE)
* Mean Absolute Error (MAE)
* R² Score

---

## Model Performance Comparison

| Model             | RMSE (USD) | MAE (USD) | R² Score |
| ----------------- | ---------: | --------: | -------: |
| Linear Regression |   6,191.69 |  4,267.21 |   0.7447 |
| Decision Tree     |   6,870.84 |  3,367.69 |   0.6857 |
| Random Forest     |   4,947.95 |  2,795.39 |   0.8370 |

**Key Insights:**

* Random Forest outperforms other models across all metrics
* Linear Regression provides a strong baseline with good interpretability
* Decision Tree shows higher variance and lower generalization performance

---

## Prediction Accuracy Within Error Thresholds

Number of predictions within a given absolute error range:

| Error Threshold | Linear Regression | Decision Tree | Random Forest |
| --------------- | ----------------: | ------------: | ------------: |
| ≤ $500          |                29 |           136 |            75 |
| ≤ $1,000        |                55 |           181 |           125 |
| ≤ $2,000        |               110 |           205 |           168 |
| ≤ $3,000        |               155 |           209 |           197 |
| ≤ $5,000        |               186 |           211 |           227 |

This highlights the **robustness of Random Forest** for real-world predictions.

---

## Model Performance Comparison

* **RMSE (USD)**
  Average size of prediction error, with larger mistakes penalized more.
  Example: Random Forest RMSE of **4,947.95** means predictions are typically off by about **$5,000**.

* **MAE (USD)**
  Average absolute difference between predicted and actual charges.
  Example: Random Forest MAE of **2,795.39** means predictions are usually within **$2,800** of the true value.

* **R² Score**
  Proportion of variance in insurance charges explained by the model.
  Example: R² of **0.8370** means the model explains **83.7%** of the cost variation.

---

### Prediction Accuracy Within Error Thresholds

* Each number shows **how many test cases** were predicted within the given dollar error.
* Example: Random Forest **≤ $1,000 = 125** means 125 predictions were within **$1,000** of the actual charge.
* Higher numbers indicate **more reliable and accurate predictions**.

---

## Example Prediction

**Input:**

```
Age: 31
Sex: Female
BMI: 25.74
Children: 0
Smoker: No
Region: Southeast
```

**Predicted Charges:**

* Linear Regression: ~$3,760
* Decision Tree: ~$3,757
* Random Forest: ~$3,943

---

## Requirements

Install the required dependencies:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

## How to Run the Project

1. Clone the repository
2. Place `insurance.csv` in the project directory
3. Run the Python script or notebook
4. Review EDA outputs and evaluation metrics
5. Modify input values to test new predictions

---

## Future Improvements

* One-hot encoding instead of label encoding for categorical variables
* Hyperparameter tuning using GridSearchCV
* Feature importance visualization
* Log transformation of target variable to handle skewness
* Deployment as a REST API or web application

---

## Conclusion

This project demonstrates how regression-based machine learning models can effectively predict insurance costs. Among all models, **Random Forest Regressor** provides the best performance, making it suitable for real-world cost estimation tasks.
