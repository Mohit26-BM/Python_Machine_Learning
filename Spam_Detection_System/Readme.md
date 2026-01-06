# Spam Mail Detection Using Machine Learning

## Overview

This project implements a **spam mail detection system** using classical machine learning algorithms and Natural Language Processing (NLP) techniques. The goal is to classify emails as **Spam** or **Ham (Not Spam)** based on their textual content.

The workflow includes data preprocessing, feature extraction using TF-IDF, model training, evaluation, and building a simple predictive system for real-world email inputs.

---

## Dataset Description

* **Dataset name:** `mail_data.csv`
* **Total samples:** 5,572 emails
* **Features:**

  * `Message`: Email text
  * `Category`: Label (`spam` or `ham`)
* **Class distribution:**

  * Ham: 4,825
  * Spam: 747

The dataset is moderately imbalanced, which makes precision and recall important evaluation metrics in addition to accuracy.

---

## Project Workflow

1. **Data Loading**

   * Load the dataset using Pandas.
   * Handle missing values by replacing them with empty strings.

2. **Label Encoding**

   * Spam → `0`
   * Ham → `1`

3. **Train-Test Split**

   * 80% training data
   * 20% testing data
   * Fixed random state for reproducibility

4. **Feature Extraction**

   * Text data converted into numerical vectors using **TF-IDF Vectorization**
   * Stop words removed
   * All text converted to lowercase

5. **Model Training**

   * Multiple machine learning classifiers are trained and evaluated:

     * Logistic Regression
     * Naive Bayes
     * Random Forest
     * Decision Tree
     * Support Vector Machine (Linear Kernel)

6. **Evaluation Metrics**

   * Accuracy
   * Precision
   * Recall
   * F1-score
   * Confusion Matrix

7. **Predictive System**

   * Classifies new, unseen email text as Spam or Ham

---

## Models Used

* Logistic Regression
* Multinomial Naive Bayes
* Random Forest Classifier
* Decision Tree Classifier
* Support Vector Machine (Linear Kernel)

---

## Model Performance Comparison

| Model                  | Training Accuracy | Test Accuracy | Spam Recall | Ham Recall |
| ---------------------- | ----------------: | ------------: | ----------: | ---------: |
| Logistic Regression    |            96.77% |        96.68% |        0.76 |       1.00 |
| Naive Bayes            |            98.07% |        97.31% |        0.81 |       1.00 |
| Random Forest          |           100.00% |        97.58% |        0.83 |       1.00 |
| Decision Tree          |           100.00% |        96.59% |        0.77 |       1.00 |
| Support Vector Machine |            99.53% |        98.21% |        0.88 |       1.00 |

**Key Observations:**

* SVM achieved the best overall test accuracy.
* Random Forest and Decision Tree show perfect training accuracy, indicating potential overfitting.
* Naive Bayes performs very well despite its simplicity and low computational cost.
* Spam recall is consistently lower than ham recall due to class imbalance.

---

## Example Predictions

```python
input_mail = ["Congratulations! You've won a $1000 Walmart gift card. Click here to claim your prize."]
Prediction: Spam

input_mail = ["Hello, How are you doing today? I hope you're having a great day!"]
Prediction: Ham
```

---

## Requirements

Install the required dependencies before running the project:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

## How to Run

1. Clone the repository
2. Ensure `mail_data.csv` is in the project directory
3. Run the Python script
4. View evaluation metrics and confusion matrices
5. Modify input text to test custom email predictions

---

## Future Improvements

* Handle class imbalance using techniques like SMOTE or class weighting
* Perform hyperparameter tuning using GridSearchCV
* Add cross-validation for more robust evaluation
* Deploy the model as a web application using Flask or FastAPI
* Experiment with deep learning models such as LSTM or Transformers

---

## Conclusion

This project demonstrates a complete end-to-end machine learning pipeline for spam detection using NLP techniques. It highlights the effectiveness of traditional ML models and provides a strong baseline for further experimentation and deployment.

---
