# Databricks Basics Cheatsheet

## Cluster Management

### Create & Configure Cluster
```python
# Via Python API
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

cluster_config = {
    "cluster_name": "my-cluster",
    "spark_version": "13.3.x-scala2.12",
    "node_type_id": "i3.xlarge",
    "num_workers": 2,
    "autoscale": {"min_workers": 2, "max_workers": 8},
    "spark_conf": {
        "spark.databricks.delta.schema.autoMerge.enabled": "true"
    }
}

cluster = w.clusters.create(**cluster_config)
```

### Common Cluster Types
| Type | Use Case |
|------|----------|
| **All-purpose** | Interactive work, dev/testing |
| **Jobs** | Production ETL/orchestration |
| **SQL Warehouse** | BI & analytics queries |

---

## Notebook Basics

### Cell Magic Commands
```python
%python          # Python cell (default)
%sql             # SQL cell
%scala           # Scala cell
%sh              # Shell commands
%md              # Markdown
%run             # Run another notebook
```

### Display & Visualization
```python
# Display DataFrame
display(df)

# Plot data
display(df.select("date", "revenue").groupBy("date").sum())

# HTML rendering
displayHTML("<h1>Custom HTML</h1>")
```

### Working with Widgets
```python
# Create dropdown
dbutils.widgets.dropdown("environment", "dev", ["dev", "staging", "prod"])

# Get widget value
env = dbutils.widgets.get("environment")

# Remove all widgets
dbutils.widgets.removeAll()
```

### File Operations
```python
# List DBFS files
dbutils.fs.ls("/dbfs/my-path/")

# Upload file
dbutils.fs.put("/path/to/file.txt", "content", overwrite=True)

# Remove file/directory
dbutils.fs.rm("/path/to/delete", recurse=True)

# Read file
content = dbutils.fs.head("/path/to/file.txt")
```

---

## Delta Lake Quick Reference

### Create Delta Table
```sql
-- From external data
CREATE TABLE bronze_customers (
    customer_id INT,
    name STRING,
    email STRING,
    created_at TIMESTAMP
)
USING DELTA;

-- From query
CREATE TABLE silver_customers AS
SELECT customer_id, name, email, current_timestamp() as ingested_at
FROM bronze_customers;
```

### DML Operations
```sql
-- INSERT
INSERT INTO table_name VALUES (1, 'John', 'john@email.com');

-- UPDATE
UPDATE table_name SET email = 'newemail@domain.com' WHERE customer_id = 1;

-- DELETE
DELETE FROM table_name WHERE created_at < '2024-01-01';

-- MERGE (upsert)
MERGE INTO target_table t
USING source_table s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.value = s.value
WHEN NOT MATCHED THEN INSERT *;
```

### Time Travel
```sql
-- Query previous version
SELECT * FROM table_name VERSION AS OF 5;

-- Query at timestamp
SELECT * FROM table_name TIMESTAMP AS OF '2024-01-01 10:00:00';

-- Show table history
DESCRIBE HISTORY table_name;

-- Restore to previous version
RESTORE TABLE table_name TO VERSION AS OF 5;
```

### Schema Evolution
```sql
-- Add column
ALTER TABLE table_name ADD COLUMN new_column STRING;

-- Rename column
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;

-- Drop column
ALTER TABLE table_name DROP COLUMN unnecessary_column;

-- Change column type
ALTER TABLE table_name ALTER COLUMN value TYPE DOUBLE;
```

---

## Spark SQL Essentials

### Common Aggregations
```sql
-- Group by with multiple aggregates
SELECT 
    category,
    COUNT(*) as count,
    SUM(amount) as total,
    AVG(amount) as avg_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount
FROM sales
GROUP BY category;

-- Window functions
SELECT 
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total,
    RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) as rank
FROM orders;
```

### Joins
```sql
-- Inner join
SELECT a.id, a.name, b.value
FROM table_a a
INNER JOIN table_b b ON a.id = b.id;

-- Left join
SELECT a.*, b.value
FROM table_a a
LEFT JOIN table_b b ON a.id = b.id;

-- Multiple joins
SELECT a.id, b.value, c.status
FROM table_a a
JOIN table_b b ON a.id = b.a_id
JOIN table_c c ON b.id = c.b_id;
```

### Common Table Expressions (CTEs)
```sql
WITH ranked_sales AS (
    SELECT 
        customer_id,
        amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) as rank
    FROM sales
),
top_customers AS (
    SELECT DISTINCT customer_id
    FROM ranked_sales
    WHERE rank <= 10
)
SELECT * FROM top_customers;
```

---

## PySpark DataFrame Basics

### Create DataFrames
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("myapp").getOrCreate()

# From Spark SQL
df = spark.sql("SELECT * FROM my_table")

# From Pandas
df = spark.createDataFrame(pandas_df)

# From data
df = spark.createDataFrame(
    [("Alice", 25), ("Bob", 30)],
    ["name", "age"]
)
```

### Common Operations
```python
# Select columns
df.select("name", "age")

# Filter
df.filter(df.age > 25)
df.where("age > 25")

# GroupBy
df.groupBy("department").agg({"salary": "sum"})
df.groupBy("department").agg({"salary": "sum", "age": "avg"})

# Join
df1.join(df2, df1.id == df2.id, "inner")

# Sort
df.orderBy("age", ascending=False)

# Distinct
df.select("department").distinct()

# Count
df.count()

# Show
df.show(10)
```

### Write DataFrame
```python
# Parquet
df.write.mode("overwrite").parquet("/path/to/output")

# Delta (recommended)
df.write.mode("overwrite").format("delta").mode("overwrite").save("/path/to/delta")

# Create table
df.write.mode("overwrite").saveAsTable("my_table")

# Append
df.write.mode("append").saveAsTable("my_table")
```

---

## Performance Tips

### Optimization Best Practices
```python
# Partition data on write
df.write \
    .partitionBy("year", "month") \
    .format("delta") \
    .mode("overwrite") \
    .save("/path/to/data")

# Bucket data for joins
df.write \
    .bucketBy(10, "id") \
    .mode("overwrite") \
    .saveAsTable("bucketed_table")

# Z-order for filtering
spark.sql("OPTIMIZE table_name ZORDER BY (date_column, category_column)")

# Cache frequently used DataFrames
df.cache()
df.count()  # Trigger caching

# Repartition for shuffles
df.repartition(200).write.format("delta").mode("overwrite").save("/path")

# Broadcast small tables
from pyspark.sql.functions import broadcast
df_large.join(broadcast(df_small), "key")
```

### Query Hints
```sql
-- Broadcast hint (for small table joins)
SELECT /*+ BROADCAST(small_table) */ *
FROM large_table
JOIN small_table ON large_table.id = small_table.id;

-- Shuffle hash join
SELECT /*+ SHUFFLE_HASH(t1) */ *
FROM t1 JOIN t2 ON t1.id = t2.id;
```

---

## Monitoring Commands

### Check Spark Configuration
```python
# View all configs
spark.sparkContext.getConf().getAll()

# Check specific config
spark.conf.get("spark.sql.shuffle.partitions")
```

### DataFrame Information
```python
# Show schema
df.printSchema()

# Show dtypes
df.dtypes

# Get column names
df.columns

# Get row count
df.count()

# Get statistics
df.describe().show()
```

---

## Debugging

### Enable Debug Logging
```python
# In notebook
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable Spark SQL debug
spark.sparkContext.setLogLevel("DEBUG")
```

### Explain Query Plan
```python
df.explain()                    # Logical plan
df.explain(extended=True)       # Logical + physical plan
df.explain(mode="cost")         # Cost statistics
```

### Data Quality Checks
```python
# Null check
df.filter(df.customer_id.isNull()).count()

# Duplicate check
df.dropDuplicates().count() == df.count()

# Data type validation
df.select("amount").dtypes
```

---

## Useful Shortcuts

| Task | Command |
|------|---------|
| Clear output | Cmd+Shift+X (Mac) / Ctrl+Shift+X (Windows) |
| Run all cells | Cmd+A then Shift+Enter |
| Go to line | Cmd+G |
| Format code | Cmd+Shift+F |
| Comment line | Cmd+/ |
| View variables | Type `df` and run |
