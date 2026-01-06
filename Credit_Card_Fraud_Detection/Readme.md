# Credit Card Fraud Detection Using Machine Learning

## Overview

This project focuses on detecting **fraudulent credit card transactions** using supervised machine learning classification models.
The main challenge addressed is **class imbalance**, as fraudulent transactions represent a very small fraction of total transactions.

The workflow includes data exploration, handling class imbalance through undersampling, model training, and evaluation using multiple classifiers.

---

## Dataset Description

* **Dataset file:** `creditcard.csv`
* **Total transactions:** 284,807
* **Fraudulent transactions:** 492
* **Legitimate transactions:** 284,315
* **Target variable:** `Class`

  * `0` → Legitimate transaction
  * `1` → Fraudulent transaction

### Key Characteristics

* Highly imbalanced dataset
* No missing values
* Features are anonymized numerical variables (`V1`–`V28`) plus `Amount` and `Time`

---

## Handling Class Imbalance

Since the dataset is highly imbalanced, **undersampling** was used:

* Randomly selected **492 legitimate transactions**
* Combined with **492 fraudulent transactions**
* Resulting balanced dataset size: **984 transactions**

This ensures fair model training and evaluation.

---

## Data Preparation

* Features (`X`) and target (`Y`) separated
* Stratified train-test split:

  * Training set: 80%
  * Test set: 20%

---

## Models Trained

The following classifiers were trained and evaluated:

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier

---

## Model Performance Summary

### Logistic Regression

* **Training Accuracy:** 95.04%
* **Test Accuracy:** 94.42%

Confusion Matrix:

```
[[97  2]
 [ 9 89]]
```

Strong balance between precision and recall, making it a reliable baseline model.

---

### Decision Tree Classifier

* **Training Accuracy:** 100.00%
* **Test Accuracy:** 89.85%

Confusion Matrix:

```
[[91  8]
 [12 86]]
```

Shows signs of **overfitting**, with perfect training accuracy but reduced test performance.

---

### Random Forest Classifier

* **Training Accuracy:** 100.00%
* **Test Accuracy:** 92.39%

Confusion Matrix:

```
[[97  2]
 [13 85]]
```

Provides better generalization than a single decision tree while maintaining strong fraud detection capability.

---

## Key Insights

* Class imbalance significantly affects fraud detection and must be handled carefully
* Logistic Regression offers strong and stable performance
* Decision Tree models tend to overfit on small balanced samples
* Random Forest improves robustness by aggregating multiple trees
* Recall for fraud detection is critical, as false negatives are costly

---

## Requirements

Install required dependencies:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

## How to Run the Project

1. Clone the repository
2. Place `creditcard.csv` in the project directory
3. Run the Python script or notebook
4. Review accuracy, confusion matrices, and classification reports

---

## Future Improvements

* Use SMOTE or other oversampling techniques instead of undersampling
* Evaluate models using ROC-AUC and Precision-Recall curves
* Hyperparameter tuning for ensemble models
* Deploy as a real-time fraud detection system

---

## Conclusion

This project demonstrates an effective approach to **credit card fraud detection** by addressing class imbalance and comparing multiple machine learning models. Logistic Regression and Random Forest show strong performance, making them suitable candidates for real-world fraud detection systems.
