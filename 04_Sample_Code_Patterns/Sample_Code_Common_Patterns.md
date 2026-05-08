# Databricks Sample Code - Common Patterns

## Pattern 1: Bronze → Silver → Gold ETL Pipeline

### Notebook: Extract to Bronze
```python
# extract_to_bronze.py
# Purpose: Load raw data from external source and store in bronze

from pyspark.sql.functions import current_timestamp, col

# Configuration
environment = dbutils.widgets.get("environment")
source_path = f"/mnt/source/{environment}/customers.csv"
bronze_table = f"{environment}_analytics.ingestion.customers_bronze"

# Load raw data
df_raw = spark.read \
    .format("csv") \
    .option("header", "true") \
    .option("inferSchema", "false") \
    .load(source_path)

# Add metadata columns
df_bronze = df_raw \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .withColumn("source_file", lit(source_path)) \
    .withColumn("environment", lit(environment))

# Write to bronze table (append mode for incremental load)
df_bronze.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable(bronze_table)

print(f"Loaded {df_bronze.count()} records to {bronze_table}")
```

### Notebook: Transform to Silver
```python
# transform_to_silver.py
# Purpose: Clean, deduplicate, and validate data

from pyspark.sql.functions import col, trim, lower, when, coalesce
from pyspark.sql.window import Window

environment = dbutils.widgets.get("environment")
bronze_table = f"{environment}_analytics.ingestion.customers_bronze"
silver_table = f"{environment}_analytics.curated.customers_silver"

# Read bronze data
df_bronze = spark.table(bronze_table)

# Data quality checks
null_checks = df_bronze.filter(col("customer_id").isNull()).count()
if null_checks > 0:
    print(f"WARNING: Found {null_checks} records with null customer_id")

# Cleaning transformations
df_silver = df_bronze \
    .dropDuplicates(["customer_id"]) \
    .filter(col("customer_id").isNotNull()) \
    .withColumn("email", lower(trim(col("email")))) \
    .withColumn("phone", coalesce(col("phone"), lit(""))) \
    .filter("created_date >= '2020-01-01'")

# Add quality timestamp
df_silver = df_silver.withColumn("quality_check_timestamp", current_timestamp())

# Write to silver
df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .saveAsTable(silver_table)

print(f"Processed {df_silver.count()} records to {silver_table}")

# Set task value for downstream
dbutils.jobs.taskValues.set(key="record_count", value=df_silver.count())
```

### Notebook: Aggregate to Gold
```python
# transform_to_gold.py
# Purpose: Create business-ready analytics views

from pyspark.sql.functions import col, count, sum as spark_sum, max as spark_max

environment = dbutils.widgets.get("environment")
silver_table = f"{environment}_analytics.curated.customers_silver"
gold_table = f"{environment}_analytics.analytics.customers_gold"

# Read silver data
df_silver = spark.table(silver_table)

# Business logic transformations
df_gold = df_silver.select(
    col("customer_id"),
    col("name"),
    col("email"),
    col("country"),
    col("created_date")
).filter("country IS NOT NULL")

# Write to gold
df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(gold_table)

print(f"Created gold table with {df_gold.count()} records")
```

---

## Pattern 2: Delta Live Tables Pipeline

### DLT Pipeline Notebook
```python
# dlt_pipeline.py
# Purpose: Define multi-stage DLT pipeline with expectations

import dlt
from pyspark.sql.functions import col, current_timestamp

# Stage 1: Bronze (Raw Ingestion)
@dlt.create_table(
    comment="Raw customer data from source system",
    partition_cols=["ingestion_date"]
)
def customers_bronze():
    return spark.read.format("csv").option("header", "true") \
        .load("/mnt/source/customers.csv") \
        .withColumn("ingestion_date", current_timestamp().cast("date"))

# Stage 2: Silver (Cleansed & Validated)
@dlt.create_table(
    comment="Cleansed customer data with quality checks"
)
@dlt.expect("valid_customer_id", "customer_id > 0")
@dlt.expect("valid_email", "email LIKE '%@%' OR email IS NULL")
@dlt.expect_all({
    "not_null_id": "customer_id IS NOT NULL",
    "not_null_name": "name IS NOT NULL"
})
def customers_silver():
    return dlt.read("customers_bronze") \
        .dropDuplicates(["customer_id"]) \
        .filter("created_date >= '2020-01-01'")

# Stage 3: Gold (Business Analytics)
@dlt.create_table(
    comment="Customer metrics for analytics"
)
def customer_metrics():
    return dlt.read("customers_silver") \
        .select("customer_id", "name", "country", "created_date")

# Monitor data quality
@dlt.create_table(
    comment="Data quality metrics"
)
def data_quality_metrics():
    return spark.sql("""
        SELECT 
            'customers_silver' as table_name,
            COUNT(*) as record_count,
            SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) as null_ids,
            current_timestamp() as check_timestamp
        FROM live.customers_silver
    """)
```

---

## Pattern 3: Data Quality Monitoring

### Quality Checks Notebook
```python
# data_quality_checks.py
# Purpose: Validate data and generate quality report

from pyspark.sql.functions import col, count, sum as spark_sum, when
from datetime import datetime

environment = dbutils.widgets.get("environment")
table_name = f"{environment}_analytics.curated.customers_silver"
quality_table = f"{environment}_analytics.metadata.data_quality_results"

df = spark.table(table_name)

# Define quality checks
checks = {
    "total_records": df.count(),
    "null_customer_ids": df.filter(col("customer_id").isNull()).count(),
    "null_emails": df.filter(col("email").isNull()).count(),
    "duplicate_ids": df.count() - df.dropDuplicates(["customer_id"]).count(),
    "invalid_dates": df.filter("created_date > current_date()").count(),
}

# Create quality report
quality_report = spark.createDataFrame([
    (environment, table_name, check_name, check_value, datetime.now())
    for check_name, check_value in checks.items()
], ["environment", "table_name", "check_name", "check_value", "check_timestamp"])

# Write to quality tracking table
quality_report.write.format("delta").mode("append").saveAsTable(quality_table)

# Alert if checks fail
if checks["null_customer_ids"] > 0:
    print(f"⚠️  ALERT: Found {checks['null_customer_ids']} null customer IDs")
if checks["duplicate_ids"] > 0:
    print(f"⚠️  ALERT: Found {checks['duplicate_ids']} duplicate customer IDs")

print(f"Quality checks completed. Report saved to {quality_table}")
```

---

## Pattern 4: Incremental Load with Checkpoint

### Incremental Load Notebook
```python
# incremental_load.py
# Purpose: Load only new data since last run

from pyspark.sql.functions import max as spark_max, col
from datetime import datetime

environment = dbutils.widgets.get("environment")
source_table = f"{environment}_source_db.customers"
bronze_table = f"{environment}_analytics.ingestion.customers_bronze"
checkpoint_table = f"{environment}_analytics.metadata.load_checkpoints"

# Get last checkpoint
try:
    last_checkpoint = spark.sql(f"""
        SELECT MAX(last_load_timestamp) as last_timestamp
        FROM {checkpoint_table}
        WHERE table_name = '{source_table}'
    """).collect()[0]["last_timestamp"]
except:
    last_checkpoint = "1900-01-01"

print(f"Last checkpoint: {last_checkpoint}")

# Load incremental data
df_new = spark.sql(f"""
    SELECT *
    FROM {source_table}
    WHERE modified_timestamp > '{last_checkpoint}'
""")

record_count = df_new.count()
print(f"Found {record_count} new records")

# Write to bronze
if record_count > 0:
    df_new.write.format("delta").mode("append").saveAsTable(bronze_table)
    
    # Update checkpoint
    checkpoint_record = spark.createDataFrame([(
        environment,
        source_table,
        datetime.now(),
        record_count
    )], ["environment", "table_name", "last_load_timestamp", "record_count"])
    
    checkpoint_record.write.format("delta").mode("append").saveAsTable(checkpoint_table)
    print(f"Checkpoint updated: {datetime.now()}")

# Return count for workflow
dbutils.jobs.taskValues.set(key="loaded_count", value=record_count)
```

---

## Pattern 5: Conditional Workflow Logic

### Quality Gate Notebook
```python
# quality_gate.py
# Purpose: Validate data quality before publishing

from pyspark.sql.functions import col, count as spark_count

environment = dbutils.widgets.get("environment")
table_name = f"{environment}_analytics.curated.customers_silver"

df = spark.table(table_name)

# Quality thresholds
total_records = df.count()
null_rate = df.filter(col("customer_id").isNull()).count() / total_records if total_records > 0 else 0
duplicate_rate = (df.count() - df.dropDuplicates(["customer_id"]).count()) / total_records if total_records > 0 else 0

print(f"Total records: {total_records}")
print(f"Null rate: {null_rate:.2%}")
print(f"Duplicate rate: {duplicate_rate:.2%}")

# Pass/fail logic
passed = (
    total_records > 0 and
    null_rate < 0.05 and  # Less than 5% nulls
    duplicate_rate < 0.01  # Less than 1% duplicates
)

if passed:
    print("✅ PASSED: Quality gate checks successful")
    dbutils.jobs.taskValues.set(key="quality_status", value="PASSED")
else:
    print("❌ FAILED: Quality gate checks failed")
    print(f"   - Null rate too high: {null_rate:.2%}")
    print(f"   - Duplicate rate too high: {duplicate_rate:.2%}")
    dbutils.jobs.taskValues.set(key="quality_status", value="FAILED")
    # Raise exception to trigger failure handler
    raise Exception("Quality gate failed - data not suitable for publishing")
```

---

## Pattern 6: Data Lineage Tracking

### Lineage Tracking Notebook
```python
# track_lineage.py
# Purpose: Log table dependencies for lineage tracking

from datetime import datetime

environment = dbutils.widgets.get("environment")

# Define lineage relationships
lineage_records = [
    {
        "source_table": f"{environment}_source.customers",
        "target_table": f"{environment}_analytics.ingestion.customers_bronze",
        "transformation_type": "INGESTION",
        "environment": environment,
        "timestamp": datetime.now()
    },
    {
        "source_table": f"{environment}_analytics.ingestion.customers_bronze",
        "target_table": f"{environment}_analytics.curated.customers_silver",
        "transformation_type": "CLEAN_VALIDATE",
        "environment": environment,
        "timestamp": datetime.now()
    },
    {
        "source_table": f"{environment}_analytics.curated.customers_silver",
        "target_table": f"{environment}_analytics.analytics.customer_metrics",
        "transformation_type": "AGGREGATE",
        "environment": environment,
        "timestamp": datetime.now()
    }
]

# Save to lineage table
lineage_df = spark.createDataFrame(lineage_records)
lineage_table = f"{environment}_analytics.metadata.table_lineage"
lineage_df.write.format("delta").mode("append").saveAsTable(lineage_table)

print(f"Tracked {len(lineage_records)} lineage relationships")

# Query lineage
spark.sql(f"""
    SELECT * FROM {lineage_table}
    WHERE environment = '{environment}'
    ORDER BY timestamp DESC
    LIMIT 10
""").display()
```

---

## Pattern 7: Error Handling & Retry Logic

### Resilient ETL Notebook
```python
# resilient_etl.py
# Purpose: Handle errors gracefully with retries

from pyspark.sql.functions import current_timestamp, col
import time

environment = dbutils.widgets.get("environment")
max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        # Attempt to load and process data
        df = spark.read.format("csv").option("header", "true") \
            .load("/mnt/source/data.csv")
        
        # Process data
        df_processed = df.filter(col("id").isNotNull())
        
        # Write with validation
        if df_processed.count() > 0:
            df_processed.write.format("delta").mode("overwrite") \
                .saveAsTable(f"{environment}_analytics.data")
            
            print("✅ SUCCESS: Data loaded successfully")
            dbutils.jobs.taskValues.set(key="load_status", value="SUCCESS")
            break
        else:
            raise Exception("No valid records found")
    
    except Exception as e:
        retry_count += 1
        print(f"❌ ERROR (Attempt {retry_count}/{max_retries}): {str(e)}")
        
        if retry_count < max_retries:
            wait_time = 60 * retry_count  # Exponential backoff
            print(f"Retrying in {wait_time} seconds...")
            # Note: Don't actually sleep - Databricks will handle retry
        else:
            print("Max retries exceeded")
            dbutils.jobs.taskValues.set(key="load_status", value="FAILED")
            raise
```

---

## Pattern 8: Masking PII Data

### PII Masking Notebook
```python
# mask_pii_data.py
# Purpose: Apply masking to sensitive data

from pyspark.sql.functions import when, concat, substring, lit, sha2
from pyspark.sql.functions import lower

environment = dbutils.widgets.get("environment")
silver_table = f"{environment}_analytics.curated.customers_silver"

df = spark.table(silver_table)

# Apply masking functions
df_masked = df.select(
    col("customer_id"),
    col("name"),
    # Mask email (show first 2 chars)
    when(
        current_user() in ("data-team@company.com", "admin@company.com"),
        col("email")
    ).otherwise(
        concat(substring(col("email"), 1, 2), lit("***@domain.com"))
    ).alias("email"),
    # Mask phone (show last 4 digits)
    when(
        is_account_group_member("data-team"),
        col("phone")
    ).otherwise(
        concat(lit("***-***-"), substring(col("phone"), -4, 4))
    ).alias("phone"),
    col("country")
)

# Write masked view
df_masked.write.format("delta").mode("overwrite") \
    .saveAsTable(f"{environment}_analytics.analytics.customers_masked")

print(f"Created masked view with PII protection")
```

---

## Pattern 9: Data Validation Framework

### Validation Rules Engine
```python
# validation_framework.py
# Purpose: Generic data validation using rules

from pyspark.sql.functions import col, when, count as spark_count, lit
import json

# Define validation rules
validation_rules = {
    "customers_silver": {
        "customer_id": {"type": "not_null", "severity": "error"},
        "email": {"type": "not_null", "severity": "warning"},
        "created_date": {"type": "date_range", "min": "2020-01-01", "severity": "error"}
    }
}

def validate_table(table_name, rules):
    """Validate a table against rules and return report"""
    df = spark.table(table_name)
    violations = []
    
    for column, rule in rules.items():
        rule_type = rule.get("type")
        severity = rule.get("severity", "warning")
        
        if rule_type == "not_null":
            violating_rows = df.filter(col(column).isNull()).count()
            if violating_rows > 0:
                violations.append({
                    "column": column,
                    "rule": "not_null",
                    "violating_rows": violating_rows,
                    "severity": severity
                })
        
        elif rule_type == "date_range":
            min_date = rule.get("min")
            violating_rows = df.filter(col(column) < min_date).count()
            if violating_rows > 0:
                violations.append({
                    "column": column,
                    "rule": f"date_range (>= {min_date})",
                    "violating_rows": violating_rows,
                    "severity": severity
                })
    
    return {
        "table": table_name,
        "total_records": df.count(),
        "violations": violations,
        "passed": len(violations) == 0
    }

# Run validation
results = {table: validate_table(table, rules) 
           for table, rules in validation_rules.items()}

# Display results
for table, result in results.items():
    print(f"\n{'='*50}")
    print(f"Table: {table}")
    print(f"Records: {result['total_records']}")
    print(f"Violations: {len(result['violations'])}")
    for violation in result['violations']:
        print(f"  - {violation['column']}: {violation['violating_rows']} rows ({violation['severity']})")
```

