# Databricks Workflows & Orchestration Cheatsheet

## Databricks Workflows Basics

### Create a Basic Workflow (via UI)
1. Click **Workflows** → **Create job**
2. Configure job name, cluster, tasks
3. Set schedule/trigger
4. Click **Create**

### Create Workflow via Python API
```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs

w = WorkspaceClient()

# Define job
job_config = {
    "name": "daily-customer-sync",
    "tasks": [
        {
            "task_key": "extract_customers",
            "notebook_task": {
                "notebook_path": "/Shared/pipelines/extract_customers",
                "base_parameters": {"environment": "prod"}
            },
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "i3.xlarge",
                "num_workers": 2
            }
        }
    ],
    "schedule": {
        "quartz_cron_expression": "0 2 * * ? *",  # 2 AM daily
        "timezone_id": "America/New_York"
    }
}

response = w.jobs.create(**job_config)
job_id = response.job_id
print(f"Created job: {job_id}")
```

---

## Workflow Task Types

### Notebook Task
```json
{
    "task_key": "notebook_task_example",
    "notebook_task": {
        "notebook_path": "/Shared/my_notebook",
        "base_parameters": {
            "date": "{{job.start_time}}",
            "environment": "prod"
        }
    },
    "new_cluster": { "spark_version": "13.3.x-scala2.12", "node_type_id": "i3.xlarge", "num_workers": 2 }
}
```

### SQL Task
```json
{
    "task_key": "sql_task_example",
    "sql_task": {
        "file": "/Shared/queries/daily_refresh.sql"
    },
    "sql_warehouse_task": {
        "warehouse_id": "1a2b3c4d5e6f7g8h"
    }
}
```

### Python/Spark Submit Task
```json
{
    "task_key": "spark_submit_example",
    "spark_python_task": {
        "python_file": "dbfs:/path/to/script.py",
        "parameters": ["--env", "prod", "--date", "2024-01-01"]
    },
    "new_cluster": { "spark_version": "13.3.x-scala2.12", "node_type_id": "i3.xlarge", "num_workers": 2 }
}
```

### Delta Live Tables (DLT) Task
```json
{
    "task_key": "dlt_pipeline_task",
    "pipeline_task": {
        "pipeline_id": "pipeline-id-12345"
    }
}
```

---

## Task Dependencies

### Linear Dependencies
```python
job_config = {
    "name": "multi-stage-etl",
    "tasks": [
        {
            "task_key": "extract",
            "notebook_task": {"notebook_path": "/Shared/extract"},
            "new_cluster": {...}
        },
        {
            "task_key": "transform",
            "notebook_task": {"notebook_path": "/Shared/transform"},
            "depends_on": [{"task_key": "extract"}],
            "new_cluster": {...}
        },
        {
            "task_key": "load",
            "notebook_task": {"notebook_path": "/Shared/load"},
            "depends_on": [{"task_key": "transform"}],
            "new_cluster": {...}
        }
    ]
}
```

### Parallel Tasks
```python
job_config = {
    "name": "parallel-processing",
    "tasks": [
        {
            "task_key": "extract_customers",
            "notebook_task": {"notebook_path": "/Shared/extract_customers"},
            "new_cluster": {...}
        },
        {
            "task_key": "extract_orders",
            "notebook_task": {"notebook_path": "/Shared/extract_orders"},
            "new_cluster": {...}
        },
        {
            "task_key": "merge_data",
            "notebook_task": {"notebook_path": "/Shared/merge"},
            "depends_on": [
                {"task_key": "extract_customers"},
                {"task_key": "extract_orders"}
            ],
            "new_cluster": {...}
        }
    ]
}
```

### Conditional Logic
```python
# Use email alerts to branch logic
job_config = {
    "tasks": [
        {
            "task_key": "quality_check",
            "notebook_task": {"notebook_path": "/Shared/quality_check"},
            "on_success": [{"task_key": "proceed"}],
            "on_failure": [{"task_key": "alert_team"}],
            "new_cluster": {...}
        }
    ]
}
```

---

## Scheduling & Triggers

### Cron Expressions
```python
# Daily at 2 AM
"0 2 * * ? *"

# Every 6 hours
"0 0,6,12,18 * * ? *"

# Monday-Friday at 9 AM
"0 9 ? * MON-FRI *"

# First day of month at 1 AM
"0 1 1 * ? *"

# Every 30 minutes
"0 */30 * * ? *"
```

### Schedule Configuration
```python
job_config = {
    "name": "scheduled_job",
    "schedule": {
        "quartz_cron_expression": "0 2 * * ? *",
        "timezone_id": "America/New_York",
        "pause_status": "UNPAUSED"
    },
    "tasks": [...]
}

# Pause schedule
w.jobs.reset(job_id=123, new_settings={"schedule": {"pause_status": "PAUSED"}})
```

### Event-Based Triggers
```python
# Trigger on S3 file arrival (requires event bridge setup)
job_config = {
    "name": "event_driven_job",
    "trigger": {
        "file_arrival_trigger": {
            "url": "s3://my-bucket/incoming/data/"
        }
    },
    "tasks": [...]
}
```

---

## Passing Parameters Between Tasks

### Using Notebook Parameters
```python
# In job config
{
    "task_key": "task_1",
    "notebook_task": {
        "notebook_path": "/Shared/task1",
        "base_parameters": {
            "date": "{{job.start_time}}",
            "environment": "prod"
        }
    }
}

# In notebook - retrieve parameters
date = dbutils.widgets.get("date")
environment = dbutils.widgets.get("environment")
```

### Passing Data Between Tasks (DBUtils)
```python
# Task 1: Save state
dbutils.jobs.taskValues.set(key="processed_count", value=1500)
dbutils.jobs.taskValues.set(key="error_list", value=["error1", "error2"])

# Task 2: Retrieve state
count = dbutils.jobs.taskValues.get(key="processed_count", taskKey="task_1")
errors = dbutils.jobs.taskValues.get(key="error_list", taskKey="task_1")
```

### Using Cluster Variables
```python
# Set in cluster config
{
    "spark_conf": {
        "spark.databricks.custom.environment": "prod",
        "spark.databricks.custom.date": "{{job.start_time}}"
    }
}

# Access in notebook
environment = spark.conf.get("spark.databricks.custom.environment")
```

---

## Error Handling & Retries

### Retry Configuration
```python
{
    "task_key": "risky_task",
    "max_retries": 3,
    "timeout_seconds": 3600,
    "notebook_task": {...},
    "new_cluster": {...}
}
```

### On Failure Actions
```python
{
    "task_key": "main_task",
    "notebook_task": {...},
    "on_failure": [
        {
            "task_key": "failure_handler"
        }
    ],
    "on_success": [
        {
            "task_key": "success_handler"
        }
    ],
    "new_cluster": {...}
}
```

### Error Notification
```python
job_config = {
    "name": "job_with_alerts",
    "tasks": [...],
    "email_notifications": {
        "on_failure": ["team@company.com"],
        "on_success": ["admin@company.com"]
    }
}
```

---

## Delta Live Tables (DLT) Pipeline

### Create DLT Pipeline
```python
from databricks.sdk.service import pipelines

w = WorkspaceClient()

pipeline_config = {
    "name": "customer_data_pipeline",
    "storage": "/Volumes/prod_analytics/pipelines/customer_pipeline",
    "configuration": {
        "environment": "prod"
    },
    "notebook_path": "/Shared/dlt/customer_pipeline",
    "target": "prod_analytics.customer_data",
    "clusters": [
        {
            "label": "default",
            "spark_conf": {
                "spark.databricks.delta.schema.autoMerge.enabled": "true"
            },
            "node_type_id": "i3.xlarge",
            "num_workers": 2
        }
    ]
}

response = w.pipelines.create(**pipeline_config)
pipeline_id = response.pipeline_id
```

### DLT Pipeline Notebook Structure
```python
# Create bronze table (raw)
@dlt.create_table(
    comment="Raw customer data from source system"
)
def customers_bronze():
    return spark.read.format("csv").load("/mnt/source/customers.csv")

# Create silver table (cleaned)
@dlt.create_table(
    comment="Cleaned customer data"
)
@dlt.expect("not_null_id", "customer_id IS NOT NULL")
@dlt.expect("valid_email", "email LIKE '%@%' OR email IS NULL")
def customers_silver():
    return (
        dlt.read("customers_bronze")
        .dropDuplicates(["customer_id"])
        .filter("created_at IS NOT NULL")
    )

# Create gold table (business logic)
@dlt.create_table(
    comment="Customer metrics for analytics"
)
def customer_metrics():
    return dlt.read("customers_silver").select("customer_id", "name", "country")
```

### DLT Data Quality Expectations
```python
@dlt.expect_all_or_drop({
    "valid_id": "customer_id > 0",
    "not_null_email": "email IS NOT NULL",
    "recent_data": "created_at > '2023-01-01'"
})
def clean_customers():
    return dlt.read("customers_bronze")
```

### Trigger DLT from Workflow
```python
{
    "task_key": "dlt_task",
    "pipeline_task": {
        "pipeline_id": "pipeline-abc123"
    }
}

# Or trigger manually
w.pipelines.start_update(pipeline_id="pipeline-abc123")
```

---

## Monitoring & Troubleshooting

### View Job Runs
```python
# List recent runs
runs = w.jobs.list_runs(job_id=123, limit=10)
for run in runs:
    print(f"Run {run.run_id}: {run.state}")

# Get specific run
run = w.jobs.get_run(run_id=456)
print(f"Status: {run.state}")
print(f"Started: {run.start_time}")
print(f"Duration: {run.end_time - run.start_time}")
```

### Check Task Logs
```python
# Get run output
run_output = w.jobs.get_run_output(run_id=456)
print(run_output.notebook_output.result)

# Stream task logs
task_id = 123
logs = w.jobs.get_run_task(run_id=456, task_key="extract_customers")
```

### Monitor Pipeline
```python
# Get pipeline status
pipeline = w.pipelines.get(pipeline_id="pipe-123")
print(f"State: {pipeline.state}")

# List recent updates
updates = w.pipelines.list_updates(pipeline_id="pipe-123", limit=5)
for update in updates:
    print(f"Update {update.update_id}: {update.state}")
```

---

## Common Patterns

### Incremental Load Pattern
```python
# Task 1: Get last processed timestamp
{
    "task_key": "get_checkpoint",
    "notebook_task": {
        "notebook_path": "/Shared/get_checkpoint",
        "base_parameters": {"table_name": "customers"}
    }
}

# Task 2: Extract new data
{
    "task_key": "extract_incremental",
    "depends_on": [{"task_key": "get_checkpoint"}],
    "notebook_task": {
        "notebook_path": "/Shared/extract",
        "base_parameters": {
            "last_timestamp": "{{tasks.get_checkpoint.values.last_timestamp}}"
        }
    }
}
```

### Parallel Ingestion with Merge
```python
{
    "name": "multi_source_etl",
    "tasks": [
        {
            "task_key": "extract_source_a",
            "notebook_task": {"notebook_path": "/Shared/extract_a"}
        },
        {
            "task_key": "extract_source_b",
            "notebook_task": {"notebook_path": "/Shared/extract_b"}
        },
        {
            "task_key": "merge_sources",
            "depends_on": [
                {"task_key": "extract_source_a"},
                {"task_key": "extract_source_b"}
            ],
            "notebook_task": {"notebook_path": "/Shared/merge"}
        }
    ]
}
```

### Quality Gate Pattern
```python
{
    "task_key": "validate_quality",
    "notebook_task": {"notebook_path": "/Shared/quality_check"},
    "on_success": [{"task_key": "publish_data"}],
    "on_failure": [{"task_key": "notify_failure"}]
}
```
