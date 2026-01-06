# Fake News Detection Using Machine Learning

## Overview

This project builds a **Fake News Detection system** using Natural Language Processing (NLP) and multiple machine learning classifiers.
The goal is to classify news articles as **Real (0)** or **Fake (1)** based on textual content.

The project covers the full ML pipeline: data cleaning, text preprocessing, feature extraction using TF-IDF, model training, evaluation, and prediction.

---

## Dataset Description

* **Dataset file:** `train.csv`
* **Total records:** 20,800
* **Target variable:** `label`

  * `0` → Real news
  * `1` → Fake news

### Columns

* `id`: Unique identifier
* `title`: News headline
* `author`: Author name
* `text`: Full article content
* `label`: News authenticity

### Data Quality Notes

* Missing values present in `title`, `author`, and `text`
* No duplicate records
* Dataset is nearly balanced between real and fake news

---

## Data Cleaning and Preprocessing

Steps performed:

1. Dropped rows with missing `text`
2. Filled missing `title` with empty strings
3. Filled missing `author` with `"unknown"`
4. Combined `author`, `title`, and `text` into a single `content` column
5. Applied text preprocessing:

   * Removed non-alphabetic characters
   * Converted text to lowercase
   * Removed stopwords
   * Applied stemming using Porter Stemmer

---

## Feature Extraction

* Used **TF-IDF Vectorization** to convert text into numerical feature vectors
* This captures word importance while reducing the impact of common words

---

## Train-Test Split

* Training set: 80%
* Test set: 20%
* Stratified split to preserve class distribution

---

## Models Trained

The following classifiers were trained and evaluated:

* Logistic Regression
* Random Forest Classifier
* Multinomial Naive Bayes
* XGBoost Classifier
* LightGBM Classifier

---

## Model Performance Summary

| Model                    | Accuracy (Train) | Accuracy (Test) | Precision (Test) | Recall (Test) | F1-Score (Test) |
| ------------------------ | ---------------- | --------------- | ---------------- | ------------- | --------------- |
| Logistic Regression      | 97.98%           | 96.08%          | 0.96             | 0.96          | 0.96            |
| Random Forest Classifier | 100.00%          | 93.33%          | 0.91             | 0.96          | 0.93            |
| Naive Bayes Classifier   | 91.50%           | 88.20%          | 0.81             | 0.99          | 0.89            |
| XGBoost Classifier       | 99.98%           | 98.15%          | 0.98             | 0.98          | 0.98            |
| LightGBM Classifier      | 100.00%          | 98.15%          | 0.98             | 0.98          | 0.98            |

---

## What the Evaluation Metrics Mean

* **Accuracy:** Percentage of correctly classified news articles
  Example: 98.15% accuracy means about 98 out of 100 articles are classified correctly.

* **Precision:** When the model predicts *fake news*, how often it is correct.

* **Recall:** How much of the actual fake news the model successfully detects.

* **F1-Score:** Balance between precision and recall.

* **Confusion Matrix:**
  Shows correct and incorrect predictions for real and fake news.

---

## Key Observations

* Logistic Regression provides a strong and stable baseline
* Random Forest shows signs of overfitting
* Naive Bayes is fast but less accurate
* XGBoost and LightGBM achieve the **best overall performance**, balancing precision and recall
* Ensemble models generalize better on unseen data

---

## Example Prediction

**Input:** A news article from the test set
**Output:**

```
Prediction: Fake News
```

The predicted label matches the true label, demonstrating correct classification.

---

## Requirements

Install the required dependencies:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn nltk xgboost lightgbm
```

---

## How to Run the Project

1. Clone the repository
2. Place `train.csv` in the project directory
3. Download NLTK stopwords if not already available:

   ```python
   nltk.download('stopwords')
   ```
4. Run the Python script or notebook
5. Review accuracy, confusion matrices, and classification reports

---

## Future Improvements

* Hyperparameter tuning for ensemble models
* Use n-grams in TF-IDF
* Try transformer-based models (BERT)
* Add cross-validation
* Deploy as a web application or API

---

## Conclusion

This project demonstrates how machine learning and NLP techniques can effectively detect fake news. Among all models tested, **XGBoost and LightGBM deliver the best performance**, making them strong candidates for real-world fake news classification systems.
