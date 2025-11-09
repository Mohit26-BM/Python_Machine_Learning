# Loan Approval Prediction (PySpark)

Predicts loan approval status (Approved / Not Approved) using Logistic Regression in PySpark MLlib.

## Dataset
Kaggle: https://www.kaggle.com/datasets/ninzaami/loan-predication  
The dataset contains applicant income, credit history, dependents, property type, and final loan status.

## Workflow
1. Load data into Spark DataFrame
2. Handle missing values
3. Encode categorical variables (`StringIndexer`, `OneHotEncoder`)
4. Assemble all features into a vector
5. Train Logistic Regression
6. Evaluate with Accuracy and F1-score
7. Visualize actual vs predicted results

## Results
- Accuracy ~78%
- F1-score ~76%
- Strong at detecting approved loans
- Some false approvals on rejected cases

## Files
- `Loan_Prediction.ipynb` – full code in PySpark
- `screenshots/` – output and charts
- `report.pdf` or `report.docx` – final report

## How to Run
Requires PySpark, Pandas, Matplotlib, Seaborn, scikit-learn.

```bash
pip install pyspark pandas matplotlib seaborn scikit-learn
