# House Price Prediction Using Machine Learning

## Overview

This project focuses on predicting **house prices** using machine learning regression models, with a primary emphasis on **XGBoost Regressor**. The dataset is based on housing-related features such as crime rate, average number of rooms, accessibility, pollution levels, and socioeconomic factors.

The project demonstrates an end-to-end machine learning pipeline including data exploration, preprocessing, model training, evaluation, and performance analysis.

---

## Dataset Description

* **Dataset name:** `HousingData.csv`
* **Total records:** 506
* **Target variable:** `MEDV`
  Median value of owner-occupied homes (in thousands of USD)

### Features

| Feature | Description                                            |
| ------- | ------------------------------------------------------ |
| CRIM    | Per capita crime rate                                  |
| ZN      | Proportion of residential land zoned                   |
| INDUS   | Proportion of non-retail business acres                |
| CHAS    | Charles River dummy variable                           |
| NOX     | Nitric oxide concentration                             |
| RM      | Average number of rooms                                |
| AGE     | Proportion of owner-occupied units built prior to 1940 |
| DIS     | Distance to employment centers                         |
| RAD     | Accessibility to highways                              |
| TAX     | Property tax rate                                      |
| PTRATIO | Pupil–teacher ratio                                    |
| B       | Proportion of Black population                         |
| LSTAT   | Percentage of lower-status population                  |

---

## Exploratory Data Analysis (EDA)

Key findings:

* Multiple numerical features show strong correlation with house prices
* `RM` (number of rooms) positively correlates with house value
* `LSTAT` (lower status population) negatively correlates with house value
* Several features contain missing values (`CRIM`, `ZN`, `INDUS`, `CHAS`, `AGE`, `LSTAT`)
* The target variable (`MEDV`) shows right skew and capped values at the upper bound

---

## Data Preprocessing

* Features and target variable separated
* Missing values retained for baseline modeling (tree-based models can handle missing values)
* Dataset split into:

  * Training set: 80%
  * Test set: 20%
* No feature scaling required due to tree-based primary model

---

## Models Implemented

The following regression models were explored:

* XGBoost Regressor
* Linear Regression
* Random Forest Regressor
* Support Vector Regressor (SVR)

The final evaluation and analysis focus on **XGBoost Regressor** due to its superior performance.

---

## Model Training

* XGBoost Regressor trained on 404 samples
* Evaluated on 102 unseen test samples
* Default hyperparameters used as baseline

---

## Model Evaluation Metrics

The model was evaluated using:

* R² Score
* Mean Absolute Error (MAE)

---

## Model Performance

### Training Performance

| Metric   |   Value |
| -------- | ------: |
| R² Score | 0.99999 |
| MAE      |  0.0072 |

### Test Performance

| Metric   |  Value |
| -------- | -----: |
| R² Score | 0.8948 |
| MAE      | 2.0874 |

---

## Performance Interpretation

* The model fits the training data almost perfectly, which indicates very strong learning capacity
* A noticeable gap between training and test performance suggests **mild overfitting**
* Test results still show strong generalization, explaining nearly **89% of variance** in unseen data
* XGBoost effectively captures nonlinear relationships present in housing features

---

## Example Prediction Use Case

The trained model can be used to predict house prices for new input data by passing feature values such as crime rate, number of rooms, distance to employment centers, and tax rates.

Predicted values represent **median house price in thousands of USD**.

---

## Requirements

Install required dependencies:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost
```

---

## How to Run the Project

1. Clone the repository
2. Place `HousingData.csv` in the project directory
3. Run the Python script or notebook
4. Review training and test performance metrics
5. Experiment with feature values or alternative models

---

## Future Improvements

* Handle missing values using imputation techniques
* Perform hyperparameter tuning with GridSearchCV
* Apply cross-validation for more robust evaluation
* Feature importance visualization using SHAP
* Compare ensemble stacking approaches
* Deploy the model as a web application

---

## Conclusion

This project demonstrates the effectiveness of **XGBoost** for structured regression problems. Despite slight overfitting, the model achieves strong predictive performance and serves as a solid baseline for house price prediction tasks.
