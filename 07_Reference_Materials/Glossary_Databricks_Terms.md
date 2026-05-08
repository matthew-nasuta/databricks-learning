# Databricks Data Engineering Glossary

## Core Concepts

**Apache Spark**
- Open-source distributed computing framework
- Powers Databricks data processing
- Processes data in parallel across clusters
- Primary languages: SQL, Python (PySpark), Scala, R

**Databricks**
- Cloud-based lakehouse platform built on Spark
- Combines data warehouse and data lake capabilities
- Provides unified interface for data engineering and analytics
- Available on AWS, Azure, GCP

**Delta Lake**
- Open-source storage layer for Databricks
- Adds ACID transactions to data lakes
- Provides time travel, schema enforcement, and data versioning
- Default table format in Databricks

**Lakehouse**
- Hybrid architecture combining data lake and data warehouse
- Offers scalability of lakes with structure of warehouses
- Supports both structured and unstructured data
- Example: Databricks platform

---

## Data Governance

**Catalog**
- Top-level container for organizing data in Unity Catalog
- Organizes data by business domain or team
- Example: `prod_analytics`, `marketing_data`, `finance_reporting`

**Schema**
- Container within a catalog for related tables/views
- Logically groups tables by functional area
- Example: `customer_data`, `transactions`, `metadata`

**Metastore**
- Centralized metadata repository
- Stores information about all catalogs, schemas, tables
- One per region
- Enables governance, lineage, and access control

**Unity Catalog (UC)**
- Databricks' centralized governance layer
- Provides RBAC, tagging, data lineage, audit logging
- Replaces older Hive Metastore
- Required for enterprise data governance

**Data Lineage**
- Track of data flow from source to destination
- Shows table-to-table dependencies
- Enables impact analysis (if I change this table, what else breaks?)
- Can be column-level or table-level

**PII (Personally Identifiable Information)**
- Data that can identify an individual (email, SSN, phone)
- Must be protected and restricted
- Examples: customer names, addresses, payment info

**Data Classification**
- Tagging/categorization of data by sensitivity level
- Example levels: public, internal, confidential, restricted
- Used to enforce access controls and compliance

**RBAC (Role-Based Access Control)**
- Grant permissions to users based on their role
- Roles: admin, analyst, engineer, read-only
- Permissions: SELECT, MODIFY, MANAGE_METADATA

**Row-Level Security**
- Restrict which rows users can see in a table
- Example: sales rep sees only their territory's data
- Implemented via row filters

**Column-Level Security**
- Restrict which columns users can see
- Example: HR sees salary, others don't
- Implemented via column masks

**Data Expectation**
- Defined quality rule for data (e.g., "no nulls", "values > 0")
- Used in DLT pipelines
- Tracks violations and quality metrics

---

## Data Lakehouse Architecture

**Bronze Layer** (Raw)
- Raw data as-is from source systems
- No transformations or cleaning
- Schema-on-read approach
- High volume, low quality

**Silver Layer** (Cleaned)
- Deduplicated, validated, enriched data
- Removed PII or applied masking
- Schema-on-write approach
- Medium volume, medium quality

**Gold Layer** (Refined)
- Business-ready analytics datasets
- Pre-aggregated or heavily processed
- Optimized for specific use cases
- Lower volume, high quality

**Medallion Architecture**
- Three-tier data architecture (bronze/silver/gold)
- Each tier has specific purpose and data quality
- Enables incremental refinement
- Standard best practice in data engineering

---

## Orchestration & Workflows

**Workflow** (or Job)
- Container for scheduled/triggered data pipeline tasks
- Can have multiple tasks with dependencies
- Runs on clusters/warehouses
- Managed by Databricks

**Task**
- Individual unit of work within a workflow
- Can be notebook, SQL, Python, or DLT pipeline
- Has dependencies on other tasks
- Can pass parameters and data between tasks

**DAG (Directed Acyclic Graph)**
- Graph representation of workflow/task dependencies
- Nodes = tasks, edges = dependencies
- Enables parallel execution when possible
- Visual way to understand data flow

**Trigger**
- Event that starts a workflow
- Types: schedule (cron), event-based (S3 arrival), manual
- Can be one-time or recurring

**Cron Expression**
- Unix-style scheduling syntax
- Example: `0 2 * * ? *` = 2 AM every day
- Used to schedule recurring workflows

**Task Dependencies**
- Relationships between tasks (which must complete first)
- Linear: A → B → C (sequential)
- Parallel: A and B run simultaneously, then C
- Enables optimization and failure handling

**Delta Live Tables (DLT)**
- Declarative framework for building data pipelines
- Define data transformations as SQL/Python functions
- Automatically handles incremental updates
- Built-in data quality expectations

**Expectation** (in DLT)
- Quality rule/assertion on data
- Example: "customer_id NOT NULL", "age > 0"
- Can drop, quarantine, or warn on violations
- Tracked in DLT metrics

---

## Data Quality & Monitoring

**Data Quality**
- Fitness of data for its intended purpose
- Dimensions: accuracy, completeness, consistency, timeliness
- Monitored via expectations and tests
- Critical for reliable analytics

**Anomaly Detection**
- Identifying unusual patterns in data
- Example: sudden drop in order volume
- Can trigger alerts or manual review
- Useful for early issue detection

**SLA (Service Level Agreement)**
- Commitment on data availability/quality
- Example: "data refreshed by 9 AM daily with <1% null values"
- Monitored and reported on

**Data Contract**
- Formal agreement on table/data structure
- Specifies schema, update frequency, quality expectations
- Enables self-service analytics
- Part of data mesh approach

**Audit Log**
- Record of who accessed/modified data
- Stored in Unity Catalog
- Required for compliance (GDPR, HIPAA, SOX)
- Enables troubleshooting and forensics

---

## Performance & Optimization

**Partitioning**
- Organizing table data into subdirectories by column value
- Example: partition by year/month
- Enables partition pruning (skip unneeded partitions)
- Improves query performance for filtered queries

**Bucketing** (or Clustering)
- Organizing data within partition using hash
- Improves join/group performance
- Similar to bucketing in Hive

**Z-Ordering** (Delta Lake)
- Multi-dimensional clustering technique
- Optimizes queries on multiple columns
- More efficient than traditional bucketing
- Recommended approach in Databricks

**Query Optimization**
- Techniques to improve query performance
- Examples: partition pruning, predicate pushdown, join reordering
- Monitored via query plans
- Measured by reduced execution time/cost

**Query Plan**
- Databricks' internal representation of how to execute query
- Logical plan: high-level operations
- Physical plan: specific execution strategy
- Viewable via `EXPLAIN` command

**Spark Configuration**
- Tuning parameters for Spark execution
- Examples: `spark.sql.shuffle.partitions`, `spark.default.parallelism`
- Can be set at cluster, job, or session level

---

## API & Integration

**REST API**
- HTTP-based interface for Databricks
- Enables programmatic job/cluster/data management
- Used for CI/CD integration
- Authentication via tokens or OAuth

**SDK** (Software Development Kit)
- Language-specific library for Databricks API
- Available for Python, Java, Scala
- Simplifies API usage vs. raw HTTP
- Example: `databricks-sdk-python`

**Connector**
- Integration between Databricks and external systems
- Examples: JDBC, ODBC, Spark connector
- Enables data movement and querying

**Lineage API**
- API to query table/column lineage
- Enables building custom lineage tools
- Part of system.access schema
- Returns lineage graph

---

## Compliance & Security

**GDPR** (General Data Protection Regulation)
- EU regulation on personal data
- Requires consent, data minimization, right to be forgotten
- Affects any system handling EU resident data

**HIPAA** (Health Insurance Portability & Accountability Act)
- US regulation on health data
- Requires encryption, access controls, audit logs
- Violations carry severe penalties

**SOX** (Sarbanes-Oxley)
- US regulation on financial data and reporting
- Requires access controls and audit trails
- Applies to public companies

**Data Retention Policy**
- Rules on how long to keep data
- Example: "Keep customer data for 5 years after deletion"
- Tracked and enforced via governance

**Encryption**
- Converting data to unreadable form
- At rest: encrypted in storage
- In transit: encrypted during transmission
- TLS for network, AES for storage

**Multi-tenancy**
- Sharing infrastructure while isolating customer data
- Each tenant can only see their own data
- Enforced via RBAC and row/column security

---

## Cloud Storage

**S3** (Simple Storage Service)
- AWS object storage
- Used with Databricks on AWS
- Accessed via s3:// paths

**ADLS** (Azure Data Lake Storage)
- Azure's object storage
- Used with Databricks on Azure
- Accessed via abfss:// paths

**GCS** (Google Cloud Storage)
- Google's object storage
- Used with Databricks on GCP
- Accessed via gs:// paths

**DBFS** (Databricks File System)
- Databricks' abstraction layer for cloud storage
- Maps to S3/ADLS/GCS
- Accessed via /dbfs/ paths

**External Location**
- Pointer to cloud storage path with credentials
- Part of Unity Catalog
- Used for external tables

---

## Common Acronyms

| Acronym | Meaning |
|---------|---------|
| ETL | Extract, Transform, Load |
| ELT | Extract, Load, Transform |
| ACID | Atomicity, Consistency, Isolation, Durability |
| PII | Personally Identifiable Information |
| RLS | Row-Level Security |
| RBAC | Role-Based Access Control |
| DLT | Delta Live Tables |
| DAG | Directed Acyclic Graph |
| SLA | Service Level Agreement |
| KPI | Key Performance Indicator |
| UI | User Interface |
| API | Application Programming Interface |
| SDK | Software Development Kit |
| CSV | Comma-Separated Values |
| JSON | JavaScript Object Notation |
| JDBC | Java Database Connectivity |
| ODBC | Open Database Connectivity |
| CTL | Control (audit/metadata table) |
| ODS | Operational Data Store |
