# Customer Segmentation Using K-Means Clustering

## Overview

This project applies **unsupervised machine learning** to segment mall customers based on their **annual income** and **spending behavior**.
Customer segmentation helps businesses understand purchasing patterns and design targeted marketing strategies.

The project uses **K-Means Clustering** along with the **Elbow Method** to determine the optimal number of customer groups.

---

## Dataset Description

* **Dataset file:** `Mall_Customers.csv`
* **Total records:** 200
* **Features:**

  * `CustomerID`: Unique customer identifier
  * `Gender`: Customer gender
  * `Age`: Customer age
  * `Annual Income (k$)`: Annual income in thousand dollars
  * `Spending Score (1-100)`: Score assigned based on customer spending behavior

### Data Quality

* No missing values
* Clean and well-structured dataset
* Suitable for clustering analysis

---

## Feature Selection

For clustering, the following features were selected:

* **Annual Income (k$)**
* **Spending Score (1-100)**

These features are commonly used for customer segmentation as they directly reflect purchasing capacity and behavior.

---

## Methodology

### 1. Elbow Method

* The Elbow Method was used to determine the optimal number of clusters.
* Within-Cluster Sum of Squares (WCSS) was calculated for cluster counts ranging from 1 to 10.
* The elbow point was observed at **K = 5**, indicating diminishing returns beyond this value.

### 2. K-Means Clustering

* Applied K-Means with:

  * `n_clusters = 5`
  * `init = 'k-means++'`
  * Fixed random state for reproducibility
* Each customer was assigned a cluster label based on similarity.

---

## Cluster Visualization

* Customers are visualized in a 2D space:

  * X-axis: Annual Income (k$)
  * Y-axis: Spending Score (1–100)
* Cluster centroids are highlighted to show the center of each group.
* Each cluster represents a distinct customer segment.

---

## Interpretation of Clusters

The five clusters generally represent:

* **Low income – low spending customers**
* **Low income – high spending customers**
* **Average income – average spending customers**
* **High income – low spending customers**
* **High income – high spending customers**

These segments can be directly used for targeted marketing and customer relationship strategies.

---

## Insights from Customer Segmentation

* Customers are clearly divided into **five distinct spending groups** based on income and behavior.
* **High income–high spending** customers are the most valuable and ideal for premium offers.
* **High income–low spending** customers represent an opportunity to increase engagement.
* **Low income–high spending** customers respond well to discounts and promotions.
* **Low income–low spending** customers are price-sensitive and contribute least to revenue.

**Key takeaway:**
Spending behavior does not always increase with income, making behavioral segmentation essential for targeted marketing.

---

## Requirements

Install the required libraries:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

## How to Run the Project

1. Clone the repository
2. Place `Mall_Customers.csv` in the project directory
3. Run the Python script or notebook
4. View the Elbow Method plot
5. Analyze customer clusters and centroids

---

## Future Improvements

* Include additional features such as age and gender
* Apply feature scaling for better distance measurement
* Compare with Hierarchical Clustering or DBSCAN
* Automate cluster labeling with business rules
* Deploy results in a dashboard (Power BI / Tableau)

---

## Conclusion

This project demonstrates how **K-Means clustering** can be used to uncover meaningful customer segments from transactional data. The resulting clusters provide actionable insights that can help businesses improve marketing effectiveness and customer engagement.
