# Unity Catalog & Data Governance Cheatsheet

## Unity Catalog Architecture

### Namespace Hierarchy
```
Metastore (1 per region)
├── Catalog (ex: prod_analytics)
│   ├── Schema (ex: customer_data)
│   │   ├── Table
│   │   ├── View
│   │   └── Volume
│   └── Schema (ex: sales_data)
│       └── Table
└── Catalog (ex: dev_analytics)
```

---

## Creating Unity Catalog Objects

### Create Catalog
```sql
-- Create catalog
CREATE CATALOG IF NOT EXISTS prod_analytics
COMMENT "Production analytics catalog";

-- Switch to catalog
USE CATALOG prod_analytics;

-- Show all catalogs
SHOW CATALOGS;

-- Describe catalog
DESCRIBE CATALOG prod_analytics;
```

### Create Schema
```sql
-- Create schema
CREATE SCHEMA IF NOT EXISTS customer_data
COMMENT "Customer master and transactional data";

-- Create schema with properties
CREATE SCHEMA IF NOT EXISTS sales_data
COMMENT "Sales and order data"
WITH DBPROPERTIES ('team' = 'sales', 'owner' = 'john@company.com');

-- Switch schema
USE SCHEMA prod_analytics.customer_data;

-- Show schemas
SHOW SCHEMAS;
```

### Create Tables in Unity Catalog
```sql
-- Create managed table (stored in UC volume)
CREATE TABLE prod_analytics.customer_data.customers (
    customer_id INT NOT NULL,
    name STRING NOT NULL,
    email STRING,
    country STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
USING DELTA
COMMENT "Customer master table"
TBLPROPERTIES (
    'delta.enableChangeDataFeed' = 'true',
    'owner' = 'data-team@company.com'
);

-- Create external table (data in cloud storage)
CREATE TABLE IF NOT EXISTS prod_analytics.sales_data.orders
USING DELTA
LOCATION 's3://my-bucket/data/orders/'
COMMENT "External order data";

-- Create table from query
CREATE TABLE prod_analytics.customer_data.customer_summary AS
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(total) as lifetime_value
FROM prod_analytics.sales_data.orders
GROUP BY customer_id;
```

### Create Views
```sql
-- Create view
CREATE VIEW prod_analytics.customer_data.vw_active_customers AS
SELECT customer_id, name, email
FROM prod_analytics.customer_data.customers
WHERE created_at > current_timestamp() - INTERVAL 1 YEAR;

-- Create materialized view (for faster queries)
CREATE MATERIALIZED VIEW prod_analytics.customer_data.mv_customer_metrics AS
SELECT 
    customer_id,
    COUNT(*) as total_orders,
    SUM(amount) as total_spent
FROM prod_analytics.sales_data.orders
GROUP BY customer_id;

-- Refresh materialized view
ALTER MATERIALIZED VIEW prod_analytics.customer_data.mv_customer_metrics REFRESH;
```

---

## Access Control & Permissions

### Grant Permissions (Object Level)

```sql
-- Grant on catalog
GRANT USAGE ON CATALOG prod_analytics TO `data-team@company.com`;

-- Grant on schema
GRANT CREATE, USAGE ON SCHEMA prod_analytics.customer_data TO `john@company.com`;

-- Grant on table
GRANT SELECT, MODIFY ON TABLE prod_analytics.customer_data.customers TO `analyst@company.com`;

-- Grant with column selection
GRANT SELECT ON COLUMN prod_analytics.customer_data.customers.email TO `external-partner@company.com`;

-- Revoke permissions
REVOKE SELECT ON TABLE prod_analytics.customer_data.customers FROM `user@company.com`;
```

### View Permissions
```sql
-- Check grants on object
SHOW GRANTS ON TABLE prod_analytics.customer_data.customers;

-- Check grants for principal
SHOW GRANTS ON SCHEMA prod_analytics.customer_data TO `john@company.com`;
```

### Row & Column Level Security

```sql
-- Create row filter (who can see which rows)
CREATE FUNCTION prod_analytics.customer_data.fn_row_filter(user STRING)
RETURNS BOOLEAN
RETURN current_user() = 'admin@company.com' OR user = current_user();

-- Apply row filter to table
ALTER TABLE prod_analytics.customer_data.customers
SET ROW FILTER fn_row_filter(email) ON (email);

-- Create column mask (hide sensitive data)
CREATE FUNCTION prod_analytics.customer_data.fn_mask_email(email STRING)
RETURNS STRING
RETURN CASE
    WHEN is_account_group_member('data-team') THEN email
    ELSE CONCAT(SUBSTRING(email, 1, 2), '***@company.com')
END;

-- Apply mask
ALTER TABLE prod_analytics.customer_data.customers
ALTER COLUMN email SET MASK fn_mask_email(email);
```

---

## Tagging & Classification

### Add Tags to Objects
```sql
-- Create tag (enum type)
CREATE TAG prod_analytics.data_level VALUES ('bronze', 'silver', 'gold');

-- Assign tag to table
ALTER TABLE prod_analytics.customer_data.customers SET TAG data_level = 'silver';

-- Assign tag to column
ALTER TABLE prod_analytics.customer_data.customers ALTER COLUMN email SET TAG pii = 'sensitive';

-- Create PII tag
CREATE TAG prod_analytics.pii_classification VALUES ('public', 'internal', 'confidential');

-- View tags on object
SELECT * FROM table_property_view WHERE table_name = 'customers';
```

### Sensitive Data Management
```sql
-- Create sensitive data tag
CREATE TAG prod_analytics.data_sensitivity VALUES ('public', 'internal', 'confidential', 'restricted');

-- Mark PII columns
ALTER TABLE prod_analytics.customer_data.customers ALTER COLUMN email SET TAG data_sensitivity = 'confidential';
ALTER TABLE prod_analytics.customer_data.customers ALTER COLUMN phone SET TAG data_sensitivity = 'confidential';
ALTER TABLE prod_analytics.customer_data.customers ALTER COLUMN ssn SET TAG data_sensitivity = 'restricted';

-- Query for sensitive columns
SELECT 
    catalog_name, schema_name, table_name, column_name, tags
FROM system.information_schema.column_lineage
WHERE tags LIKE '%sensitive%';
```

---

## Metadata & Lineage

### Set Table Comments & Properties
```sql
-- Add/update comment
COMMENT ON TABLE prod_analytics.customer_data.customers 
IS 'Master table containing all customer information. Updated daily from source system.';

-- Add column comments
COMMENT ON COLUMN prod_analytics.customer_data.customers.customer_id 
IS 'Unique identifier for customer (PK)';

COMMENT ON COLUMN prod_analytics.customer_data.customers.email 
IS 'Customer email - PII data, restricted access';

-- Set table properties
ALTER TABLE prod_analytics.customer_data.customers
SET TBLPROPERTIES (
    'owner' = 'data-team@company.com',
    'sla' = '99.9%',
    'refresh_frequency' = 'daily',
    'pii_data' = 'yes'
);
```

### Query Lineage
```sql
-- Get table lineage (input tables)
SELECT * FROM system.access.table_lineage
WHERE table_name = 'customer_summary';

-- Get column lineage
SELECT * FROM system.access.column_lineage
WHERE to_table = 'customer_summary';

-- Search lineage
SELECT * FROM system.access.table_lineage
WHERE from_table IN ('customers', 'orders');
```

### Data Quality Expectations
```sql
-- Create expectations table
CREATE TABLE prod_analytics.quality.expectations (
    table_name STRING,
    column_name STRING,
    expectation_type STRING,
    expectation_value STRING,
    created_at TIMESTAMP
);

-- Example expectations
INSERT INTO prod_analytics.quality.expectations VALUES
('customers', 'customer_id', 'not_null', 'true', current_timestamp()),
('customers', 'email', 'not_null', 'true', current_timestamp()),
('customers', 'email', 'unique', 'true', current_timestamp()),
('orders', 'amount', 'numeric_range', '0,999999', current_timestamp());
```

---

## Volume Management

### Create & Manage Volumes
```sql
-- Create external volume (UC volume backed by S3)
CREATE VOLUME prod_analytics.customer_data.raw_data_volume;

-- Create volume with specific path
CREATE VOLUME IF NOT EXISTS prod_analytics.customer_data.external_volume
LOCATION 's3://my-bucket/volumes/data/';

-- List volumes
SHOW VOLUMES;

-- Get volume details
DESCRIBE VOLUME prod_analytics.customer_data.raw_data_volume;

-- Grant access to volume
GRANT READ ON VOLUME prod_analytics.customer_data.raw_data_volume TO `analyst@company.com`;
```

### Work with Volumes
```python
# In PySpark
# Read from volume
df = spark.read.format("parquet").load("/Volumes/prod_analytics/customer_data/raw_data_volume/parquet_files/")

# Write to volume
df.write.format("delta").mode("overwrite").save("/Volumes/prod_analytics/customer_data/raw_data_volume/processed_data/")

# List volume contents
dbutils.fs.ls("/Volumes/prod_analytics/customer_data/raw_data_volume/")
```

---

## Unity Catalog Best Practices

### Naming Conventions
```sql
-- Catalog: descriptive, lowercase, underscore-separated
-- Good: prod_analytics, dev_warehouse, hr_operations
-- Bad: prodAnalytics, PA, analytics

-- Schema: function-based grouping
-- Good: customer_data, sales_metrics, hr_records
-- Bad: schema1, data, temp

-- Table naming: entity_state pattern
-- Good: customers_silver, orders_gold, product_master_bronze
-- Bad: cust, o, tab1

-- Column naming: lowercase, descriptive
-- Good: customer_id, order_created_date, total_amount
-- Bad: id, date, amt
```

### Catalog Structure Example
```sql
-- Multi-tenant structure
prod_analytics/
├── customer_data/
│   ├── customers_bronze
│   ├── customers_silver
│   ├── customers_gold
│   └── vw_active_customers
├── sales_data/
│   ├── orders_bronze
│   ├── orders_silver
│   ├── orders_gold
│   └── mv_sales_metrics
└── quality/
    ├── data_quality_results
    └── expectations
```

---

## Audit & Compliance

### Query Audit Logs
```sql
-- View audit logs
SELECT 
    timestamp,
    user_identity.email as user,
    action_type,
    request_params,
    response.result
FROM system.access.audit
WHERE object_type = 'TABLE'
ORDER BY timestamp DESC
LIMIT 100;

-- Find who accessed sensitive data
SELECT 
    timestamp,
    user_identity.email as user,
    action_type
FROM system.access.audit
WHERE full_name_arg LIKE '%confidential%'
ORDER BY timestamp DESC;

-- Compliance report
SELECT 
    object_name,
    object_type,
    created_by,
    created_at,
    modified_by,
    modified_at
FROM system.access.objects_audit
WHERE object_type = 'TABLE'
ORDER BY created_at DESC;
```

### Create Compliance Rules
```sql
-- Require comments on new tables
-- (Enforced via policies/workspace rules)

-- Require PII tags
-- (Enforced via governance)

-- Document lineage
-- (Tracked in system.access.table_lineage)
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| **RESOURCE_NOT_FOUND** | Object doesn't exist | Check object path: `catalog.schema.table` |
| **PERMISSION_DENIED** | No access to object | Ask workspace admin to grant permissions |
| **INVALID_TABLE_NAME** | Missing catalog/schema | Use full path: `catalog.schema.table` |
| **OBJECT_ALREADY_EXISTS** | Table/schema already created | Use `IF NOT EXISTS` or drop first |
| **EXTERNAL_LOCATION_INVALID** | Bad S3/ADLS path | Verify cloud storage credentials |
