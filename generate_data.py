"""
AML Synthetic Data Generator
Generates: Customers, Transactions tables (normalized, related via customer_id)
Designed so that a small % of customers have genuinely anomalous behavior
baked in -- this lets the SQL rule logic actually DETECT something real,
rather than visualizing pre-existing labels.
"""

import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

NUM_CUSTOMERS = 500
AVG_TXNS_PER_CUSTOMER = 4.6  # ~2000 transactions total

OCCUPATIONS = ["Salaried Employee", "Business Owner", "Self-Employed",
               "Retired", "Government Employee", "Student", "Homemaker"]
SOURCE_OF_FUNDS = ["Salary", "Business Income", "Savings", "Investment Returns",
                   "Inheritance", "Loan", "Rental Income"]
COUNTRIES_LOW_RISK = ["India", "USA", "UK", "Germany", "Canada", "Australia"]
COUNTRIES_HIGH_RISK = ["Cayman Islands", "Panama", "UAE", "Cyprus", "Malta"]
TXN_TYPES = ["Wire Transfer", "Cash Deposit", "Cash Withdrawal", "NEFT/RTGS", "Card Payment"]
TXN_MODE = ["Online", "Branch", "ATM", "Mobile App"]

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

def random_date():
    delta = END_DATE - START_DATE
    return START_DATE + timedelta(days=random.randint(0, delta.days))

# ---- Generate Customers ----
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    cust_id = f"CUST{i:05d}"
    is_pep = random.random() < 0.05  # 5% PEP
    # ~8% of customers are "seeded" as genuinely higher-risk profile
    is_seeded_risky = random.random() < 0.08
    customers.append({
        "customer_id": cust_id,
        "name": fake.name(),
        "age": random.randint(21, 75),
        "occupation": random.choice(OCCUPATIONS),
        "country": random.choice(COUNTRIES_LOW_RISK),
        "pep_status": "Yes" if is_pep else "No",
        "source_of_funds": random.choice(SOURCE_OF_FUNDS),
        "account_open_date": (random_date() - timedelta(days=random.randint(30, 1500))).date().isoformat(),
        "_seeded_risky": is_seeded_risky,  # internal flag, NOT exported to final dataset
    })

# ---- Generate Transactions ----
transactions = []
txn_counter = 1

for cust in customers:
    n_txns = max(1, int(random.gauss(AVG_TXNS_PER_CUSTOMER, 2)))

    # baseline "normal" amount for this customer (their typical transaction size)
    baseline_amount = random.randint(5000, 80000)

    for _ in range(n_txns):
        txn_id = f"TXN{txn_counter:06d}"
        txn_counter += 1

        beneficiary_country = random.choice(COUNTRIES_LOW_RISK)
        amount = int(random.gauss(baseline_amount, baseline_amount * 0.2))
        amount = max(1000, amount)

        # Inject anomalies for seeded-risky customers
        if cust["_seeded_risky"] and random.random() < 0.4:
            # spike: 5-15x their normal baseline
            amount = int(baseline_amount * random.uniform(5, 15))
            beneficiary_country = random.choice(COUNTRIES_HIGH_RISK)

        # occasionally, ANY customer can have a one-off high value txn (realistic noise)
        elif random.random() < 0.03:
            amount = int(baseline_amount * random.uniform(4, 8))

        transactions.append({
            "txn_id": txn_id,
            "customer_id": cust["customer_id"],
            "transaction_date": random_date().date().isoformat(),
            "transaction_type": random.choice(TXN_TYPES),
            "transaction_mode": random.choice(TXN_MODE),
            "amount": amount,
            "beneficiary_country": beneficiary_country,
        })

# strip internal-only field before export
for c in customers:
    del c["_seeded_risky"]

# ---- Write CSVs ----
import csv

with open("customers.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=customers[0].keys())
    writer.writeheader()
    writer.writerows(customers)

with open("transactions.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
    writer.writeheader()
    writer.writerows(transactions)

print(f"Generated {len(customers)} customers and {len(transactions)} transactions")
