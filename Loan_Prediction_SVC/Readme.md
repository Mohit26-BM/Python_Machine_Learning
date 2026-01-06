# Loan Approval Prediction Using Machine Learning

## Overview

This project focuses on predicting **loan approval status** using machine learning classification techniques. Financial institutions can use such models to automate loan eligibility decisions based on applicant demographics, income, credit history, and property information.

The project demonstrates a full data science pipeline including exploratory data analysis, data cleaning, feature engineering, model training, evaluation, and real-world prediction.

---

## Dataset Description

* **Dataset name:** `loan.csv`
* **Total records (after cleaning):** 480
* **Target variable:** `Loan_Status`

  * 1 → Loan Approved
  * 0 → Loan Rejected

### Features

* `Gender`
* `Married`
* `Dependents`
* `Education`
* `Self_Employed`
* `ApplicantIncome`
* `CoapplicantIncome`
* `LoanAmount`
* `Loan_Amount_Term`
* `Credit_History`
* `Property_Area`

---

## Exploratory Data Analysis (EDA)

Key observations:

* Credit history is the strongest indicator of loan approval
* Majority of approved loans belong to applicants with credit history = 1
* Loan approvals are more frequent for graduates and urban/semiurban properties
* The dataset is moderately imbalanced in favor of approved loans
* Missing values are present in multiple categorical and numerical columns

---

## Data Cleaning and Preprocessing

Steps performed:

1. **Handling Missing Values**

   * Rows with missing values were removed for simplicity and consistency

2. **Label Encoding**

   * Loan_Status: Y → 1, N → 0
   * Gender: Male → 1, Female → 0
   * Married: Yes → 1, No → 0
   * Education: Graduate → 1, Not Graduate → 0
   * Self_Employed: Yes → 1, No → 0
   * Property_Area: Rural → 0, Semiurban → 1, Urban → 2

3. **Feature Engineering**

   * Converted `Dependents` from categorical (`3+`) to numerical values
   * Removed `Loan_ID` as it has no predictive value

---

## Train-Test Split

* Training set: 90%
* Test set: 10%
* Stratified split used to preserve class distribution

---

## Model Implemented

* **Support Vector Machine (Linear Kernel)**

The linear kernel was chosen for:

* Interpretability
* Strong performance on small to medium-sized datasets
* Ability to handle high-dimensional feature spaces

---

## Model Evaluation

### Performance Metrics

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

### Results

| Metric    |  Value |
| --------- | -----: |
| Accuracy  | 83.33% |
| Precision |   0.84 |
| Recall    |   0.94 |
| F1-score  |   0.89 |

### Confusion Matrix

|                 | Predicted Rejected | Predicted Approved |
| --------------- | -----------------: | -----------------: |
| Actual Rejected |                  9 |                  6 |
| Actual Approved |                  2 |                 31 |

**Observations:**

* Model performs well in identifying approved loans
* Recall for rejected loans is lower, indicating some false approvals
* Suitable for decision-support systems but may require stricter thresholds in production

---

## Example Prediction

**Input Applicant Profile:**

```
Gender: Female
Married: No
Dependents: 0
Education: Graduate
Self Employed: No
Applicant Income: 3510
Coapplicant Income: 0
Loan Amount: 76
Loan Term: 360
Credit History: 0
Property Area: Urban
```

**Predicted Output:**

```
Loan Status: Rejected
```

---

## Requirements

Install the required dependencies:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

## How to Run the Project

1. Clone the repository
2. Place `loan.csv` in the project directory
3. Run the Python script or notebook
4. Review evaluation metrics and confusion matrix
5. Modify input features to test new predictions

---

## Future Improvements

* Compare multiple classifiers (Logistic Regression, Random Forest, KNN)
* Handle class imbalance using SMOTE or class weighting
* Use imputation instead of row deletion for missing values
* Perform hyperparameter tuning with GridSearchCV
* Deploy as a loan eligibility web application

---

## Conclusion

This project demonstrates how machine learning can assist in loan approval decisions by leveraging applicant data. The Support Vector Machine model provides a strong baseline with reliable performance and interpretability, making it suitable for financial decision-support systems.
