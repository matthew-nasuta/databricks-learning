# Python/PySpark Exercises for Databricks Learning
# Start simple, progress to advanced
# Run these in Databricks notebook cells

# ============================================================================
# SECTION 1: BASIC DATAFRAME OPERATIONS
# ============================================================================

# Exercise 1.1: Create a DataFrame
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.sql.functions import col, lit, current_timestamp, count as spark_count

# Create sample employee data
employees_data = [
    (1, "Alice Johnson", "Engineering", 120000),
    (2, "Bob Smith", "Sales", 95000),
    (3, "Carol White", "Engineering", 115000),
    (4, "David Brown", "HR", 85000),
    (5, "Eve Davis", "Sales", 98000)
]

employees_schema = StructType([
    StructField("emp_id", IntegerType(), True),
    StructField("emp_name", StringType(), True),
    StructField("department", StringType(), True),
    StructField("salary", IntegerType(), True)
])

df_employees = spark.createDataFrame(employees_data, schema=employees_schema)

# TODO: Display the DataFrame
# EXPECTED: 5 rows with employee info
df_employees.display()
# OR: df_employees.show()


# Exercise 1.2: Select specific columns
# TODO: Select only name and salary
# EXPECTED: 2 columns, 5 rows
df_employees.select("emp_name", "salary").display()


# Exercise 1.3: Filter data
# TODO: Filter for Engineering department
# EXPECTED: 2 rows (Alice, Carol)
df_engineering = df_employees.filter(col("department") == "Engineering")
df_engineering.display()


# Exercise 1.4: Multiple conditions
# TODO: Filter for Engineering with salary > 115000
# EXPECTED: 1 row (Alice)
df_filtered = df_employees.filter(
    (col("department") == "Engineering") & (col("salary") > 115000)
)
df_filtered.display()


# Exercise 1.5: Add a new column
# TODO: Add bonus column (salary * 0.1)
# EXPECTED: New column with calculated values
df_with_bonus = df_employees.withColumn(
    "bonus",
    col("salary") * 0.1
)
df_with_bonus.display()


# Exercise 1.6: Rename column
# TODO: Rename 'emp_name' to 'employee_name'
# EXPECTED: Column renamed
df_renamed = df_employees.withColumnRenamed("emp_name", "employee_name")
df_renamed.display()


# Exercise 1.7: Sort data
# TODO: Sort by salary descending
# EXPECTED: Alice (120000) first, David (85000) last
df_sorted = df_employees.orderBy(col("salary").desc())
df_sorted.display()


# Exercise 1.8: Count and aggregation
# TODO: Get total count of employees
# EXPECTED: 5
count = df_employees.count()
print(f"Total employees: {count}")


# ============================================================================
# SECTION 2: INTERMEDIATE - AGGREGATIONS & GROUPBY
# ============================================================================

# Exercise 2.1: GroupBy with aggregation
# TODO: Count employees by department
# EXPECTED: Engineering (2), Sales (2), HR (1)
df_dept_count = df_employees.groupBy("department").count()
df_dept_count.display()


# Exercise 2.2: Multiple aggregations
# TODO: Calculate dept statistics
# EXPECTED: Department, count, avg salary, max salary, min salary
df_dept_stats = df_employees.groupBy("department").agg(
    spark_count("emp_id").alias("emp_count"),
    F.avg("salary").alias("avg_salary"),
    F.max("salary").alias("max_salary"),
    F.min("salary").alias("min_salary")
)
df_dept_stats.display()


# Exercise 2.3: Filter with HAVING
# TODO: Find departments with more than 1 employee
# EXPECTED: 2 rows (Engineering, Sales)
df_large_depts = df_employees.groupBy("department").count().filter(col("count") > 1)
df_large_depts.display()


# Exercise 2.4: Window functions - ROW_NUMBER
# TODO: Rank employees by salary within department
# EXPECTED: Ranking resets per department
from pyspark.sql.window import Window

window_spec = Window.partitionBy("department").orderBy(col("salary").desc())
df_ranked = df_employees.withColumn(
    "salary_rank",
    F.row_number().over(window_spec)
)
df_ranked.display()


# Exercise 2.5: Window function - Running total
# TODO: Calculate running total salary by department
# EXPECTED: Cumulative values
window_running = Window.partitionBy("department").orderBy("emp_id")
df_running = df_employees.withColumn(
    "running_salary_total",
    F.sum("salary").over(window_running)
)
df_running.display()


# Exercise 2.6: LAG and LEAD functions
# TODO: Show previous and next salary
# EXPECTED: Compare salaries
window_lag_lead = Window.orderBy("salary")
df_lag_lead = df_employees.withColumn(
    "prev_salary",
    F.lag("salary").over(window_lag_lead)
).withColumn(
    "next_salary",
    F.lead("salary").over(window_lag_lead)
)
df_lag_lead.display()


# ============================================================================
# SECTION 3: JOINS
# ============================================================================

# Create department data
departments_data = [
    (1, "Engineering", "Frank Miller", 500000),
    (2, "Sales", "Grace Lee", 300000),
    (3, "HR", "Henry Zhang", 150000)
]

departments_schema = StructType([
    StructField("dept_id", IntegerType(), True),
    StructField("dept_name", StringType(), True),
    StructField("manager", StringType(), True),
    StructField("budget", IntegerType(), True)
])

df_departments = spark.createDataFrame(departments_data, schema=departments_schema)

# Create employee-department mapping
emp_dept_data = [
    (1, 1),
    (2, 2),
    (3, 1),
    (4, 3),
    (5, 2)
]

emp_dept_schema = StructType([
    StructField("emp_id", IntegerType(), True),
    StructField("dept_id", IntegerType(), True)
])

df_emp_dept = spark.createDataFrame(emp_dept_data, schema=emp_dept_schema)


# Exercise 3.1: INNER JOIN
# TODO: Join employees with departments
# EXPECTED: 5 rows with employee and dept info
df_inner_join = df_emp_dept.join(
    df_departments,
    df_emp_dept.dept_id == df_departments.dept_id,
    "inner"
).select(
    df_emp_dept.emp_id,
    df_departments.dept_name
)
df_inner_join.display()


# Exercise 3.2: LEFT JOIN
# TODO: All departments with employee counts
# EXPECTED: All depts listed
df_left_join = df_departments.join(
    df_emp_dept,
    df_departments.dept_id == df_emp_dept.dept_id,
    "left"
).groupBy(df_departments.dept_name).count()
df_left_join.display()


# Exercise 3.3: Multiple joins
# TODO: Combine employees, emp_dept, departments
# EXPECTED: Full employee details with department
df_multi_join = df_employees.join(
    df_emp_dept,
    df_employees.emp_id == df_emp_dept.emp_id
).join(
    df_departments,
    df_emp_dept.dept_id == df_departments.dept_id
).select(
    df_employees.emp_name,
    df_departments.dept_name,
    df_employees.salary
)
df_multi_join.display()


# ============================================================================
# SECTION 4: STRING & TYPE CONVERSIONS
# ============================================================================

# Exercise 4.1: String operations
# TODO: Manipulate strings
# EXPECTED: Upper/lower/substring operations
df_string_ops = df_employees.select(
    col("emp_name"),
    F.upper(col("emp_name")).alias("name_upper"),
    F.lower(col("emp_name")).alias("name_lower"),
    F.substring(col("emp_name"), 1, 5).alias("name_first_5"),
    F.length(col("emp_name")).alias("name_length")
)
df_string_ops.display()


# Exercise 4.2: String concatenation
# TODO: Combine columns
# EXPECTED: Full details string
df_concat = df_employees.select(
    col("emp_name"),
    F.concat(
        col("emp_name"), 
        lit(" - "), 
        col("department"),
        lit(" ($"),
        col("salary"),
        lit(")")
    ).alias("full_info")
)
df_concat.display()


# Exercise 4.3: Conditional logic
# TODO: Categorize salary ranges
# EXPECTED: Low, Medium, High categories
df_conditional = df_employees.select(
    col("emp_name"),
    col("salary"),
    F.when(col("salary") < 90000, "Low")
     .when(col("salary") < 110000, "Medium")
     .otherwise("High")
     .alias("salary_category")
)
df_conditional.display()


# Exercise 4.4: Type conversions
# TODO: Convert between types
# EXPECTED: String to int, etc.
df_conversion = df_employees.select(
    col("emp_id").cast("string").alias("emp_id_str"),
    col("salary").cast("double").alias("salary_double"),
    F.date_format(current_timestamp(), "yyyy-MM-dd").alias("today")
)
df_conversion.display()


# ============================================================================
# SECTION 5: DATA QUALITY & TRANSFORMATION
# ============================================================================

# Create sample data with quality issues
orders_data = [
    (1, 101, 100.00, "2024-01-01"),
    (2, None, 200.00, "2024-01-02"),
    (3, 103, None, "2024-01-03"),
    (4, 104, 150.00, "2024-01-04"),
    (5, 105, -50.00, "2024-01-05"),  # Invalid negative amount
]

orders_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("amount", DoubleType(), True),
    StructField("order_date", StringType(), True)
])

df_orders = spark.createDataFrame(orders_data, schema=orders_schema)


# Exercise 5.1: Find NULL values
# TODO: Identify incomplete records
# EXPECTED: Rows with missing data
df_nulls = df_orders.filter(
    col("customer_id").isNull() | 
    col("amount").isNull()
)
df_nulls.display()


# Exercise 5.2: Fill NULL values
# TODO: Replace nulls with defaults
# EXPECTED: Nulls replaced
df_filled = df_orders.fillna({
    "customer_id": -1,
    "amount": 0.0
})
df_filled.display()


# Exercise 5.3: Data validation
# TODO: Find invalid records
# EXPECTED: Records with amount <= 0
df_invalid = df_orders.filter(col("amount") <= 0)
df_invalid.display()


# Exercise 5.4: Remove duplicates
# TODO: Create dupe data and remove
# EXPECTED: Clean data
df_with_dupes = df_orders.union(df_orders.limit(2))  # Add duplicates
df_deduped = df_with_dupes.dropDuplicates()
print(f"Before dedup: {df_with_dupes.count()}, After: {df_deduped.count()}")


# Exercise 5.5: Data completeness check
# TODO: Calculate % non-null for each column
# EXPECTED: Completeness metrics
from pyspark.sql import functions as F

df_completeness = df_orders.select([
    ((F.count(col(c)) / F.count(lit(1))) * 100).alias(f"{c}_completeness")
    for c in df_orders.columns
])
df_completeness.display()


# ============================================================================
# SECTION 6: FILE I/O & PERSISTENCE
# ============================================================================

# Exercise 6.1: Write to Delta Lake
# TODO: Save DataFrame as Delta table
# EXPECTED: Table created in DBFS
df_employees.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("learning.exercises.employees_delta")

print("Table saved successfully")


# Exercise 6.2: Read from Delta
# TODO: Read back the saved table
# EXPECTED: Data retrieved
df_read = spark.read.format("delta").table("learning.exercises.employees_delta")
df_read.display()


# Exercise 6.3: Write Parquet
# TODO: Save as Parquet file
# EXPECTED: File created
df_employees.write \
    .format("parquet") \
    .mode("overwrite") \
    .save("/tmp/employees_parquet")

print("Parquet saved")


# Exercise 6.4: Write CSV (for export)
# TODO: Export to CSV
# EXPECTED: CSV file created
df_employees.write \
    .format("csv") \
    .mode("overwrite") \
    .option("header", "true") \
    .save("/tmp/employees_csv")

print("CSV exported")


# ============================================================================
# SECTION 7: COMPLEX TRANSFORMATIONS (ETL Patterns)
# ============================================================================

# Exercise 7.1: Bronze → Silver transformation
# TODO: Clean raw data
# EXPECTED: Cleaned version

# Simulate raw bronze data
df_bronze = df_orders.select(
    col("order_id"),
    col("customer_id"),
    col("amount"),
    col("order_date").cast("date").alias("order_date"),
    current_timestamp().alias("ingestion_timestamp")
)

# Clean to silver
df_silver = df_bronze \
    .filter(col("customer_id").isNotNull()) \
    .filter(col("amount") > 0) \
    .filter(col("amount") < 100000) \
    .withColumn("amount_rounded", F.round(col("amount"), 2))

df_silver.display()


# Exercise 7.2: Silver → Gold aggregation
# TODO: Create analytics-ready dataset
# EXPECTED: Aggregated metrics

df_gold = df_silver.groupBy("customer_id").agg(
    F.count("order_id").alias("total_orders"),
    F.sum("amount").alias("total_spent"),
    F.avg("amount").alias("avg_order"),
    F.max("amount").alias("max_order"),
    F.min(col("order_date")).alias("first_order"),
    F.max(col("order_date")).alias("last_order")
).orderBy(F.desc("total_spent"))

df_gold.display()


# Exercise 7.3: Data quality check framework
# TODO: Create reusable quality checks
# EXPECTED: Quality metrics

def quality_check(df, column, check_type, threshold=None):
    """Generic quality check function"""
    if check_type == "null_count":
        return df.filter(col(column).isNull()).count()
    elif check_type == "unique_count":
        return df.select(column).distinct().count()
    elif check_type == "min_max":
        result = df.agg(
            F.min(column).alias("min"),
            F.max(column).alias("max")
        ).collect()[0]
        return (result.min, result.max)

# Use the function
null_orders = quality_check(df_silver, "order_id", "null_count")
unique_customers = quality_check(df_silver, "customer_id", "unique_count")
amount_range = quality_check(df_silver, "amount", "min_max")

print(f"Null orders: {null_orders}")
print(f"Unique customers: {unique_customers}")
print(f"Amount range: {amount_range}")


# ============================================================================
# SECTION 8: OPTIMIZATION & PERFORMANCE
# ============================================================================

# Exercise 8.1: Caching
# TODO: Cache frequently used DataFrames
# EXPECTED: Improved performance on repeated operations

df_large = df_employees.union(df_employees).union(df_employees)
df_large.cache()
print(f"Cached {df_large.count()} rows")

# Multiple operations will be faster
_ = df_large.filter(col("department") == "Engineering").count()
_ = df_large.filter(col("salary") > 100000).count()

df_large.unpersist()


# Exercise 8.2: Repartition
# TODO: Repartition for better performance
# EXPECTED: Optimized partition count
df_repartitioned = df_large.repartition(10, "department")
print(f"Repartitioned to 10 partitions")


# Exercise 8.3: Broadcast join
# TODO: Broadcast small table for efficient join
# EXPECTED: Better join performance
from pyspark.sql.functions import broadcast

df_small = df_departments  # Small reference table
df_large_fact = df_employees  # Large fact table

df_broadcast_join = df_large_fact.join(
    broadcast(df_small),
    "dept_id",
    "left"
)


# Exercise 8.4: Explain query plan
# TODO: Analyze execution plan
# EXPECTED: See physical/logical plan
df_plan = df_employees \
    .filter(col("department") == "Engineering") \
    .groupBy("department").count()

df_plan.explain(extended=True)


# ============================================================================
# SECTION 9: PRACTICAL BUSINESS LOGIC
# ============================================================================

# Exercise 9.1: Customer segmentation
# TODO: Segment customers by value
# EXPECTED: VIP, Regular, Occasional categories

df_customer_value = df_gold.withColumn(
    "customer_segment",
    F.when(col("total_spent") > 500, "VIP")
     .when(col("total_spent") > 100, "Regular")
     .otherwise("Occasional")
).orderBy(F.desc("total_spent"))

df_customer_value.display()


# Exercise 9.2: Sales trend analysis
# TODO: Calculate period-over-period growth
# EXPECTED: Growth metrics

# Add date column
df_with_period = df_silver.withColumn(
    "month",
    F.trunc(col("order_date"), "month")
)

# Monthly sales
df_monthly = df_with_period.groupBy("month").agg(
    F.sum("amount").alias("monthly_revenue"),
    F.count("order_id").alias("order_count")
).orderBy("month")

df_monthly.display()


# Exercise 9.3: RFM Analysis (Recency, Frequency, Monetary)
# TODO: Create RFM scores
# EXPECTED: RFM segments

from datetime import datetime, timedelta

current_date = datetime.strptime("2024-02-01", "%Y-%m-%d")

df_rfm = df_silver.groupBy("customer_id").agg(
    F.max("order_date").alias("last_purchase"),
    F.count("order_id").alias("frequency"),
    F.sum("amount").alias("monetary")
).withColumn(
    "recency",
    F.datediff(lit(current_date), col("last_purchase"))
)

df_rfm.display()


# ============================================================================
# SECTION 10: CHALLENGES - Write your own solutions!
# ============================================================================

# Challenge 1: Multi-level aggregation
# TODO: For each department, get:
#   - Count of employees
#   - Total salary spend
#   - Average salary
#   - Salary as % of total company salary
# Write your own code here


# Challenge 2: Anomaly detection
# TODO: Find orders that are statistical outliers
#   - Find orders with amount > 2 standard deviations from mean
# Write your own code here


# Challenge 3: Customer churn prediction
# TODO: Identify at-risk customers
#   - Last purchase > 30 days ago AND
#   - Decreasing purchase frequency trend
# Write your own code here


# Challenge 4: Data reconciliation
# TODO: Compare two datasets
#   - Find records only in df_bronze
#   - Find records only in df_silver
#   - Identify discrepancies
# Write your own code here


# Challenge 5: Dynamic schema handling
# TODO: Create a function that reads CSV with unknown schema
#   - Detect data types
#   - Handle nulls intelligently
#   - Apply data quality rules
# Write your own code here


# ============================================================================
# SECTION 11: IMPORT STATEMENTS (Add at top of notebook)
# ============================================================================

"""
from pyspark.sql import SparkSession, functions as F, Window
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, DateType
from pyspark.sql.functions import (
    col, lit, when, otherwise, case,
    sum as spark_sum, count as spark_count, avg, min, max,
    upper, lower, substring, length, concat, trim,
    to_date, to_timestamp, date_format, datediff,
    row_number, rank, dense_rank, lag, lead,
    round, abs, cast, coalesce,
    current_timestamp, current_date
)
from datetime import datetime, timedelta
import json
"""


# ============================================================================
# HELPFUL REFERENCE FUNCTIONS
# ============================================================================

def show_dataframe_info(df):
    """Display comprehensive DataFrame info"""
    print("=" * 80)
    print(f"Rows: {df.count()}")
    print(f"Columns: {len(df.columns)}")
    print("\nSchema:")
    df.printSchema()
    print("\nFirst 5 rows:")
    df.show(5)
    print("=" * 80)

# Usage: show_dataframe_info(df_employees)


def compare_dataframes(df1, df2, name1="DF1", name2="DF2"):
    """Compare two DataFrames"""
    print(f"\n{name1} rows: {df1.count()}")
    print(f"{name2} rows: {df2.count()}")
    
    # Find rows only in df1
    only_in_df1 = df1.join(df2, df1.columns, "leftanti")
    print(f"Rows only in {name1}: {only_in_df1.count()}")
    
    # Find rows only in df2
    only_in_df2 = df2.join(df1, df1.columns, "leftanti")
    print(f"Rows only in {name2}: {only_in_df2.count()}")

# Usage: compare_dataframes(df_employees, df_read)


def profile_dataframe(df):
    """Create data profile of DataFrame"""
    from pyspark.sql import functions as F
    
    profile = []
    for col_name in df.columns:
        col_profile = {
            "column": col_name,
            "type": dict(df.dtypes)[col_name],
            "null_count": df.filter(col(col_name).isNull()).count(),
            "unique_count": df.select(col_name).distinct().count(),
            "null_percent": (df.filter(col(col_name).isNull()).count() / df.count() * 100)
        }
        profile.append(col_profile)
    
    profile_df = spark.createDataFrame(profile)
    profile_df.display()

# Usage: profile_dataframe(df_orders)
