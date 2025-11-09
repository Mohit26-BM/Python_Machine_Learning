# ASD Classification Analysis

## Dataset Overview

* The dataset includes features such as:

  * Demographic info (`age`, `gender`, `ethnicity`, `relation`, etc.)
  * ASD screening scores (`A1_Score` to `A10_Score`)
  * Other relevant attributes like `jaundice`, `used_app_before`
* Target variable: `Class/ASD`

  * Class 0: Non-ASD (639 samples)
  * Class 1: ASD (161 samples)

---

## Step-by-step Data Preprocessing

### 1. Handling Missing Values

* Some categorical columns (`ethnicity`, `relation`, etc.) contain missing values represented as `"?"`.
* These `"?"` entries were replaced with a new category `"Others"` to avoid dropping data and preserve information.

### 2. Handling Categorical Variables

* Categorical features with `Yes/No` or multiple categories were label encoded or one-hot encoded (depending on the pipeline).
* For features like `relation`, categories with low counts (e.g., `Relative`, `Health care professional`) were combined into `"Others"` to reduce sparsity.

### 3. Outlier Detection and Treatment

* Outliers were detected in numerical columns (`age`, `result`) using the Interquartile Range (IQR) method:

  * Lower bound = Q1 - 1.5 * IQR
  * Upper bound = Q3 + 1.5 * IQR
* Two datasets were created:

  * **Original dataset:** Outliers left as-is.
  * **Cleaned dataset:** Outliers replaced with the median value to reduce their impact.

### 4. Train-Test Split

* Both datasets were split into training (80%) and testing (20%) sets using stratified sampling to preserve class proportions.

### 5. Handling Class Imbalance with SMOTE

* The dataset is imbalanced (ASD class ~20% of total).
* Synthetic Minority Over-sampling Technique (SMOTE) was applied **only on the training sets** to synthetically generate minority class examples and balance classes.
* This helps models learn better representations of ASD cases.

---

## Modeling and Evaluation

Three classifiers were evaluated on both datasets (original and cleaned):

* **Decision Tree Classifier**
* **Random Forest Classifier**
* **XGBoost Classifier**

### Model Training

* For each classifier:

  * Applied SMOTE to training data.
  * Trained model on resampled data.
  * Evaluated using:

    * 5-fold cross-validation accuracy on training data.
    * Test set performance (Accuracy, Precision, Recall, F1-score for ASD class).

---

## Cross-Validation and Test Performance (Before Hyperparameter Tuning)

| Model         | Dataset          | Mean CV Accuracy (%) | Test Accuracy (%) | Precision (ASD) (%) | Recall (ASD) (%) | F1-Score (ASD) (%) |
| ------------- | ---------------- | -------------------- | ----------------- | ------------------- | ---------------- | ------------------ |
| Random Forest | Original         | 82.97                | 83.13             | 61                  | 69               | 65                 |
| Random Forest | Outlier-Replaced | 83.44                | 85.00             | 64                  | 78               | 70                 |
| Decision Tree | Original         | 80.00                | 79.00             | 54                  | 53               | 54                 |
| Decision Tree | Outlier-Replaced | 80.00                | 76.00             | 46                  | 47               | 47                 |
| XGBoost       | Original         | 81.56                | 81.00             | 56                  | 61               | 59                 |
| XGBoost       | Outlier-Replaced | 81.87                | 83.00             | 61                  | 69               | 65                 |

---

## Hyperparameter Tuning Results

### Decision Tree, Random Forest, and XGBoost

| Model         | Dataset          | Accuracy (%) | Precision (ASD) (%) | Recall (ASD) (%) | F1-score (ASD) (%) | Best Hyperparameters                                                                                                    |
| ------------- | ---------------- | ------------ | ------------------- | ---------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Decision Tree | Original         | 78.12        | 51.06               | 66.67            | 57.83              | `min_samples_split=5`, `min_samples_leaf=1`, `max_depth=5`, `criterion='gini'`                                          |
| Decision Tree | Outlier-Replaced | 75.62        | 47.37               | 75.00            | 58.06              | `min_samples_split=2`, `min_samples_leaf=2`, `max_depth=5`, `criterion='gini'`                                          |
| Random Forest | Original         | 85.00        | 61.11               | 91.67            | 73.33              | `n_estimators=200`, `min_samples_split=5`, `min_samples_leaf=2`, `max_depth=5`, `criterion='entropy'`, `bootstrap=True` |
| Random Forest | Outlier-Replaced | 83.75        | 58.93               | 91.67            | 71.74              | `n_estimators=100`, `min_samples_split=5`, `min_samples_leaf=2`, `max_depth=5`, `criterion='gini'`, `bootstrap=True`    |
| XGBoost       | Original         | 83.12        | 58.49               | 86.11            | 69.66              | `subsample=0.6`, `n_estimators=300`, `max_depth=5`, `learning_rate=0.01`, `colsample_bytree=0.6`                        |
| XGBoost       | Outlier-Replaced | 81.25        | 55.56               | 83.33            | 66.67              | `subsample=0.6`, `n_estimators=300`, `max_depth=5`, `learning_rate=0.01`, `colsample_bytree=0.6`                        |

---

## Key Insights

1. **Random Forest** consistently performs best:

   * High **recall** (~91%) → effectively identifies most ASD cases.
   * Good **F1-score** (71–73%) → balances precision and recall.
2. **XGBoost** is slightly behind Random Forest, with F1-score ~66–70%.
3. **Decision Tree** performs worst, with lower accuracy, precision, and recall.
4. **Outlier treatment** (median replacement) slightly reduced performance in some cases; SMOTE handled the imbalance well.
5. **Hyperparameter tuning** improves model performance, especially for Random Forest.

---

This README now provides:

* Dataset overview and preprocessing steps
* Model evaluation before and after hyperparameter tuning
* Comprehensive metrics for comparison across **all models** and datasets

---
---
