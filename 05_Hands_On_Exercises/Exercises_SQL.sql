-- SQL Exercises for Databricks Learning
-- Start simple, progress to advanced
-- Run these in Databricks SQL editor or notebook

-- ============================================================================
-- SECTION 1: BASIC SQL - SELECT, FILTER, AGGREGATE
-- ============================================================================

-- Exercise 1.1: Simple SELECT
-- Create sample data and basic query
CREATE TABLE IF NOT EXISTS learning.basic.employees (
    emp_id INT,
    emp_name STRING,
    department STRING,
    salary INT,
    hire_date DATE
);

INSERT INTO learning.basic.employees VALUES
(1, 'Alice Johnson', 'Engineering', 120000, '2020-01-15'),
(2, 'Bob Smith', 'Sales', 95000, '2020-06-20'),
(3, 'Carol White', 'Engineering', 115000, '2021-03-10'),
(4, 'David Brown', 'HR', 85000, '2021-11-01'),
(5, 'Eve Davis', 'Sales', 98000, '2022-02-14');

-- TODO: Write query to select all employees
-- EXPECTED: 5 rows with all columns
SELECT * FROM learning.basic.employees;


-- Exercise 1.2: Filter with WHERE
-- TODO: Find employees in Engineering department
-- EXPECTED: 2 rows (Alice, Carol)
SELECT emp_name, department, salary 
FROM learning.basic.employees 
WHERE department = 'Engineering';


-- Exercise 1.3: Filter with multiple conditions
-- TODO: Find Engineering employees with salary > 115000
-- EXPECTED: 1 row (Alice)
SELECT emp_name, department, salary 
FROM learning.basic.employees 
WHERE department = 'Engineering' AND salary > 115000;


-- Exercise 1.4: ORDER BY
-- TODO: List employees sorted by salary descending
-- EXPECTED: Eve (98000), Bob (95000), David (85000), Carol (115000), Alice (120000)
SELECT emp_name, salary 
FROM learning.basic.employees 
ORDER BY salary DESC;


-- Exercise 1.5: COUNT aggregation
-- TODO: Count total employees
-- EXPECTED: 5
SELECT COUNT(*) as total_employees 
FROM learning.basic.employees;


-- Exercise 1.6: COUNT with GROUP BY
-- TODO: Count employees by department
-- EXPECTED: Engineering (2), Sales (2), HR (1)
SELECT department, COUNT(*) as emp_count 
FROM learning.basic.employees 
GROUP BY department
ORDER BY emp_count DESC;


-- Exercise 1.7: Multiple aggregations
-- TODO: Get department summary (count, avg salary, max salary)
-- EXPECTED: 3 rows with aggregations
SELECT 
    department,
    COUNT(*) as emp_count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary,
    MIN(salary) as min_salary
FROM learning.basic.employees 
GROUP BY department;


-- Exercise 1.8: HAVING clause
-- TODO: Find departments with more than 1 employee
-- EXPECTED: Engineering (2), Sales (2)
SELECT 
    department,
    COUNT(*) as emp_count
FROM learning.basic.employees 
GROUP BY department
HAVING COUNT(*) > 1;


-- ============================================================================
-- SECTION 2: INTERMEDIATE - JOINS, SUBQUERIES, CTEs
-- ============================================================================

-- Setup: Create related tables
CREATE TABLE IF NOT EXISTS learning.intermediate.departments (
    dept_id INT,
    dept_name STRING,
    manager STRING,
    budget INT
);

INSERT INTO learning.intermediate.departments VALUES
(1, 'Engineering', 'Frank Miller', 500000),
(2, 'Sales', 'Grace Lee', 300000),
(3, 'HR', 'Henry Zhang', 150000);

CREATE TABLE IF NOT EXISTS learning.intermediate.emp_dept (
    emp_id INT,
    dept_id INT,
    emp_name STRING,
    salary INT
);

INSERT INTO learning.intermediate.emp_dept VALUES
(1, 1, 'Alice', 120000),
(2, 2, 'Bob', 95000),
(3, 1, 'Carol', 115000),
(4, 3, 'David', 85000),
(5, 2, 'Eve', 98000);


-- Exercise 2.1: INNER JOIN
-- TODO: Join employees with departments
-- EXPECTED: 5 rows with employee and department info
SELECT 
    e.emp_name,
    d.dept_name,
    e.salary
FROM learning.intermediate.emp_dept e
INNER JOIN learning.intermediate.departments d
    ON e.dept_id = d.dept_id;


-- Exercise 2.2: LEFT JOIN
-- TODO: Show all departments with employees (if any)
-- EXPECTED: All departments listed with matching employees
SELECT 
    d.dept_name,
    COUNT(e.emp_id) as emp_count
FROM learning.intermediate.departments d
LEFT JOIN learning.intermediate.emp_dept e
    ON d.dept_id = e.dept_id
GROUP BY d.dept_name;


-- Exercise 2.3: Subquery in WHERE
-- TODO: Find employees with above-average salary
-- EXPECTED: Alice (120000), Carol (115000), Eve (98000)
SELECT emp_name, salary
FROM learning.intermediate.emp_dept
WHERE salary > (SELECT AVG(salary) FROM learning.intermediate.emp_dept);


-- Exercise 2.4: Subquery in FROM
-- TODO: Get high earners by department
-- EXPECTED: Top earner in each dept
SELECT 
    dept_name,
    max_earner,
    max_salary
FROM (
    SELECT 
        d.dept_name,
        e.emp_name as max_earner,
        e.salary as max_salary,
        ROW_NUMBER() OVER (PARTITION BY d.dept_id ORDER BY e.salary DESC) as rn
    FROM learning.intermediate.emp_dept e
    JOIN learning.intermediate.departments d ON e.dept_id = d.dept_id
)
WHERE rn = 1;


-- Exercise 2.5: Common Table Expression (CTE)
-- TODO: Use CTE to find departments over budget
-- EXPECTED: Compare department budget to total salaries
WITH dept_salary_summary AS (
    SELECT 
        d.dept_id,
        d.dept_name,
        d.budget,
        SUM(e.salary) as total_salary
    FROM learning.intermediate.departments d
    LEFT JOIN learning.intermediate.emp_dept e ON d.dept_id = e.dept_id
    GROUP BY d.dept_id, d.dept_name, d.budget
)
SELECT 
    dept_name,
    budget,
    total_salary,
    (budget - total_salary) as remaining_budget
FROM dept_salary_summary
ORDER BY remaining_budget;


-- Exercise 2.6: Multiple CTEs
-- TODO: Complex query with multiple CTEs
WITH emp_rank AS (
    SELECT 
        emp_name,
        salary,
        dept_id,
        RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) as salary_rank
    FROM learning.intermediate.emp_dept
),
high_earners AS (
    SELECT * FROM emp_rank WHERE salary_rank <= 2
)
SELECT 
    e.emp_name,
    d.dept_name,
    e.salary,
    e.salary_rank
FROM high_earners e
JOIN learning.intermediate.departments d ON e.dept_id = d.dept_id
ORDER BY d.dept_name;


-- ============================================================================
-- SECTION 3: ADVANCED - WINDOW FUNCTIONS, ADVANCED QUERIES
-- ============================================================================

-- Exercise 3.1: ROW_NUMBER with PARTITION
-- TODO: Rank employees by salary within each department
-- EXPECTED: Ranking restarts for each dept
SELECT 
    emp_name,
    salary,
    dept_id,
    ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) as dept_rank
FROM learning.intermediate.emp_dept
ORDER BY dept_id, dept_rank;


-- Exercise 3.2: RANK vs DENSE_RANK
-- TODO: Show difference between RANK and DENSE_RANK
-- Create sample data with duplicate salaries
WITH salary_data AS (
    SELECT 
        emp_name,
        salary,
        RANK() OVER (ORDER BY salary DESC) as rank_result,
        DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank_result
    FROM learning.intermediate.emp_dept
)
SELECT * FROM salary_data;


-- Exercise 3.3: Running total (SUM OVER)
-- TODO: Create running salary total for each department
-- EXPECTED: Cumulative salary by dept
SELECT 
    emp_name,
    dept_id,
    salary,
    SUM(salary) OVER (PARTITION BY dept_id ORDER BY emp_name) as running_total
FROM learning.intermediate.emp_dept
ORDER BY dept_id;


-- Exercise 3.4: LAG and LEAD
-- TODO: Show employee salary compared to next/previous
-- EXPECTED: Compare salaries within department
SELECT 
    emp_name,
    salary,
    LAG(salary) OVER (ORDER BY salary) as prev_salary,
    LEAD(salary) OVER (ORDER BY salary) as next_salary
FROM learning.intermediate.emp_dept
ORDER BY salary;


-- Exercise 3.5: PERCENT_RANK
-- TODO: Calculate percentile rank for employees
-- EXPECTED: Show where each employee ranks percentile-wise
SELECT 
    emp_name,
    salary,
    PERCENT_RANK() OVER (ORDER BY salary) as percentile_rank
FROM learning.intermediate.emp_dept
ORDER BY percentile_rank DESC;


-- ============================================================================
-- SECTION 4: DELTA LAKE OPERATIONS
-- ============================================================================

-- Exercise 4.1: Create Delta table from CSV
-- TODO: Create delta table and insert data
CREATE TABLE IF NOT EXISTS learning.delta.customers (
    customer_id INT,
    customer_name STRING,
    email STRING,
    created_date DATE
)
USING DELTA;

INSERT INTO learning.delta.customers VALUES
(1, 'Alice Customer', 'alice@example.com', '2024-01-01'),
(2, 'Bob Customer', 'bob@example.com', '2024-02-15');

-- View the table
SELECT * FROM learning.delta.customers;


-- Exercise 4.2: UPDATE operation
-- TODO: Update customer email
-- EXPECTED: Email changed for customer 1
UPDATE learning.delta.customers 
SET email = 'alice.new@example.com' 
WHERE customer_id = 1;

SELECT * FROM learning.delta.customers WHERE customer_id = 1;


-- Exercise 4.3: MERGE operation (Upsert)
-- TODO: Merge new customer data
-- EXPECTED: Update existing, insert new
MERGE INTO learning.delta.customers t
USING (
    SELECT 1 as customer_id, 'Alice Updated' as customer_name, 'alice.v2@example.com' as email, '2024-01-01' as created_date
    UNION ALL
    SELECT 3 as customer_id, 'Carol Customer' as customer_name, 'carol@example.com' as email, '2024-03-20' as created_date
) s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET 
    t.customer_name = s.customer_name,
    t.email = s.email
WHEN NOT MATCHED THEN INSERT *;

SELECT * FROM learning.delta.customers ORDER BY customer_id;


-- Exercise 4.4: DELETE operation
-- TODO: Delete a customer
-- EXPECTED: Customer 2 removed
DELETE FROM learning.delta.customers WHERE customer_id = 2;

SELECT COUNT(*) as remaining_customers FROM learning.delta.customers;


-- Exercise 4.5: Time Travel
-- TODO: Query previous versions
-- EXPECTED: See historical data
DESCRIBE HISTORY learning.delta.customers;

-- Query specific version (usually version 0 is oldest)
SELECT * FROM learning.delta.customers VERSION AS OF 0;


-- ============================================================================
-- SECTION 5: DATA QUALITY & VALIDATION
-- ============================================================================

-- Exercise 5.1: Find NULL values
-- TODO: Identify incomplete records
-- EXPECTED: Records with missing data
CREATE TABLE IF NOT EXISTS learning.quality.orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2)
);

INSERT INTO learning.quality.orders VALUES
(1, 1, '2024-01-01', 100.00),
(2, NULL, '2024-01-02', 200.00),
(3, 3, NULL, 150.00),
(4, 4, '2024-01-04', NULL),
(5, 5, '2024-01-05', 300.00);

-- Find orders with NULL values
SELECT * FROM learning.quality.orders WHERE customer_id IS NULL OR order_date IS NULL OR amount IS NULL;


-- Exercise 5.2: Find duplicates
-- TODO: Identify duplicate orders
-- EXPECTED: Count of duplicate customer orders
SELECT 
    customer_id,
    COUNT(*) as order_count
FROM learning.quality.orders
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- Exercise 5.3: Data type validation
-- TODO: Verify data types and value ranges
-- EXPECTED: Find invalid amounts
SELECT * FROM learning.quality.orders WHERE amount <= 0 OR amount > 10000;


-- Exercise 5.4: Completeness check
-- TODO: Calculate data completeness percentage
-- EXPECTED: % of non-null values per column
SELECT 
    'customer_id' as column_name,
    COUNT(CASE WHEN customer_id IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) as completeness_pct
FROM learning.quality.orders
UNION ALL
SELECT 
    'order_date' as column_name,
    COUNT(CASE WHEN order_date IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) as completeness_pct
FROM learning.quality.orders
UNION ALL
SELECT 
    'amount' as column_name,
    COUNT(CASE WHEN amount IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) as completeness_pct
FROM learning.quality.orders;


-- ============================================================================
-- SECTION 6: PRACTICAL BUSINESS QUERIES
-- ============================================================================

-- Exercise 6.1: Sales analysis
-- TODO: Top products by revenue
-- Create sample sales data
CREATE TABLE IF NOT EXISTS learning.business.sales (
    sale_id INT,
    product_name STRING,
    quantity INT,
    unit_price DECIMAL(10,2),
    sale_date DATE
);

INSERT INTO learning.business.sales VALUES
(1, 'Widget A', 10, 25.00, '2024-01-01'),
(2, 'Widget B', 5, 50.00, '2024-01-01'),
(3, 'Widget A', 15, 25.00, '2024-01-02'),
(4, 'Widget C', 8, 100.00, '2024-01-02'),
(5, 'Widget B', 3, 50.00, '2024-01-03');

-- Find total revenue by product
SELECT 
    product_name,
    SUM(quantity * unit_price) as total_revenue,
    COUNT(*) as transaction_count
FROM learning.business.sales
GROUP BY product_name
ORDER BY total_revenue DESC;


-- Exercise 6.2: Customer lifetime value
-- TODO: Calculate CLV for customers
CREATE TABLE IF NOT EXISTS learning.business.customer_orders (
    order_id INT,
    customer_id INT,
    order_total DECIMAL(10,2),
    order_date DATE
);

INSERT INTO learning.business.customer_orders VALUES
(1, 101, 100.00, '2024-01-01'),
(2, 101, 150.00, '2024-01-15'),
(3, 102, 200.00, '2024-01-05'),
(4, 101, 75.00, '2024-02-01'),
(5, 103, 250.00, '2024-01-20');

SELECT 
    customer_id,
    COUNT(*) as total_orders,
    SUM(order_total) as lifetime_value,
    AVG(order_total) as avg_order_value,
    MIN(order_date) as first_order,
    MAX(order_date) as last_order
FROM learning.business.customer_orders
GROUP BY customer_id
ORDER BY lifetime_value DESC;


-- Exercise 6.3: Monthly trends
-- TODO: Analyze monthly revenue trends
SELECT 
    TRUNC(order_date, 'MONTH') as month,
    COUNT(*) as order_count,
    SUM(order_total) as monthly_revenue,
    AVG(order_total) as avg_order_value
FROM learning.business.customer_orders
GROUP BY TRUNC(order_date, 'MONTH')
ORDER BY month;


-- ============================================================================
-- SECTION 7: PERFORMANCE & OPTIMIZATION
-- ============================================================================

-- Exercise 7.1: EXPLAIN to understand query plan
-- TODO: Analyze query execution plan
EXPLAIN SELECT 
    product_name,
    SUM(quantity * unit_price) as total_revenue
FROM learning.business.sales
WHERE sale_date >= '2024-01-01'
GROUP BY product_name;


-- Exercise 7.2: Partition pruning example
-- TODO: Create partitioned table and query efficiently
CREATE TABLE IF NOT EXISTS learning.performance.events (
    event_id INT,
    event_type STRING,
    event_timestamp TIMESTAMP,
    user_id INT
)
USING DELTA
PARTITIONED BY (event_date DATE);

-- When querying, always filter on partition column for efficiency
SELECT * FROM learning.performance.events 
WHERE event_date >= '2024-01-01' AND event_date < '2024-02-01'
LIMIT 100;


-- ============================================================================
-- CHALLENGES - Solutions not provided, try them yourself!
-- ============================================================================

-- Challenge 1: Complex aggregation
-- TODO: Find the department with the highest total salary
-- Write your own query here


-- Challenge 2: Multi-step transformation
-- TODO: For each customer, calculate:
--   - Total orders
--   - Total revenue
--   - Percentage of total company revenue
-- Write your own query here


-- Challenge 3: Ranking with ties
-- TODO: Rank products by revenue, showing ties correctly
-- Write your own query here


-- Challenge 4: Data reconciliation
-- TODO: Compare sales table with orders table
--   - Find orders not in sales
--   - Find sales not in orders
--   - Identify discrepancies
-- Write your own query here


-- Challenge 5: Year-over-year analysis
-- TODO: Compare 2023 vs 2024 sales by month
-- Write your own query here
