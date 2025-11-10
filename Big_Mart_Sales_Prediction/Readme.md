# Big Mart Sales Prediction using Machine Learning

This project predicts product sales across Big Mart outlets using machine learning.  
The goal is to help retail planning, optimize inventory, and understand sales patterns through data-driven modeling.

---

## Project Overview

The notebook performs end-to-end regression modeling on historical sales data from Big Mart.  
It includes data cleaning, exploratory analysis, feature encoding, model training, and performance evaluation.

---

## Dataset

The dataset contains product and outlet features that influence sales.  
Key columns include:

| Feature | Description |
|---------|-------------|
| `Item_Identifier` | Unique product ID |
| `Item_Weight` | Weight of the product |
| `Item_Fat_Content` | Type of fat content (Low Fat / Regular) |
| `Item_Visibility` | Display visibility in store |
| `Item_Type` | Category of product |
| `Item_MRP` | Maximum retail price |
| `Outlet_Identifier` | Unique store ID |
| `Outlet_Size` | Size of the outlet |
| `Outlet_Location_Type` | Tier 1/2/3 |
| `Outlet_Type` | Grocery or Supermarket category |
| `Item_Outlet_Sales` | **Target Variable** – product sales figure |

---

##  Approach

### 1. Data Cleaning
- Checked for null values
- Imputed missing `Item_Weight` using mean
- Filled missing `Outlet_Size` using mode by `Outlet_Type`
- Corrected inconsistent entries in `Item_Fat_Content`

### 2. Exploratory Data Analysis
- Distribution plots for numeric variables  
- Count plots for categorical variables  
- Identified skew, sales variation, and category frequency

### 3. Feature Engineering
- Label Encoding applied to categorical columns:
  - `Item_Fat_Content`
  - `Item_Type`
  - `Outlet_Identifier`
  - `Outlet_Size`
  - `Outlet_Location_Type`
  - `Outlet_Type`

### 4. Model Training
Algorithms used:
- **XGBRegressor**
- **RandomForestRegressor**
- **DecisionTreeRegressor**

Data split:
```python
train_test_split(X, y, test_size=0.2, random_state=2)
````

---

## Model Performance

| Model                       | MAE      | MSE        | R² Score |
| --------------------------- | -------- | ---------- | -------- |
| **XGBoost Regressor**       | ~858.95  | ~1,495,063 | ~0.516   |
| **Random Forest Regressor** | ~827.19  | ~1,397,686 | ~0.547   |
| **Decision Tree Regressor** | ~1078.39 | ~2,303,799 | ~0.254   |

**Best Model:** Random Forest (highest R²)

---

## 🛠 Dependencies

```python
numpy
pandas
matplotlib
seaborn
sklearn
xgboost
```

---

## How to Run

1. Clone repository
2. Place `train.csv` in working directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the notebook or script

---

## Outcome

* A trained machine learning model that predicts outlet sales
* Insights into key factors affecting retail performance
* Useful for inventory forecasting and business decision support

---

## Future Improvements

* Hyperparameter tuning (GridSearch / RandomizedSearch)
* Feature scaling and one-hot encoding for higher accuracy
* Try Gradient Boosting, LightGBM, or Neural Networks
* Deploy model using Flask / FastAPI

---
