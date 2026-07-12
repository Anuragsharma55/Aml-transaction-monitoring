-- ============================================================
-- Run 01_schema.sql first, then this, then 02_flagging_logic.sql
-- Adjust the file path to wherever you place customers.csv / transactions.csv
-- If LOCAL INFILE is disabled on your MySQL instance, use MySQL Workbench's
-- Table Data Import Wizard instead (right-click table > Table Data Import Wizard)
-- ============================================================

USE aml_monitoring;

LOAD DATA LOCAL INFILE 'customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'transactions.csv'
INTO TABLE transactions
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Sanity check
SELECT COUNT(*) AS customer_count FROM customers;
SELECT COUNT(*) AS transaction_count FROM transactions;
