# SQL Cheatsheet for Data Engineering

## Table Management

### Create Tables
```sql
-- Create delta table with schema
CREATE TABLE catalog.schema.table_name (
    id INT NOT NULL,
    name STRING,
    amount DECIMAL(10,2),
    created_at TIMESTAMP
) USING DELTA;

-- Create table from query (CTAS)
CREATE TABLE catalog.schema.new_table AS
SELECT id, name, amount
FROM catalog.schema.source_table
WHERE amount > 0;

-- Create external table
CREATE EXTERNAL TABLE catalog.schema.ext_table
LOCATION 's3://bucket/path/'
USING DELTA;

-- Create temporary view
CREATE TEMP VIEW temp_view AS
SELECT * FROM catalog.schema.table_name
WHERE status = 'active';

-- Create or replace
CREATE OR REPLACE TABLE catalog.schema.table_name (
    id INT,
    name STRING
) USING DELTA;
```

### Alter Tables
```sql
-- Add column
ALTER TABLE table_name ADD COLUMN new_col STRING;

-- Drop column
ALTER TABLE table_name DROP COLUMN old_col;

-- Rename column
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;

-- Change column type
ALTER TABLE table_name ALTER COLUMN col_name TYPE DOUBLE;

-- Add/update table comment
COMMENT ON TABLE table_name IS 'Updated description';

-- Add column comment
COMMENT ON COLUMN table_name.column_name IS 'Column description';

-- Set table properties
ALTER TABLE table_name SET TBLPROPERTIES (
    'owner' = 'team@company.com',
    'refresh_frequency' = 'daily'
);
```

### Delete & Drop
```sql
-- Delete rows
DELETE FROM table_name WHERE id = 1;

-- Drop table (remove data)
DROP TABLE IF EXISTS table_name;

-- Truncate table (keep schema)
TRUNCATE TABLE table_name;

-- Drop external table (keep data)
DROP TABLE IF EXISTS table_name;
```

---

## Data Modification (DML)

### Insert
```sql
-- Insert single row
INSERT INTO table_name (col1, col2, col3)
VALUES (1, 'value', 100);

-- Insert multiple rows
INSERT INTO table_name VALUES
(1, 'val1', 100),
(2, 'val2', 200),
(3, 'val3', 300);

-- Insert from query
INSERT INTO table_name
SELECT id, name, amount * 1.1
FROM source_table
WHERE status = 'active';

-- Append data
INSERT INTO table_name
SELECT * FROM new_data;
```

### Update
```sql
-- Update specific rows
UPDATE table_name
SET amount = amount * 1.1
WHERE status = 'active';

-- Update multiple columns
UPDATE table_name
SET status = 'inactive', updated_at = current_timestamp()
WHERE last_activity < current_date() - INTERVAL 1 YEAR;

-- Update with join
UPDATE table_name t
SET t.category = s.new_category
FROM source_table s
WHERE t.id = s.id;
```

### Delete
```sql
-- Delete specific rows
DELETE FROM table_name
WHERE status = 'inactive';

-- Delete old data
DELETE FROM table_name
WHERE created_at < '2023-01-01';

-- Delete duplicates
DELETE FROM table_name
WHERE id NOT IN (
    SELECT MAX(id)
    FROM table_name
    GROUP BY unique_key
);
```

### Merge (Upsert)
```sql
-- Basic merge
MERGE INTO target_table t
USING source_table s
ON t.id = s.id
WHEN MATCHED THEN
    UPDATE SET t.amount = s.amount, t.updated_at = current_timestamp()
WHEN NOT MATCHED THEN
    INSERT (id, name, amount, updated_at) 
    VALUES (s.id, s.name, s.amount, current_timestamp());

-- Merge with conditions
MERGE INTO target_table t
USING source_table s
ON t.id = s.id AND t.version = s.version
WHEN MATCHED AND s.is_delete = true THEN
    DELETE
WHEN MATCHED AND s.is_delete = false THEN
    UPDATE SET t.* = s.*
WHEN NOT MATCHED AND s.is_delete = false THEN
    INSERT *;

-- Merge with multiple conditions
MERGE INTO inventory t
USING new_stock s
ON t.product_id = s.product_id AND t.warehouse_id = s.warehouse_id
WHEN MATCHED AND t.qty != s.qty THEN
    UPDATE SET t.qty = s.qty, t.last_updated = current_timestamp()
WHEN NOT MATCHED THEN
    INSERT VALUES (s.product_id, s.warehouse_id, s.qty, current_timestamp());
```

---

## Querying & Transformation

### SELECT Variations
```sql
-- Basic select
SELECT id, name, amount FROM table_name;

-- Select with aliases
SELECT 
    id AS customer_id,
    name AS customer_name,
    amount * 1.1 AS adjusted_amount
FROM table_name;

-- Select distinct
SELECT DISTINCT country FROM customers;

-- Select with LIMIT
SELECT * FROM table_name LIMIT 100;

-- Select with OFFSET
SELECT * FROM table_name LIMIT 10 OFFSET 20;
```

### Filtering
```sql
-- WHERE clause
SELECT * FROM table_name WHERE amount > 100;

-- Multiple conditions
SELECT * FROM table_name 
WHERE country = 'USA' AND status = 'active';

-- IN clause
SELECT * FROM table_name 
WHERE country IN ('USA', 'UK', 'Canada');

-- BETWEEN
SELECT * FROM table_name 
WHERE amount BETWEEN 100 AND 500;

-- Pattern matching
SELECT * FROM table_name 
WHERE name LIKE 'John%';

-- IS NULL
SELECT * FROM table_name WHERE email IS NULL;

-- IS NOT NULL
SELECT * FROM table_name WHERE email IS NOT NULL;
```

### Aggregations
```sql
-- Count
SELECT COUNT(*) as total_records FROM table_name;

-- Count distinct
SELECT COUNT(DISTINCT customer_id) as unique_customers FROM orders;

-- Sum
SELECT SUM(amount) as total_amount FROM orders;

-- Average
SELECT AVG(amount) as avg_amount FROM orders;

-- Min/Max
SELECT MIN(created_date), MAX(created_date) FROM orders;

-- Group by
SELECT 
    country,
    COUNT(*) as customer_count,
    SUM(amount) as total_spent,
    AVG(amount) as avg_spent
FROM customers
GROUP BY country;

-- Group by with HAVING
SELECT 
    category,
    COUNT(*) as product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 10;
```

### Joins
```sql
-- Inner join
SELECT a.id, a.name, b.order_id, b.amount
FROM customers a
INNER JOIN orders b ON a.id = b.customer_id;

-- Left join
SELECT a.*, b.order_id
FROM customers a
LEFT JOIN orders b ON a.id = b.customer_id;

-- Right join
SELECT a.*, b.order_id
FROM customers a
RIGHT JOIN orders b ON a.id = b.customer_id;

-- Full outer join
SELECT a.*, b.order_id
FROM customers a
FULL OUTER JOIN orders b ON a.id = b.customer_id;

-- Cross join (cartesian product)
SELECT * FROM t1 CROSS JOIN t2;

-- Self join
SELECT a.name, b.name
FROM employees a
JOIN employees b ON a.manager_id = b.id;

-- Multiple joins
SELECT a.id, a.name, b.order_id, c.product_name
FROM customers a
JOIN orders b ON a.id = b.customer_id
JOIN products c ON b.product_id = c.id;
```

### Window Functions
```sql
-- Row number
SELECT 
    id,
    name,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;

-- Rank
SELECT 
    id,
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;

-- Dense rank
SELECT 
    id,
    name,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;

-- Running total
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions
ORDER BY date;

-- Partition running total
SELECT 
    customer_id,
    date,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY date) as customer_running_total
FROM orders
ORDER BY customer_id, date;

-- Lead/lag
SELECT 
    date,
    amount,
    LAG(amount) OVER (ORDER BY date) as previous_amount,
    LEAD(amount) OVER (ORDER BY date) as next_amount
FROM sales;

-- Percent rank
SELECT 
    id,
    score,
    PERCENT_RANK() OVER (ORDER BY score) as percentile
FROM test_results;
```

### Set Operations
```sql
-- UNION (distinct)
SELECT id, name FROM table1
UNION
SELECT id, name FROM table2;

-- UNION ALL
SELECT id, name FROM table1
UNION ALL
SELECT id, name FROM table2;

-- INTERSECT
SELECT id FROM table1
INTERSECT
SELECT id FROM table2;

-- EXCEPT
SELECT id FROM table1
EXCEPT
SELECT id FROM table2;
```

### Common Table Expressions (CTEs)
```sql
-- Single CTE
WITH customer_summary AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(amount) as total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT * FROM customer_summary
WHERE total_spent > 1000;

-- Multiple CTEs
WITH 
customer_orders AS (
    SELECT customer_id, COUNT(*) as order_count
    FROM orders
    GROUP BY customer_id
),
customer_revenue AS (
    SELECT customer_id, SUM(amount) as total_revenue
    FROM orders
    GROUP BY customer_id
)
SELECT 
    c.customer_id,
    o.order_count,
    r.total_revenue
FROM customers c
LEFT JOIN customer_orders o ON c.id = o.customer_id
LEFT JOIN customer_revenue r ON c.id = r.customer_id;

-- Recursive CTE
WITH RECURSIVE number_series AS (
    SELECT 1 as num
    UNION ALL
    SELECT num + 1
    FROM number_series
    WHERE num < 100
)
SELECT * FROM number_series;
```

---

## String Functions

```sql
SELECT
    SUBSTRING(name, 1, 5) as first_5,
    LENGTH(name) as name_length,
    UPPER(name) as uppercase,
    LOWER(name) as lowercase,
    TRIM(name) as trimmed,
    LTRIM(name) as left_trim,
    RTRIM(name) as right_trim,
    CONCAT(first_name, ' ', last_name) as full_name,
    SPLIT(email, '@')[0] as email_username,
    REPLACE(phone, '-', '') as phone_no_dash,
    INSTR(email, '@') as at_position,
    LIKE_MATCH(name, 'John%') as starts_with_john
FROM users;
```

---

## Date Functions

```sql
SELECT
    CURRENT_DATE as today,
    CURRENT_TIMESTAMP as now,
    DATE_ADD(created_date, 30) as future_date,
    DATE_SUB(created_date, 7) as past_date,
    DATEDIFF(CURRENT_DATE, created_date) as days_ago,
    DATE_FORMAT(created_date, 'yyyy-MM-dd') as formatted_date,
    YEAR(created_date) as year,
    MONTH(created_date) as month,
    DAYOFWEEK(created_date) as day_of_week,
    LAST_DAY(created_date) as last_day_of_month,
    DATE_TRUNC('month', created_date) as month_start
FROM orders;
```

---

## Mathematical Functions

```sql
SELECT
    ABS(-10) as absolute,
    ROUND(3.14159, 2) as rounded,
    CEIL(3.14) as ceiling,
    FLOOR(3.99) as floor,
    POWER(2, 8) as power,
    SQRT(16) as square_root,
    MOD(10, 3) as modulo,
    GREATEST(1, 5, 3) as max_val,
    LEAST(1, 5, 3) as min_val
FROM numbers;
```

---

## Conditional Functions

```sql
-- CASE expression
SELECT 
    name,
    CASE 
        WHEN amount >= 1000 THEN 'VIP'
        WHEN amount >= 500 THEN 'Gold'
        WHEN amount >= 100 THEN 'Silver'
        ELSE 'Bronze'
    END as customer_tier
FROM customers;

-- IF function
SELECT 
    name,
    IF(status = 'active', 'Active', 'Inactive') as status_label
FROM users;

-- COALESCE (returns first non-null)
SELECT 
    COALESCE(phone, email, 'No contact info') as contact_info
FROM users;

-- NULLIF
SELECT 
    name,
    NULLIF(previous_amount, current_amount) as change_if_different
FROM accounts;
```

---

## Type Conversions

```sql
SELECT
    CAST(amount AS INT) as amount_int,
    CAST(created_date AS STRING) as date_string,
    amount::DOUBLE as amount_double,  -- Alternative syntax
    TO_DATE('2024-04-15') as parsed_date,
    TO_TIMESTAMP('2024-04-15 10:30:00') as parsed_timestamp
FROM transactions;
```

---

## Delta Lake Specific

### Time Travel
```sql
-- Query specific version
SELECT * FROM table_name VERSION AS OF 5;

-- Query at timestamp
SELECT * FROM table_name TIMESTAMP AS OF '2024-04-15 10:00:00';

-- Show history
DESCRIBE HISTORY table_name LIMIT 10;

-- Show details
DESCRIBE DETAIL table_name;
```

### Optimization
```sql
-- Optimize table (consolidate files)
OPTIMIZE table_name;

-- Optimize with Z-order
OPTIMIZE table_name ZORDER BY (date_column, category_column);

-- Compact small files
OPTIMIZE table_name WHERE year = 2024;
```

### Vacuum (Clean up old versions)
```sql
-- Default: keep 7 days
VACUUM table_name;

-- Keep 30 days
VACUUM table_name RETAIN 30 DAYS;

-- Keep 1 day
VACUUM table_name RETAIN 1 DAYS;
```

---

## Performance Tips

### Use Partition Pruning
```sql
-- ✅ GOOD: Uses partitions efficiently
SELECT * FROM sales 
WHERE date >= '2024-01-01' AND date < '2024-02-01';

-- ❌ BAD: Scans all partitions
SELECT * FROM sales 
WHERE YEAR(date) = 2024;
```

### Use Broadcast Joins
```sql
-- ✅ GOOD: Broadcast small table
SELECT /*+ BROADCAST(small_table) */ *
FROM large_table
JOIN small_table ON large_table.id = small_table.id;
```

### Push Down Filters
```sql
-- ✅ GOOD: Filter early
SELECT * FROM (
    SELECT * FROM raw_data WHERE date >= '2024-01-01'
) t
JOIN reference ON t.id = reference.id;

-- ❌ BAD: Filter late
SELECT * FROM raw_data
JOIN reference ON raw_data.id = reference.id
WHERE date >= '2024-01-01';
```

---

## Common Data Engineering Queries

### Find Duplicates
```sql
SELECT id, COUNT(*) as duplicate_count
FROM table_name
GROUP BY id
HAVING COUNT(*) > 1;
```

### Remove Duplicates (Keep Latest)
```sql
DELETE FROM table_name
WHERE (id, created_at) NOT IN (
    SELECT id, MAX(created_at)
    FROM table_name
    GROUP BY id
);
```

### Find Null Percentages
```sql
SELECT 
    'column1' as column_name,
    COUNT(CASE WHEN column1 IS NULL THEN 1 END) * 100.0 / COUNT(*) as null_percent
FROM table_name
UNION ALL
SELECT 
    'column2' as column_name,
    COUNT(CASE WHEN column2 IS NULL THEN 1 END) * 100.0 / COUNT(*) as null_percent
FROM table_name;
```

### Data Quality Check
```sql
SELECT 
    table_name,
    COUNT(*) as total_records,
    COUNT(DISTINCT id) as unique_ids,
    COUNT(CASE WHEN email IS NULL THEN 1 END) as null_emails,
    MIN(created_date) as earliest_record,
    MAX(created_date) as latest_record
FROM table_name
GROUP BY table_name;
```
