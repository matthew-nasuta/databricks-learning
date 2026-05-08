# Databricks Hands-On Labs

## Lab 1: Delta Lake Fundamentals (1-2 hours)

### Objective
Learn Delta Lake basics: creating tables, time travel, ACID operations, schema evolution.

### Prerequisites
- Databricks workspace access
- All-purpose cluster created
- Basic SQL knowledge

### Instructions

#### Step 1: Create Bronze Table
```sql
-- Lab 1: Create raw customer data in bronze
CREATE TABLE IF NOT EXISTS lab_workspace.bronze.customers_raw (
    customer_id INT,
    name STRING,
    email STRING,
    created_date DATE
)
USING DELTA;

-- Insert sample data
INSERT INTO lab_workspace.bronze.customers_raw VALUES
(1, 'Alice Johnson', 'alice@email.com', '2024-01-15'),
(2, 'Bob Smith', 'bob@email.com', '2024-02-20'),
(3, 'Carol White', 'carol@email.com', '2024-03-10');

-- Verify data
SELECT * FROM lab_workspace.bronze.customers_raw;
```

#### Step 2: Explore Delta Log
```sql
-- View table history (time travel)
DESCRIBE HISTORY lab_workspace.bronze.customers_raw;

-- Query data from specific version
SELECT * FROM lab_workspace.bronze.customers_raw VERSION AS OF 0;

-- Query data from timestamp
SELECT * FROM lab_workspace.bronze.customers_raw 
TIMESTAMP AS OF '2024-01-15 10:00:00';
```

#### Step 3: ACID Operations
```sql
-- UPDATE operation
UPDATE lab_workspace.bronze.customers_raw 
SET email = 'alice.johnson@newdomain.com' 
WHERE customer_id = 1;

-- DELETE operation
DELETE FROM lab_workspace.bronze.customers_raw 
WHERE customer_id = 3;

-- MERGE (upsert)
MERGE INTO lab_workspace.bronze.customers_raw t
USING (
    SELECT 4 as customer_id, 'David Lee' as name, 'david@email.com' as email, '2024-04-01' as created_date
) s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET t.email = s.email
WHEN NOT MATCHED THEN INSERT *;

-- Check history again
DESCRIBE HISTORY lab_workspace.bronze.customers_raw;
```

#### Step 4: Schema Evolution
```sql
-- Add new column
ALTER TABLE lab_workspace.bronze.customers_raw 
ADD COLUMN phone STRING;

-- Update the new column
UPDATE lab_workspace.bronze.customers_raw 
SET phone = '555-1234' 
WHERE customer_id = 1;

-- Verify schema change
DESCRIBE DETAIL lab_workspace.bronze.customers_raw;
```

#### Step 5: Restore Previous Version
```sql
-- Restore to version 1
RESTORE TABLE lab_workspace.bronze.customers_raw TO VERSION AS OF 1;

-- Verify data is restored
SELECT * FROM lab_workspace.bronze.customers_raw;
```

### Lab Deliverable
- Screenshot of DESCRIBE HISTORY output showing at least 5 versions
- SQL queries demonstrating UPDATE, DELETE, MERGE
- Evidence of schema evolution

---

## Lab 2: Unity Catalog & Data Governance (2-3 hours)

### Objective
Set up Unity Catalog, organize data with proper structure, apply access controls, and track lineage.

### Prerequisites
- Lab 1 completed
- Unity Catalog enabled in workspace
- Admin permissions

### Instructions

#### Step 1: Create Catalog Structure
```sql
-- Create catalogs
CREATE CATALOG IF NOT EXISTS dev_analytics
COMMENT "Development analytics catalog";

CREATE CATALOG IF NOT EXISTS prod_analytics
COMMENT "Production analytics catalog";

-- Switch to prod catalog
USE CATALOG prod_analytics;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS bronze
COMMENT "Raw ingested data";

CREATE SCHEMA IF NOT EXISTS silver
COMMENT "Cleaned and validated data";

CREATE SCHEMA IF NOT EXISTS gold
COMMENT "Business-ready analytics data";

-- Verify structure
SHOW CATALOGS;
SHOW SCHEMAS IN prod_analytics;
```

#### Step 2: Create Managed Tables
```sql
USE CATALOG prod_analytics;
USE SCHEMA bronze;

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT NOT NULL,
    name STRING NOT NULL,
    email STRING,
    country STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
USING DELTA
COMMENT "Customer master table from source system"
TBLPROPERTIES (
    'owner' = 'data-engineering@company.com',
    'environment' = 'production',
    'refresh_frequency' = 'daily'
);

-- Load sample data
INSERT INTO prod_analytics.bronze.customers VALUES
(1, 'Alice', 'alice@example.com', 'USA', current_timestamp(), current_timestamp()),
(2, 'Bob', 'bob@example.com', 'UK', current_timestamp(), current_timestamp()),
(3, 'Carol', 'carol@example.com', 'Canada', current_timestamp(), current_timestamp());
```

#### Step 3: Create Silver Table with Transformations
```sql
USE CATALOG prod_analytics;
USE SCHEMA silver;

CREATE TABLE IF NOT EXISTS customers_cleaned AS
SELECT 
    customer_id,
    UPPER(name) as name,
    LOWER(email) as email,
    country,
    created_at,
    current_timestamp() as processed_at
FROM prod_analytics.bronze.customers
WHERE email IS NOT NULL;

-- Add comment
COMMENT ON TABLE prod_analytics.silver.customers_cleaned 
IS 'Cleaned customer data with validation checks';

-- Add column comments
COMMENT ON COLUMN prod_analytics.silver.customers_cleaned.customer_id 
IS 'Unique customer identifier (PK)';

COMMENT ON COLUMN prod_analytics.silver.customers_cleaned.email 
IS 'Customer email address - CONFIDENTIAL PII';
```

#### Step 4: Create Gold Table for Analytics
```sql
USE CATALOG prod_analytics;
USE SCHEMA gold;

CREATE TABLE IF NOT EXISTS customer_summary AS
SELECT 
    customer_id,
    name,
    country,
    COUNT(*) as total_records
FROM prod_analytics.silver.customers_cleaned
GROUP BY customer_id, name, country;
```

#### Step 5: Apply Tags & Set Permissions
```sql
-- Create PII tag
CREATE TAG prod_analytics.pii_classification VALUES ('public', 'internal', 'confidential');

-- Tag the email column as confidential
ALTER TABLE prod_analytics.silver.customers_cleaned 
ALTER COLUMN email SET TAG pii_classification = 'confidential';

-- Grant permissions
-- Grant schema usage
GRANT USAGE ON SCHEMA prod_analytics.bronze TO `analysts@company.com`;
GRANT USAGE ON SCHEMA prod_analytics.silver TO `analysts@company.com`;
GRANT USAGE ON SCHEMA prod_analytics.gold TO `analysts@company.com`;

-- Grant table select
GRANT SELECT ON TABLE prod_analytics.gold.customer_summary TO `analysts@company.com`;

-- View permissions
SHOW GRANTS ON TABLE prod_analytics.gold.customer_summary;
```

#### Step 6: Track Lineage
```sql
-- Query lineage information
SELECT 
    from_table,
    to_table,
    transformation_type
FROM system.access.table_lineage
WHERE to_table LIKE '%customer%'
ORDER BY to_table;

-- Create lineage tracking table
CREATE TABLE prod_analytics.metadata.table_lineage (
    source_table STRING,
    target_table STRING,
    transformation_type STRING,
    created_at TIMESTAMP
);

-- Manually log transformations
INSERT INTO prod_analytics.metadata.table_lineage VALUES
('prod_analytics.bronze.customers', 'prod_analytics.silver.customers_cleaned', 'CLEAN_VALIDATE', current_timestamp()),
('prod_analytics.silver.customers_cleaned', 'prod_analytics.gold.customer_summary', 'AGGREGATE', current_timestamp());
```

### Lab Deliverable
- Screenshot of catalog/schema structure
- SQL showing table creation with comments
- Evidence of tags applied
- Permissions grants output
- Lineage tracking query result

---

## Lab 3: Data Orchestration with Workflows (2-3 hours)

### Objective
Create a multi-task Databricks Workflow with dependencies, parameters, error handling, and scheduling.

### Prerequisites
- Labs 1-2 completed
- Job cluster permissions

### Instructions

#### Step 1: Create Extraction Notebook
Save as `/Shared/Lab3_Extract`

```python
# Lab 3: Extract Data Notebook

# Get parameters
environment = dbutils.widgets.get("environment")
date = dbutils.widgets.get("date")

print(f"Extracting data for {environment} on {date}")

# Simulate data extraction
from pyspark.sql.functions import current_timestamp, lit

df = spark.createDataFrame([
    (1, 'Alice', 'alice@example.com'),
    (2, 'Bob', 'bob@example.com'),
    (3, 'Carol', 'carol@example.com')
], ['customer_id', 'name', 'email'])

# Add metadata
df_extract = df \
    .withColumn("extracted_at", current_timestamp()) \
    .withColumn("environment", lit(environment))

# Save extraction count to task values
record_count = df_extract.count()
dbutils.jobs.taskValues.set(key="extracted_count", value=record_count)

# Write temp data
df_extract.write.format("delta").mode("overwrite") \
    .option("path", f"/tmp/lab3_extract_{environment}") \
    .saveAsTable(f"temp.lab3_customers_extract")

print(f"Extracted {record_count} records")
```

#### Step 2: Create Transform Notebook
Save as `/Shared/Lab3_Transform`

```python
# Lab 3: Transform Data Notebook

from pyspark.sql.functions import col, lower, upper, trim

environment = dbutils.widgets.get("environment")

# Read extracted data
df = spark.table("temp.lab3_customers_extract")

# Get count from previous task
extracted_count = dbutils.jobs.taskValues.get(key="extracted_count", taskKey="extract_data")
print(f"Processing {extracted_count} records from extraction task")

# Data cleaning
df_clean = df \
    .withColumn("name", upper(trim(col("name")))) \
    .withColumn("email", lower(trim(col("email"))))

# Validate
null_count = df_clean.filter(col("customer_id").isNull()).count()
if null_count > 0:
    raise Exception(f"Found {null_count} null customer IDs - data validation failed")

# Save transformed count
transformed_count = df_clean.count()
dbutils.jobs.taskValues.set(key="transformed_count", value=transformed_count)

print(f"Transformed {transformed_count} records")
```

#### Step 3: Create Load Notebook
Save as `/Shared/Lab3_Load`

```python
# Lab 3: Load Data Notebook

from pyspark.sql.functions import current_timestamp

environment = dbutils.widgets.get("environment")

# Get counts from previous tasks
extracted_count = dbutils.jobs.taskValues.get(key="extracted_count", taskKey="extract_data")
transformed_count = dbutils.jobs.taskValues.get(key="transformed_count", taskKey="transform_data")

print(f"Loading {transformed_count} transformed records (extracted: {extracted_count})")

# Read transformed data
df = spark.table("temp.lab3_customers_extract")

# Add load timestamp
df_load = df.withColumn("loaded_at", current_timestamp())

# Write to final table
target_table = f"prod_analytics.bronze.lab3_customers"
df_load.write.format("delta").mode("overwrite").saveAsTable(target_table)

# Log completion
print(f"Successfully loaded {df_load.count()} records to {target_table}")
```

#### Step 4: Create Workflow via Python API
```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

job_config = {
    "name": "Lab3_ETL_Pipeline",
    "tasks": [
        {
            "task_key": "extract_data",
            "notebook_task": {
                "notebook_path": "/Shared/Lab3_Extract",
                "base_parameters": {
                    "environment": "dev",
                    "date": "{{job.start_time}}"
                }
            },
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "i3.xlarge",
                "num_workers": 1
            },
            "timeout_seconds": 1800
        },
        {
            "task_key": "transform_data",
            "depends_on": [{"task_key": "extract_data"}],
            "notebook_task": {
                "notebook_path": "/Shared/Lab3_Transform",
                "base_parameters": {
                    "environment": "dev"
                }
            },
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "i3.xlarge",
                "num_workers": 1
            },
            "timeout_seconds": 1800
        },
        {
            "task_key": "load_data",
            "depends_on": [{"task_key": "transform_data"}],
            "notebook_task": {
                "notebook_path": "/Shared/Lab3_Load",
                "base_parameters": {
                    "environment": "dev"
                }
            },
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "i3.xlarge",
                "num_workers": 1
            },
            "timeout_seconds": 1800
        }
    ],
    "schedule": {
        "quartz_cron_expression": "0 2 * * ? *",
        "timezone_id": "America/New_York"
    },
    "email_notifications": {
        "on_failure": ["your-email@company.com"]
    }
}

response = w.jobs.create(**job_config)
job_id = response.job_id
print(f"Created job: {job_id}")

# Trigger manual run
run_response = w.jobs.run_now(job_id=job_id)
run_id = run_response.run_id
print(f"Triggered run: {run_id}")
```

#### Step 5: Monitor Workflow
```python
# Check run status
run = w.jobs.get_run(run_id=run_id)
print(f"Run Status: {run.state}")

# List all runs
runs = w.jobs.list_runs(job_id=job_id, limit=5)
for run in runs:
    print(f"Run {run.run_id}: {run.state}")

# Get run output
try:
    output = w.jobs.get_run_output(run_id=run_id)
    print(output.notebook_output.result)
except:
    print("Run still in progress or no output yet")
```

### Lab Deliverable
- Screenshot of created workflow in UI
- Successful run completion showing all 3 tasks completed
- Parameter passing evidence from task values
- Workflow run history showing schedule configured

---

## Lab 4: Delta Live Tables Pipeline (2-3 hours)

### Objective
Build end-to-end DLT pipeline with data quality expectations and monitoring.

### Prerequisites
- Labs 1-3 completed
- DLT cluster available

### Instructions

#### Step 1: Create DLT Pipeline Notebook
Save as `/Shared/Lab4_DLT_Pipeline`

```python
import dlt
from pyspark.sql.functions import col, current_timestamp, upper

# Bronze layer - raw ingestion
@dlt.create_table(
    comment="Raw order data from source system",
    partition_cols=["ingestion_date"]
)
def orders_bronze():
    return spark.createDataFrame([
        (1, 101, 'USA', 250.00, '2024-04-01'),
        (2, 102, 'UK', 150.00, '2024-04-02'),
        (3, 103, 'Canada', 300.00, '2024-04-03'),
    ], ['order_id', 'customer_id', 'country', 'amount', 'date']) \
    .withColumn("ingestion_date", current_timestamp().cast("date"))

# Silver layer - cleaned with expectations
@dlt.create_table(
    comment="Cleaned order data with quality checks"
)
@dlt.expect("valid_order_id", "order_id > 0")
@dlt.expect("valid_amount", "amount > 0")
@dlt.expect_all({
    "not_null_order": "order_id IS NOT NULL",
    "not_null_customer": "customer_id IS NOT NULL",
    "valid_country": "country IN ('USA', 'UK', 'Canada')"
})
def orders_silver():
    return dlt.read("orders_bronze") \
        .dropDuplicates(["order_id"]) \
        .filter("amount >= 0")

# Gold layer - business metrics
@dlt.create_table(
    comment="Order metrics by country"
)
def order_metrics():
    return dlt.read("orders_silver") \
        .groupBy("country") \
        .agg({
            "order_id": "count",
            "amount": "sum"
        }) \
        .withColumnRenamed("count(order_id)", "total_orders") \
        .withColumnRenamed("sum(amount)", "total_value")

# Data quality monitoring
@dlt.create_table(
    comment="DLT quality metrics"
)
def dlt_quality_metrics():
    return spark.sql("""
        SELECT 
            'orders_silver' as table_name,
            COUNT(*) as record_count,
            SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) as null_orders,
            SUM(CASE WHEN amount < 0 THEN 1 ELSE 0 END) as invalid_amounts,
            current_timestamp() as check_time
        FROM live.orders_silver
    """)
```

#### Step 2: Create DLT Pipeline
```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import pipelines

w = WorkspaceClient()

pipeline = w.pipelines.create(
    name="Lab4_DLT_Pipeline",
    storage="/Volumes/prod_analytics/pipelines/lab4_dlt",
    notebook_path="/Shared/Lab4_DLT_Pipeline",
    target="prod_analytics.lab4_dlt",
    configuration={
        "environment": "dev"
    },
    clusters=[{
        "label": "default",
        "node_type_id": "i3.xlarge",
        "num_workers": 1
    }]
)

pipeline_id = pipeline.pipeline_id
print(f"Created DLT pipeline: {pipeline_id}")
```

#### Step 3: Trigger Pipeline Update
```python
# Start pipeline update
update = w.pipelines.start_update(pipeline_id=pipeline_id)
update_id = update.update_id

print(f"Started update: {update_id}")

# Check update status
import time
while True:
    status = w.pipelines.get_update(pipeline_id=pipeline_id, update_id=update_id)
    print(f"Status: {status.state}")
    if status.state in ["COMPLETED", "FAILED"]:
        break
    time.sleep(5)
```

### Lab Deliverable
- DLT pipeline created and successfully run
- Screenshot of pipeline DAG showing all tables
- Data quality expectations validation results
- Query showing processed data in gold layer

---

## Lab Completion Checklist

- [ ] Lab 1: Delta Lake fundamentals - all steps completed
- [ ] Lab 2: Unity Catalog - catalog structure and governance configured
- [ ] Lab 3: Workflows - multi-task job created and executed
- [ ] Lab 4: DLT - pipeline built with quality expectations
- [ ] All screenshots and outputs documented
- [ ] Ready for advanced topics
