# Methodology — Risk Scoring Logic

This document explains exactly how each customer's risk score and level are derived, so the logic is auditable and defensible in review.

## Step 1: Transaction-Level Flags (`transaction_flags` view)

Each transaction is evaluated independently against three rules:

| Flag | Logic |
|---|---|
| `flag_amount_outlier` | Transaction amount exceeds the customer's own average + 3 standard deviations (or 4x average if the customer has too few transactions for a stable standard deviation) |
| `flag_high_risk_country` | Beneficiary country is in the high-risk jurisdiction reference list (Cayman Islands, Panama, UAE, Cyprus, Malta) |
| `flag_large_value` | Transaction amount exceeds a flat regulatory-style threshold (₹500,000) |

**Why baseline-relative, not a fixed global threshold?** A ₹2,00,000 transaction is unremarkable for a business owner who regularly moves large sums, but highly anomalous for a customer whose typical transaction is ₹10,000. Comparing against the customer's own pattern catches behavior change, which is the actual signal AML monitoring cares about.

## Step 2: Customer-Level Risk Score (`customer_risk_scores` view)

Each customer's flags are aggregated and weighted:

```
risk_score =
    (30 if PEP status = Yes else 0)
  + MIN(outlier_transaction_count × 15, 45)
  + MIN(high_risk_country_transaction_count × 20, 60)
  + MIN(large_value_transaction_count × 10, 30)
```

Weights are capped (via `LEAST`/`MIN`) so a single customer with many small flags doesn't runaway to an artificially extreme score — this keeps scoring proportionate.

## Step 3: Risk Level & Alert Reason (`customer_risk_summary` view)

```
risk_level:
    >= 50  → High
    >= 20  → Medium
    else   → Low

alert_reason (first matching condition wins):
    PEP + high-risk country transaction  → "PEP + High-Risk Corridor"
    high-risk country transaction only   → "High-Risk Jurisdiction Transfer"
    amount outlier                       → "Transaction Value Spike vs. Baseline"
    large value transaction              → "Large Value Transaction"
    none of the above                    → "No Alert"
```

## Why Not Machine Learning?

This project intentionally uses documented, rule-based statistical detection rather than ML classification. In real AML compliance contexts, rule-based systems are preferred specifically because:
- Every flag can be explained to a regulator or auditor in plain language
- Thresholds can be adjusted transparently as policy changes
- There's no "black box" risk of a model making an undefendable decision

This mirrors how many production AML/KYC monitoring systems are actually built.
