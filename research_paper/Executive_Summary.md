# Executive Summary
## Customer Engagement and Product Utilization Analytics for Retention Strategy

**Prepared by:** Devansh Sharma  
**Institution:** Unified Mentor  
**Project Domain:** Data Science and Banking Analytics

### 1. Project Overview

This project examines customer engagement, banking product utilization, and customer churn using a dataset containing 10,000 European banking customer records from 2025.

The objective is to identify customer groups with different retention patterns and develop data-driven recommendations that can support more targeted customer-engagement strategies.

The analysis uses Python-based exploratory data analysis, customer segmentation, product utilization analysis, financial analysis, and rule-based customer risk prioritization.

### 2. Key Findings

The analysis produced the following findings:

- **Overall churn rate:** 20.37% of customers in the dataset had exited.
- **Customer engagement:** Inactive customers had a churn rate of 26.85%, compared with 14.27% among active customers.
- **Product utilization:** Customers with one product had a churn rate of 27.71%, compared with 7.58% among customers with two products.
- **High-balance disengagement:** 2,456 customers were both inactive and had balances above the dataset median. Of these, 1,662 had not exited.
- **Customer relationship strength:** The average Relationship Strength Index (RSI) was 63.36 among retained customers and 55.18 among exited customers.

These findings indicate that customer activity and product utilization are useful dimensions for examining differences in retention patterns.

### 3. Priority Areas for Action

Based on the analytical results, the following areas deserve attention:

**A. Re-engagement of inactive customers**

Financial institutions could consider targeted communication and engagement initiatives for inactive customers, particularly those who maintain substantial account balances.

**B. Improving product engagement**

Customers using only one banking product could be offered relevant information about additional services based on their needs and eligibility. Product recommendations should prioritize suitability rather than simply increasing product count.

**C. Monitoring unusual product-utilization patterns**

Customers using three or four products showed high churn rates in this dataset. However, these groups contain relatively few observations, so further investigation is necessary before developing specific interventions.

**D. Data-driven customer monitoring**

Institutions could periodically monitor customer activity, product utilization, and account characteristics to identify changes in engagement and review retention strategies.

### 4. Recommended Implementation Approach

A practical implementation approach could include:

1. Establishing customer-engagement indicators using available account and activity data.
2. Identifying inactive customers and reviewing their retention risk.
3. Developing targeted engagement campaigns for relevant customer groups.
4. Monitoring campaign outcomes using retention and engagement indicators.
5. Periodically reviewing segmentation criteria to ensure that interventions remain relevant and effective.

### 5. Expected Benefits

If implemented and evaluated appropriately, these recommendations could help financial institutions:

- Identify customer groups requiring additional engagement.
- Improve the prioritization of retention initiatives.
- Understand relationships between product utilization and customer retention.
- Support more structured customer-monitoring processes.
- Make better use of available customer data in retention planning.

These are potential benefits, not outcomes demonstrated by the present analysis.

### 6. Limitations and Responsible Interpretation

The analysis is based on a cross-sectional dataset from 2025. It does not establish causal relationships or demonstrate changes in customer behaviour over time.

Customer activity is represented by an available activity indicator rather than detailed transaction frequency or recency. The customer risk categories and Relationship Strength Index are descriptive analytical tools, not validated predictive models.

The findings should therefore be treated as dataset-specific analytical evidence. Further validation using longitudinal customer records, transaction-level information, and real-world intervention outcomes would be necessary before operational or policy-level implementation.

### 7. Conclusion

This project demonstrates how exploratory data analysis and customer segmentation can help examine banking customer-retention patterns. The results highlight the importance of customer engagement and product utilization when identifying groups that may benefit from targeted retention initiatives.

The proposed recommendations provide a starting point for more structured, evidence-informed retention planning. Further validation and continuous monitoring are recommended before applying these approaches at institutional scale.
