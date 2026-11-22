# Customer Engagement and Product Utilization Analytics for Data-Driven Retention Strategy in Banking

**RESEARCH PAPER**

**Author:** Devansh Sharma

**Institution:** Unified Mentor

**Project Domain:** Data Science and Banking Analytics

**Under the Guidance of:** Sandeep CS




## Abstract

Customer retention is an important concern for banking institutions because customer disengagement and account closure can affect long-term customer relationships and business performance. Understanding the relationship between customer engagement, product utilization, and churn can help institutions identify customer groups that may require targeted retention strategies.

This study analyzes a European banking customer dataset containing 10,000 customer records and 14 original attributes. The analysis uses Python-based exploratory data analysis (EDA), customer engagement classification, product utilization analysis, financial analysis, and business-rule-based customer risk prioritization. A descriptive Relationship Strength Index (RSI) is also developed to examine customer relationship characteristics.

The results indicate an overall customer churn rate of 20.37%. Inactive customers demonstrate a higher churn rate than active customers. Customers using one banking product have a churn rate of 27.71%, while customers using two products have a churn rate of 7.58%. The analysis also identifies 2,456 inactive customers with above-median account balances, including 1,662 customers who have not exited and may represent an actionable group for targeted engagement initiatives.

The findings demonstrate how descriptive analytics can support customer segmentation and retention planning. The study also highlights the importance of interpreting analytical results within the limitations of the available dataset.

**Keywords:** Customer Retention, Customer Churn, Exploratory Data Analysis, Product Utilization, Customer Engagement, Banking Analytics, Data Science.

---

## 1. Introduction

Customer retention is a significant aspect of the banking industry. Banks invest resources in acquiring customers, maintaining relationships, and providing financial products and services. However, customers may discontinue their banking relationships because of changing financial requirements, dissatisfaction, reduced engagement, or other factors.

Customer churn refers to customers discontinuing their relationship with an institution. Analyzing churn patterns can help organizations understand which customer groups are more likely to leave and where retention initiatives may be useful.

Customer engagement and product utilization are two important dimensions of customer relationship analysis. Customers who actively engage with banking services or use multiple products may demonstrate different retention patterns from customers with limited engagement. Financial characteristics, such as account balance, can also provide additional context when identifying customer groups for retention attention.

This project applies data analytics techniques to examine customer engagement, product utilization, financial characteristics, and churn patterns in a European banking dataset. The objective is to convert customer-level information into meaningful analytical insights and practical retention recommendations.

## 2. Problem Statement and Objectives

### 2.1 Problem Statement

Banking institutions need to identify customer groups that demonstrate higher churn rates and understand the characteristics associated with customer disengagement. Without structured analysis, it may be difficult to prioritize retention initiatives or identify customers who could benefit from targeted engagement.

This project addresses the problem by analyzing customer engagement indicators, product utilization, financial attributes, and customer exit status to identify patterns that can support retention planning.

### 2.2 Objectives

The primary objectives are:

1. Analyze customer demographics and financial characteristics.
2. Examine the relationship between customer engagement and churn.
3. Evaluate churn patterns across different product-usage groups.
4. Identify inactive customers with relatively high account balances.
5. Develop descriptive customer engagement and risk-prioritization segments.
6. Construct a Relationship Strength Index to summarize selected relationship indicators.
7. Develop practical recommendations based on the analytical findings.

## 3. Dataset Description and Methodology

### 3.1 Dataset Description

The study uses a European banking customer dataset containing 10,000 records and 14 original columns. The dataset represents customer information for the year 2025.

The attributes cover several categories:

- **Customer demographics:** Age, gender, and geography.
- **Financial characteristics:** Account balance, estimated salary, and credit score.
- **Relationship information:** Tenure and credit card ownership.
- **Product utilization:** Number of products held by each customer.
- **Engagement:** Active membership indicator.
- **Outcome variable:** Customer exit status.

The target variable, `Exited`, indicates whether a customer has exited the banking relationship.

### 3.2 Data Preparation and Quality Assessment

The dataset was inspected to understand its structure, data types, distributions, and completeness. The initial dataset contained 10,000 records and 14 columns.

The data quality assessment identified no missing values or duplicate rows. The dataset was also checked for valid categorical values, numerical ranges, and the binary nature of the customer exit variable.

Customer identification fields were excluded from analytical presentation because they do not contribute meaningful behavioural information to the segmentation analysis.

### 3.3 Analytical Methodology

A descriptive and business-rule-based analytical approach was adopted.

The analysis was conducted through the following stages:

1. Data inspection and validation.
2. Exploratory analysis of demographic, financial, and behavioural attributes.
3. Comparison of churn rates across engagement groups.
4. Product utilization and retention analysis.
5. Identification of inactive customers with above-median balances.
6. Development of engagement segments and risk-prioritization categories.
7. Construction and interpretation of the Relationship Strength Index.
8. Development of retention recommendations.

The analysis uses Python libraries, including Pandas and NumPy for data manipulation and numerical analysis, Matplotlib and Seaborn for notebook visualizations, and Plotly and Streamlit for interactive dashboard presentation.

### 3.4 Customer Segmentation and Relationship Strength Index

Customer engagement was classified using activity status and product utilization. The analysis produced four engagement segments:

- Active Engaged
- Active but Low-Product
- Inactive High-Balance
- Inactive Disengaged

A separate risk-prioritization framework classified customers into five categories: High Priority, Elevated Priority, Moderate Priority, Lower Priority, and Special Monitoring.

The Relationship Strength Index (RSI) was developed as a descriptive composite measure using four components:

- Active membership: 25%
- Credit card ownership: 25%
- Product count, capped at two: 25%
- Tenure, scaled against ten years: 25%

The weighted components were combined and expressed on a 0–100 scale. The index is intended to summarize selected customer relationship indicators. It is not a calibrated churn probability or a trained predictive model.

## 4. Exploratory Data Analysis and Key Findings

### 4.1 Overall Customer Churn

The dataset contains 10,000 customers, of whom 7,963 were retained and 2,037 exited.

| Customer Status | Number of Customers | Percentage |
|---|---:|---:|
| Retained | 7,963 | 79.63% |
| Exited | 2,037 | 20.37% |
| Total | 10,000 | 100% |

The overall churn rate of 20.37% establishes the baseline for comparing customer groups throughout the analysis.

### 4.2 Customer Engagement and Churn

Customer activity showed a meaningful association with retention outcomes.

Active customers had a churn rate of approximately 14.27%, while inactive customers had a churn rate of approximately 26.85%.

The engagement segmentation produced the following results:

| Engagement Segment | Customers | Churn Rate |
|---|---:|---:|
| Active Engaged | 2,588 | 9.66% |
| Active but Low-Product | 2,563 | 18.92% |
| Inactive High-Balance | 2,456 | 32.33% |
| Inactive Disengaged | 2,393 | 21.23% |

The Active Engaged segment recorded the lowest churn rate. The Inactive High-Balance segment recorded the highest churn rate among the four engagement groups.

These results suggest that customer activity status is an important indicator for descriptive retention analysis. However, active membership is only a proxy for engagement and does not provide detailed transaction-level behaviour.

### 4.3 Product Utilization Analysis

Product utilization was examined by comparing customer counts and churn rates across the number of products held.

| Number of Products | Customers | Exited Customers | Churn Rate |
|---|---:|---:|---:|
| 1 | 5,084 | 1,409 | 27.71% |
| 2 | 4,590 | 348 | 7.58% |
| 3 | 266 | 220 | 82.71% |
| 4 | 60 | 60 | 100.00% |

Customers using two products demonstrated a considerably lower churn rate than customers using one product.

However, the three-product and four-product groups recorded very high churn rates despite having relatively small sample sizes. These results require cautious interpretation and should not be generalized without further investigation.

The analysis also indicates that simply having more products does not guarantee stronger retention. Product suitability, customer experience, and actual usage behaviour may require additional investigation.

### 4.4 Identification of High-Value Disengaged Customers

To identify customers who may deserve additional retention attention, the analysis examined inactive customers with above-median account balances.

The dataset median balance was approximately 97,198.54. This threshold was used as a relative segmentation boundary within the dataset rather than as a universal definition of high-value customers.

The resulting high-priority segment contained 2,456 inactive customers with above-median balances. Among them, 794 had exited and 1,662 remained customers of the bank.

The retained group of 1,662 customers represents a potential target for proactive engagement campaigns. Their average account balance was approximately 131,360.36.

This segment is particularly relevant because it combines an inactivity indicator with a relatively higher account balance. However, account balance should be treated as a proxy for potential financial value, not as a direct measure of profitability or customer lifetime value.

### 4.5 Relationship Strength Analysis

The Relationship Strength Index provides a descriptive summary of selected customer relationship indicators.

The average RSI scores were:

| Customer Group | Average RSI |
|---|---:|
| Retained Customers | 63.36 |
| Exited Customers | 55.18 |
| Overall Customers | 61.69 |

Retained customers demonstrated a higher average RSI than exited customers. This indicates that the selected relationship indicators collectively differed between the two groups.

However, the difference does not establish causation or predictive accuracy. Further validation using independent data would be required before using the index for operational decision-making.

## 5. Discussion and Retention Recommendations

The findings provide several practical insights for customer-retention planning.

### 5.1 Prioritize Inactive Customers with Higher Balances

The retained inactive high-balance group of 1,662 customers can be considered for targeted engagement initiatives.

Banks could evaluate personalized communication, account-service reviews, and relevant financial product information for this group. Such initiatives should be designed around customer needs rather than indiscriminate product promotion.

### 5.2 Improve Engagement Among Single-Product Customers

Customers using one product demonstrated a higher churn rate than customers using two products. Banks could investigate whether these customers have unmet financial requirements or limited awareness of available services.

Personalized product education and needs-based recommendations may help strengthen customer relationships. Any cross-selling initiative should prioritize suitability and customer benefit.

### 5.3 Monitor Customers with Low Engagement

The higher churn rate among inactive customers indicates that reduced engagement can serve as a useful signal for further investigation.

Financial institutions could consider periodic engagement reviews and voluntary customer feedback to understand reasons for inactivity. Additional transaction-level information would improve the ability to distinguish temporary inactivity from genuine disengagement.

### 5.4 Investigate Unusual High-Churn Product Groups

The three-product and four-product categories recorded unusually high churn rates. Since their sample sizes are relatively small, banks should investigate these groups separately before introducing broad retention policies.

Further analysis could examine customer characteristics, product combinations, service satisfaction, and account activity.

### 5.5 Adopt Evidence-Based Retention Monitoring

The engagement segments and RSI can provide a starting point for descriptive monitoring. Institutions should periodically evaluate these indicators against updated customer information.

Before deploying any risk-prioritization framework operationally, its stability, fairness, and effectiveness should be validated using additional data.

## 6. Limitations

The study has several limitations:

1. **Single-year dataset:** The dataset represents 2025 customer records and does not provide longitudinal information for establishing changes in retention over time.
2. **Limited engagement information:** Active membership is used as an engagement proxy. Transaction frequency, recency, and detailed service interactions are unavailable.
3. **Limited product information:** Product utilization is measured by the number of products rather than individual product types or combinations.
4. **Relative balance threshold:** The median balance is dataset-specific and should not be treated as a universal financial-value threshold.
5. **Small product groups:** The three-product and four-product groups contain relatively few observations, which limits the generalizability of their churn rates.
6. **Descriptive segmentation:** Risk categories and the RSI are based on business rules and are not trained predictive models.
7. **No causal inference:** Observed differences represent associations in the dataset and do not establish that a particular customer characteristic causes churn.

Future research could incorporate longitudinal customer records, transaction-level engagement information, customer feedback, and additional validation methods to improve retention analysis.

## 7. Conclusion

This study demonstrates how exploratory data analysis and business-rule-based segmentation can be used to examine customer engagement, product utilization, and churn patterns in a banking dataset.

The analysis identified an overall churn rate of 20.37% and showed that inactive customers experienced higher churn than active customers. Product utilization analysis revealed substantial differences between customers using one and two products, while the small three-product and four-product groups demonstrated unusually high churn rates requiring cautious interpretation.

The identification of 1,662 retained inactive customers with above-median balances provides a potential opportunity for targeted engagement initiatives. The Relationship Strength Index further summarizes selected customer relationship indicators and highlights differences between retained and exited customers.

Overall, the project illustrates the value of descriptive analytics in supporting customer-retention planning. The findings can help guide further investigation and the development of customer-focused strategies, provided that the limitations of the available data are considered.

## References

1. European Banking Customer Dataset (2025). Dataset provided for the project analysis. Original publisher and source documentation should be added here if available.
2. Pandas Development Team. *pandas: Python Data Analysis Library*. https://pandas.pydata.org/
3. NumPy Developers. *NumPy Documentation*. https://numpy.org/doc/
4. Streamlit, Inc. *Streamlit Documentation*. https://docs.streamlit.io/
5. Plotly Technologies Inc. *Plotly Python Documentation*. https://plotly.com/python/

---

**End of Research Paper**
