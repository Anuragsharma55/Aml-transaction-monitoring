# AML Transaction Monitoring & Customer Risk Scoring Dashboard

A rule-based transaction monitoring system that flags customers for AML (Anti-Money Laundering) review by scoring behavior against their own historical baseline — not against pre-labeled or static thresholds.

---

## Problem Statement

Financial institutions process thousands of customer transactions daily and are regulatorily required to identify potentially suspicious activity — unusual transaction sizes, high-risk jurisdiction exposure, and politically exposed person (PEP) involvement — before it escalates into compliance risk.

Manually reviewing every transaction is not scalable. Compliance and Governance Monitoring teams need a system that:
1. **Flags anomalies automatically** based on a customer's own transaction behavior, not arbitrary fixed thresholds
2. **Scores and ranks customers by risk level** so analysts prioritize the highest-risk cases first
3. **Surfaces the "why"** behind each flag (jurisdiction exposure, value spike, PEP status) so it's auditable and defensible
4. **Visualizes the result** for both a quick executive view and detailed case-by-case drill-down

This project builds that pipeline end-to-end: synthetic transaction data → SQL-based rule detection → Power BI dashboard.

---

## What This Project Does

- Generates a realistic synthetic dataset of 500 customers and ~2,000 transactions, with a small percentage of customers carrying genuinely anomalous behavior (transaction spikes, high-risk jurisdiction transfers)
- Computes a **risk score per customer** using SQL, based on:
  - Deviation from the customer's own historical transaction average (statistical outlier detection, 3-standard-deviation threshold)
  - Exposure to high-risk jurisdictions (Cayman Islands, Panama, UAE, Cyprus, Malta)
  - PEP (Politically Exposed Person) status
  - Large absolute transaction values
- Buckets customers into **High / Medium / Low risk** based on a weighted, documented score — not a black box, and not machine learning
- Surfaces an **alert reason** per customer (e.g. "PEP + High-Risk Corridor", "Transaction Value Spike vs. Baseline")
- Visualizes all of it across a 5-page Power BI dashboard

**Note on scope:** this project deliberately uses rule-based statistical detection, not machine learning, to keep the logic auditable and interview-defensible — real AML monitoring systems rely heavily on documented, explainable rules for exactly this reason.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data generation | Python (pandas, Faker) |
| Data storage & rule logic | MySQL |
| Visualization | Power BI (Power Query, DAX) |

---
## How to Run

1. **Generate data** (already included, or regenerate):
   ```
   pip install faker
   python data/generate_data.py
   ```
2. **Set up MySQL:**
   ```sql
   -- run in this order
   source sql/01_schema.sql;
   source sql/00_load_data.sql;   -- or use MySQL Workbench's Table Data Import Wizard
   source sql/02_flagging_logic.sql;
   ```
3. **Validate the output:**
   ```sql
   SELECT risk_level, COUNT(*) FROM aml_monitoring.customer_risk_summary GROUP BY risk_level;
   ```
4. **Open the Power BI file**, refresh the data source to point at your local MySQL instance, done.

---

## Sample Output

Validated risk distribution on the included synthetic dataset (500 customers):

| Risk Level | Customers |
|---|---|
| Low | 447 |
| Medium | 40 |
| High | 13 |

This funnel shape — mostly low-risk, with a small escalating tail — mirrors what's expected in a real AML monitoring population.

---

## Dashboard Pages

1. **Executive Summary** — (https://raw.githubusercontent.com/Anuragsharma55/Aml-transaction-monitoring/b73cf0795a903c5bf3bc9d637f1691b5d0231c69/page1_executive_summary.png)
2. **Risk Analysis** — (https://github.com/Anuragsharma55/Aml-transaction-monitoring/blob/main/page2_risk_analysis.png)
3. **Transaction Analysis** —(https://github.com/Anuragsharma55/Aml-transaction-monitoring/blob/cce59f62100fe6f47d4778175139fdab20cf881f/page3_transaction_analysis.png)
4. **Geographic & Behavioral Risk** —(https://github.com/Anuragsharma55/Aml-transaction-monitoring/blob/fb2922bc3946e8cbfcce3ef6adf109ca55c08f6a/page4_geographic_risk.png)
5. **Customer Details** —(https://github.com/Anuragsharma55/Aml-transaction-monitoring/blob/ddd65b9c140c6fa72883949fb9489263cf437160/page5_customer_details.png)

---

## Author

Anurag Sharma — [GitHub](https://github.com/Anuragsharma55)
