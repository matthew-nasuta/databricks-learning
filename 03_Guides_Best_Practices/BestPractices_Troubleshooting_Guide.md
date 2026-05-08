# Databricks Best Practices & Troubleshooting Guide

## Part 1: Best Practices

### Data Modeling Best Practices

#### 1. Use Medallion Architecture (Bronze/Silver/Gold)
```
✅ GOOD - Three-tier data lake
├── Bronze: Raw data as-is from sources
├── Silver: Cleaned, deduplicated, validated
└── Gold: Business-ready, aggregated datasets

❌ BAD - Single flat structure
└── Data: Mix of raw, transformed, and aggregated
```

**Benefits:**
- Clear separation of concerns
- Easy data quality management
- Enables independent tuning of each layer
- Reduces impact of source system changes

#### 2. Use Delta Lake for All Tables
```sql
-- ✅ GOOD: Delta tables everywhere
CREATE TABLE customers USING DELTA;

-- ❌ BAD: Still using Parquet
CREATE TABLE customers USING PARQUET;
```

**Why:** Delta provides ACID, time travel, schema enforcement, better performance.

#### 3. Partition Strategically
```sql
-- ✅ GOOD: Partition on frequently filtered columns
CREATE TABLE events
PARTITIONED BY (year, month, day)
USING DELTA;

-- ❌ BAD: Too many partitions (cardinality explosion)
CREATE TABLE events
PARTITIONED BY (event_id, user_id, timestamp)
USING DELTA;
```

**Guidelines:**
- Partition on date/time columns
- Avoid high-cardinality columns (>10K values)
- Typical: 1-3 partition columns
- Each partition = subdirectory

#### 4. Use Z-Order for Multi-Column Filtering
```sql
-- After data loads, optimize table
OPTIMIZE table_name ZORDER BY (date_column, category_column);
```

**When to use:** Tables > 10GB with frequent multi-column filters.

### Code Quality Best Practices

#### 1. Use Comments Extensively
```sql
-- ✅ GOOD: Clear, detailed comments
CREATE TABLE silver.customers (
    customer_id INT NOT NULL COMMENT "Unique customer identifier (PK)",
    name STRING NOT NULL COMMENT "Customer full name",
    email STRING COMMENT "Email address (PII - restricted access)",
    created_at TIMESTAMP COMMENT "Account creation timestamp (UTC)"
) USING DELTA
COMMENT "Master customer table loaded daily from CRM system";

-- ❌ BAD: Unclear comments
CREATE TABLE customers (
    id INT,
    name STRING,
    email STRING
) USING DELTA;
```

#### 2. Use Meaningful Naming Conventions
```sql
-- ✅ GOOD: Descriptive, layered naming
prod_analytics.bronze.customers_raw
prod_analytics.silver.customers_cleaned
prod_analytics.gold.customer_metrics

-- ❌ BAD: Unclear, hard to search
db1.schema1.tab_001
db1.schema1.tab_002
```

#### 3. Add Column Comments & Tags
```sql
-- Document sensitive data
COMMENT ON COLUMN silver.customers.email 
IS 'Customer email - PII data. Restricted to data team and admins only.';

-- Tag for governance
ALTER TABLE silver.customers 
ALTER COLUMN ssn SET TAG data_sensitivity = 'restricted';
```

#### 4. Version Your Code
```python
# ✅ GOOD: Include version/date
# customers_etl.py v2.1
# Last modified: 2024-04-15
# Author: data-team@company.com
# Changes: Added email validation, improved error handling

# ❌ BAD: No versioning info
# customers_etl.py
```

### Performance Best Practices

#### 1. Cache Frequently Used DataFrames
```python
# ✅ GOOD: Cache for repeated use
df_reference = spark.table("dim_date")
df_reference.cache()

result = df_main.join(df_reference, "date_id")
result.write.mode("overwrite").saveAsTable("result_table")

df_reference.unpersist()  # Clean up

# ❌ BAD: Read same table multiple times
df1 = df_main.join(spark.table("dim_date"), "date_id")
df2 = df_main.join(spark.table("dim_date"), "date_id")  # Read again
```

#### 2. Use Broadcast Joins for Small Tables
```python
# ✅ GOOD: Broadcast small table
from pyspark.sql.functions import broadcast

df_result = df_large.join(
    broadcast(df_small),  # < 100MB
    "key",
    "inner"
)

# ❌ BAD: Let Spark decide (might shuffle)
df_result = df_large.join(df_small, "key", "inner")
```

#### 3. Use Repartition Before Writing
```python
# ✅ GOOD: Repartition to match query patterns
df.repartition(200, "date", "category") \
    .write \
    .partitionBy("date", "category") \
    .mode("overwrite") \
    .saveAsTable("my_table")

# ❌ BAD: Use default partitions (inefficient)
df.write.mode("overwrite").saveAsTable("my_table")
```

#### 4. Push Down Filters Early
```python
# ✅ GOOD: Filter early (before joins)
df = spark.table("large_table") \
    .filter("date >= '2024-01-01'") \
    .join(small_table, "id") \
    .select("name", "amount")

# ❌ BAD: Filter after aggregation
df = spark.table("large_table") \
    .join(small_table, "id") \
    .groupBy("name").sum("amount") \
    .filter("date >= '2024-01-01'")  # Too late!
```

### Data Governance Best Practices

#### 1. Always Tag Sensitive Data
```sql
-- Create PII tag
CREATE TAG IF NOT EXISTS pii_classification VALUES ('public', 'internal', 'confidential', 'restricted');

-- Tag columns
ALTER TABLE silver.customers ALTER COLUMN email SET TAG pii_classification = 'confidential';
ALTER TABLE silver.customers ALTER COLUMN ssn SET TAG pii_classification = 'restricted';
ALTER TABLE silver.customers ALTER COLUMN name SET TAG pii_classification = 'internal';
```

#### 2. Implement Row & Column Security
```sql
-- Row filter: only see own department
ALTER TABLE salary_data
SET ROW FILTER row_filter_department ON (department);

-- Column mask: show email partially
ALTER TABLE users ALTER COLUMN email 
SET MASK mask_email_function ON (email);
```

#### 3. Document All Tables
```sql
-- Comprehensive comments
COMMENT ON TABLE gold.customer_metrics IS 
'Customer aggregated metrics for analytics. 
Source: silver.customers + silver.orders
Updated: Daily at 2 AM UTC
Owner: analytics@company.com
Last reviewed: 2024-04-15
PII: Yes (contains customer names)
Retention: 3 years';
```

#### 4. Enable Audit Logging
```python
# Query audit logs to track access
spark.sql("""
    SELECT 
        timestamp,
        user_identity.email as user,
        action_type,
        request_params,
        response.result
    FROM system.access.audit
    WHERE object_type = 'TABLE'
    AND timestamp > current_timestamp() - INTERVAL 7 DAY
    ORDER BY timestamp DESC
""").display()
```

### Orchestration Best Practices

#### 1. Use Task Dependencies for Clarity
```json
✅ GOOD - Clear dependency chain:
extract → validate → transform → load → publish

❌ BAD - No dependencies:
[All tasks run in parallel potentially]
```

#### 2. Add Meaningful Error Handling
```python
{
    "task_key": "critical_load",
    "notebook_task": {...},
    "on_failure": [
        {
            "task_key": "notify_team_failure"
        },
        {
            "task_key": "rollback_changes"
        }
    ],
    "on_success": [
        {
            "task_key": "publish_metrics"
        }
    ],
    "max_retries": 2,
    "timeout_seconds": 3600
}
```

#### 3. Use Parameters for Flexibility
```python
# ✅ GOOD: Parameterized for reuse
{
    "task_key": "extract",
    "notebook_task": {
        "notebook_path": "/Shared/extract",
        "base_parameters": {
            "environment": "{{job.task_trigger_type}}",
            "date": "{{job.start_time}}"
        }
    }
}

# ❌ BAD: Hardcoded
{
    "task_key": "extract",
    "notebook_task": {
        "notebook_path": "/Shared/extract",
        "base_parameters": {
            "environment": "prod",
            "date": "2024-04-15"
        }
    }
}
```

#### 4. Monitor Job Health
```sql
-- Create job monitoring dashboard
SELECT 
    job_id,
    job_name,
    last_run_state,
    last_run_end_time,
    DATEDIFF(HOUR, last_run_end_time, current_timestamp()) as hours_since_run
FROM system.access.jobs_audit
WHERE last_run_state != 'SUCCESS'
ORDER BY last_run_end_time DESC;
```

---

## Part 2: Troubleshooting Guide

### Common Issues & Solutions

#### Issue 1: "RESOURCE_NOT_FOUND: Catalog not found"
```
Error: RESOURCE_NOT_FOUND: Catalog 'my_catalog' not found

Solution:
1. Verify catalog name spelling
2. Check catalog exists: SHOW CATALOGS;
3. Use full path: catalog.schema.table
4. Ask admin to create catalog if needed

Prevention:
- Double-check paths before writing code
- Use autocomplete in notebook
```

#### Issue 2: "PERMISSION_DENIED"
```
Error: PERMISSION_DENIED: User xyz@company.com does not have permission

Solution:
1. Verify user has necessary grants:
   SHOW GRANTS ON TABLE my_table;
2. Ask table owner to grant permissions:
   GRANT SELECT ON TABLE my_table TO 'user@company.com';
3. Check if user is in correct group

Prevention:
- Principle of least privilege
- Use group-based permissions
- Document access requirements
```

#### Issue 3: "Out of Memory" Errors
```
Error: java.lang.OutOfMemoryError: Java heap space

Solutions:
1. Increase cluster memory:
   - Use larger instance types
   - Add more workers
   
2. Optimize code:
   - Filter data earlier
   - Use broadcast for small tables
   - Repartition strategically
   
3. Split into smaller batches:
   - Process by date range
   - Process by region/category
   - Use incremental logic

4. Check for skew:
   - Uneven data distribution
   - One partition much larger
   - Fix with repartitioning
```

#### Issue 4: "Query Timeout"
```
Error: Query execution exceeded timeout

Solutions:
1. Add partition filters:
   WHERE date >= '2024-04-01'  # Much faster
   
2. Use Z-order clustering:
   OPTIMIZE table_name ZORDER BY (date, category)
   
3. Increase timeout in job config:
   "timeout_seconds": 7200  # 2 hours
   
4. Break into smaller queries:
   - Process in batches
   - Use separate jobs for each stage

5. Check EXPLAIN plan:
   EXPLAIN SELECT * FROM my_table
   - Look for full table scans
   - Check join strategies
```

#### Issue 5: "Schema Mismatch in MERGE"
```
Error: org.apache.spark.sql.AnalysisException: cannot resolve

Solution:
1. Check column names match exactly (case-sensitive)
2. Enable schema merge:
   df.write.option("mergeSchema", "true")...
3. Verify data types match
4. Use SELECT * to include all columns

Example fix:
MERGE INTO target_table t
USING source_table s
ON t.customer_id = s.customer_id  # Check exact names
WHEN MATCHED THEN UPDATE SET 
    t.name = s.name,
    t.email = s.email
WHEN NOT MATCHED THEN INSERT *;
```

#### Issue 6: "External Location Invalid"
```
Error: INVALID_EXTERNAL_LOCATION: Invalid path

Solution:
1. Verify S3/ADLS path format:
   - S3: s3://bucket-name/path/
   - ADLS: abfss://container@storage.dfs.core.windows.net/path/
   - GCS: gs://bucket-name/path/
   
2. Check credentials/IAM:
   - Verify mount or service principal
   - Check permissions on storage
   
3. Use ls to verify path exists:
   dbutils.fs.ls("s3://bucket-name/path/")
   
4. Create external location in UC:
   CREATE EXTERNAL LOCATION my_location URL 's3://bucket/path'
```

#### Issue 7: "Workflow Circular Dependency"
```
Error: Circular dependency detected in workflow

Solution:
1. Review task dependencies
2. Remove circular references:
   ❌ A depends on B, B depends on A
   ✅ A → B → C (linear)
3. Redraw dependency chain
4. Use separate jobs if needed
```

#### Issue 8: "Task Values Not Accessible"
```
Error: TaskValueException: Task value not found

Solution:
1. Verify value was set in upstream task:
   dbutils.jobs.taskValues.set(key="count", value=100)
   
2. Use correct task key:
   dbutils.jobs.taskValues.get(key="count", taskKey="extract")  # Correct
   
3. Ensure dependent task is configured:
   "depends_on": [{"task_key": "extract"}]
   
4. Check value type - must be JSON serializable
```

### Debugging Techniques

#### 1. Use EXPLAIN to Analyze Queries
```sql
-- Simple plan
EXPLAIN SELECT * FROM large_table WHERE date = '2024-04-01'

-- Detailed plan with costs
EXPLAIN COST SELECT * FROM table1 
JOIN table2 ON table1.id = table2.id

-- Physical plan
EXPLAIN EXTENDED SELECT COUNT(*) FROM table1
```

#### 2. Enable Verbose Logging
```python
# Increase Spark logging
spark.sparkContext.setLogLevel("DEBUG")

# In notebook
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("myapp")
logger.debug("Debug message")
```

#### 3. Profile Data Processing
```python
# Check DataFrame sizes
df.count()  # Row count
df.cache().count()  # Cache and measure

# Check memory usage
spark.conf.get("spark.driver.memory")

# Profile transformations
import time
start = time.time()
result = df.groupBy("category").count()
result.show()
elapsed = time.time() - start
print(f"Execution time: {elapsed:.2f}s")
```

#### 4. Test Incrementally
```python
# Test with small subset first
df_small = spark.table("my_table").limit(100)
df_result = df_small.groupBy("category").agg({"amount": "sum"})
df_result.show()

# Then scale up
df = spark.table("my_table")
df_result = df.groupBy("category").agg({"amount": "sum"})
df_result.show()
```

#### 5. Monitor Cluster Performance
```python
# Check task stats
spark.sparkContext.statusTracker().getExecutorInfos()

# Memory usage
spark.sparkContext._jsc.sc().getExecutorMemoryStatus()

# Active tasks
spark.sparkContext.statusTracker().getTaskInfos()
```

### Monitoring Checklist

```
Regular Monitoring Tasks:
☐ Check job success rates (weekly)
☐ Monitor pipeline latency (daily)
☐ Review data quality metrics (daily)
☐ Audit access logs (weekly)
☐ Track cost trends (monthly)
☐ Update documentation (quarterly)
☐ Review governance policies (quarterly)
☐ Test disaster recovery (quarterly)
```

### Performance Tuning Checklist

```
Before Optimizing:
☐ Measure baseline performance
☐ Identify actual bottleneck (not guessing)
☐ Run EXPLAIN to understand plan
☐ Check Spark UI for skew/issues
☐ Profile with small dataset first

During Optimization:
☐ Change one thing at a time
☐ Measure impact of each change
☐ Keep detailed notes
☐ Don't over-optimize prematurely

After Optimization:
☐ Document changes made
☐ Update monitoring/alerts
☐ Train team on new patterns
☐ Plan for future scale
```
