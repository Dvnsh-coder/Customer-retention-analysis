# Customer Engagement & Product Utilization Analytics

## Retention Strategy Dashboard

### 1. Project Overview

This project analyzes customer engagement, product utilization, and churn patterns in a European banking dataset. Its objective is to identify customer groups with higher churn rates, understand the relationship between product usage and customer retention, and develop data-driven recommendations to support customer retention strategies.

The project combines exploratory data analysis, business-rule-based customer segmentation, retention metrics, and an interactive Streamlit dashboard.

### 2. Business Objectives

- Analyze customer engagement patterns and their relationship with churn.
- Evaluate how the number of banking products relates to customer retention.
- Identify inactive customers with relatively high account balances.
- Develop customer risk-prioritization segments.
- Recommend targeted retention strategies based on analytical findings.

### 3. Dataset Overview

The analysis uses a European banking customer dataset containing **10,000 customer records and 14 original columns**.

Key attributes include:

- **Customer Profile:** Age, Gender, Geography, Tenure
- **Financial Information:** Balance, Estimated Salary, Credit Score
- **Product Information:** Number of Products, Credit Card Ownership
- **Engagement:** Active Membership
- **Target Variable:** Customer Exit Status

The dataset represents customer records for the year 2025.

### 4. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter Notebook

### 5. Analytical Methodology

The project follows a descriptive and business-rule-based analytical approach.

1. Data loading, inspection, and quality validation.
2. Exploratory analysis of customer demographics, financial attributes, and product usage.
3. Customer engagement classification using activity and product-usage indicators.
4. Product utilization and churn-rate analysis.
5. Identification of inactive customers with above-median balances.
6. Development of a descriptive Relationship Strength Index (RSI).
7. Customer risk prioritization using defined business rules.
8. Formulation of targeted retention recommendations.

### 6. Key Findings

- Overall customer churn rate: **20.37%**.
- Inactive customers had a higher churn rate than active customers.
- Customers using one product had a churn rate of **27.71%**, compared with **7.58%** for customers using two products.
- Customers using three or four products showed very high churn rates, but these groups had relatively small sample sizes.
- The high-priority segment contained **2,456 inactive customers with above-median balances**.
- Among these, **1,662 customers were retained**, representing an actionable group for targeted engagement campaigns.

### 7. Interactive Dashboard

The Streamlit dashboard provides four analytical modules:

- **Engagement & Churn Overview:** Customer engagement distribution and retention indicators.
- **Product Utilization:** Product-count distribution and corresponding churn patterns.
- **High-Value Disengaged Detector:** Identification of retained, inactive customers with above-median balances.
- **Retention Strength Analysis:** Analysis of the descriptive Relationship Strength Index and its components.

The dashboard also supports interactive filtering by engagement segment, product count, balance, and estimated salary.

### 8. Project Structure

```text
Customer-retention-analytics/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   └── European_Bank.csv
│   └── processed/
│       └── .gitkeep
│
├── notebooks/
│   └── 01_data_understanding.ipynb
│
├── .gitignore
├── requirements.txt
└── README.md
```

### 9. Installation and Execution

**Prerequisites:** Python and Git.

1. Navigate to the project directory.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment.

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

4. Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

5. Run the Streamlit dashboard from the project root:

```bash
python -m streamlit run dashboard/app.py
```

Open the local URL displayed in the terminal.

**Dataset requirement:** Place the authorized dataset at `data/raw/European_Bank.csv` before running the dashboard. The raw dataset is not included in the repository.

### 10. Limitations

- The dataset represents a single year (2025), so the analysis does not establish longitudinal customer-retention trends.
- Customer activity is represented by an active-membership indicator; transaction-level engagement data is unavailable.
- Product utilization is measured by product count, not by individual product types or combinations.
- The high-balance threshold is based on the dataset median and should not be interpreted as a universal measure of customer wealth.
- Customer risk categories and the Relationship Strength Index are descriptive business-rule-based measures, not trained predictive models.
- Findings describe associations and should not be interpreted as evidence of causation.

### 11. Conclusion

The analysis highlights meaningful differences in churn across customer engagement and product-utilization groups. It identifies retained, inactive customers with above-median balances as a potential priority group for targeted engagement initiatives.

The dashboard translates these findings into an interactive analytical tool that can support customer-retention planning and business decision-making.

---

**Project Domain:** Banking Analytics | Customer Retention | Data Science