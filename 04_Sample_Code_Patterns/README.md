# 💻 Sample Code Patterns

Production-ready code examples for common data engineering scenarios.

## 📂 Files in This Folder

### **Sample_Code_Common_Patterns.md**

**When:** Building actual pipelines, need proven patterns  
**Size:** 2,000+ lines of production-ready code  
**Languages:** SQL, Python, configuration

---

## 🎯 9 Complete Patterns Included

### 1. **Bronze → Silver → Gold ETL Pipeline**
**Use case:** Transform raw data to analytics-ready  
**Includes:**
- Extract to bronze notebook
- Transform to silver notebook
- Aggregate to gold notebook
- Full notebook code with explanations

**When to use:**
- Building data warehouse
- Creating transformation workflows
- Starting new data pipeline

---

### 2. **Delta Live Tables (DLT) Pipeline**
**Use case:** Modern, declarative data pipeline  
**Includes:**
- Bronze layer (raw ingestion)
- Silver layer (cleaning & validation)
- Gold layer (aggregations)
- Data quality expectations
- Monitoring tables

**When to use:**
- Need built-in data quality
- Want automatic incremental updates
- Prefer declarative over imperative

---

### 3. **Data Quality Monitoring Framework**
**Use case:** Automated quality checks  
**Includes:**
- Quality checks notebook
- Results tracking table
- Alert configuration
- Dashboard ready

**When to use:**
- Ensure data reliability
- Track quality over time
- Early problem detection

---

### 4. **Incremental Load with Checkpoint**
**Use case:** Only load new data since last run  
**Includes:**
- Checkpoint tracking
- Last load timestamp logic
- Incremental extraction
- Checkpoint updates

**When to use:**
- Large source systems
- Need fast load times
- Minimize data movement

---

### 5. **Conditional Workflow Logic**
**Use case:** Data quality gate before publishing  
**Includes:**
- Quality validation
- Pass/fail decision logic
- Success/failure handlers
- Conditional branching

**When to use:**
- Ensure data before publishing
- Prevent bad data propagation
- Workflow control

---

### 6. **Data Lineage Tracking**
**Use case:** Track data flow from source to destination  
**Includes:**
- Lineage logging
- Table dependencies
- Transformation types
- Query history

**When to use:**
- Impact analysis
- Compliance reporting
- Troubleshooting data issues

---

### 7. **Error Handling & Retry Logic**
**Use case:** Resilient, production-grade pipelines  
**Includes:**
- Try-catch patterns
- Retry with backoff
- Error logging
- Failure notifications

**When to use:**
- Critical production pipelines
- Unreliable source systems
- Need high reliability

---

### 8. **Masking PII Data**
**Use case:** Protect sensitive information  
**Includes:**
- PII detection
- Masking functions
- Role-based visibility
- Compliance checks

**When to use:**
- Handle customer data
- Meet privacy regulations
- External data sharing

---

### 9. **Data Validation Framework**
**Use case:** Reusable quality validation  
**Includes:**
- Generic validation rules
- Not-null checks
- Range checks
- Uniqueness checks
- Custom rules

**When to use:**
- Scale quality checks
- Multiple similar datasets
- Reusable rules

---

## 🚀 How to Use These Patterns

### Step 1: Find Your Pattern
Look through the 9 patterns and find the one that matches your use case.

### Step 2: Copy the Code
Copy the complete code from the pattern into your notebook.

### Step 3: Customize
- Replace table names with yours
- Adjust column names
- Modify logic as needed
- Add comments

### Step 4: Test
- Run on small dataset first
- Verify output
- Check for errors
- Optimize if needed

### Step 5: Deploy
- Move to production cluster
- Schedule if needed
- Set up monitoring
- Document for team

---

## 📊 Pattern Comparison

| Pattern | Language | Complexity | Time to Deploy |
|---------|----------|-----------|----------------|
| 1. Bronze/Silver/Gold | SQL + Python | ⭐⭐ | 2-4 hours |
| 2. DLT Pipeline | Python | ⭐⭐ | 1-2 hours |
| 3. Quality Monitoring | SQL + Python | ⭐⭐⭐ | 4-6 hours |
| 4. Incremental Load | SQL + Python | ⭐⭐⭐ | 2-3 hours |
| 5. Quality Gate | Python | ⭐ | 1-2 hours |
| 6. Lineage Tracking | SQL + Python | ⭐⭐ | 2-3 hours |
| 7. Error Handling | Python | ⭐⭐ | 1-2 hours |
| 8. PII Masking | SQL | ⭐⭐ | 2-3 hours |
| 9. Validation Framework | Python | ⭐⭐⭐ | 3-4 hours |

---

## 🎯 Quick Selection Guide

**Q: I need to transform raw data to analytics**
→ Pattern 1: Bronze/Silver/Gold

**Q: I want built-in data quality**
→ Pattern 2: DLT Pipeline

**Q: I need to monitor data quality**
→ Pattern 3: Quality Monitoring

**Q: My source data is huge, need fast loads**
→ Pattern 4: Incremental Load

**Q: I need to validate data before publishing**
→ Pattern 5: Quality Gate

**Q: I need to track data lineage**
→ Pattern 6: Lineage Tracking

**Q: I need robust error handling**
→ Pattern 7: Error Handling

**Q: I need to hide sensitive data**
→ Pattern 8: PII Masking

**Q: I need reusable validation rules**
→ Pattern 9: Validation Framework

---

## 💡 Pro Tips for Using Patterns

✅ **DO:**
- Understand the pattern before copying
- Customize for your specific needs
- Add error handling for production
- Monitor after deployment
- Document your implementation

❌ **DON'T:**
- Copy-paste without modifications
- Use without understanding the code
- Deploy without testing
- Ignore security implications
- Skip documentation

---

## 🔄 Pattern Combinations

Common combinations for real-world scenarios:

### Scenario 1: Daily Customer Sync
- Pattern 4 (Incremental Load)
- Pattern 1 (Bronze/Silver/Gold)
- Pattern 3 (Quality Monitoring)
- Pattern 5 (Quality Gate)

### Scenario 2: Real-Time Analytics
- Pattern 2 (DLT Pipeline)
- Pattern 3 (Quality Monitoring)
- Pattern 6 (Lineage Tracking)

### Scenario 3: High-Compliance Environment
- Pattern 1 (Bronze/Silver/Gold)
- Pattern 8 (PII Masking)
- Pattern 7 (Error Handling)
- Pattern 6 (Lineage Tracking)

### Scenario 4: Enterprise Data Platform
- Pattern 2 (DLT Pipeline)
- Pattern 4 (Incremental Load)
- Pattern 9 (Validation Framework)
- Pattern 3 (Quality Monitoring)
- Pattern 6 (Lineage Tracking)

---

## 🧪 Testing Patterns

Before using in production:

1. **Unit Testing:** Test individual functions
2. **Integration Testing:** Test with real data
3. **Edge Cases:** Test with nulls, duplicates, extreme values
4. **Performance:** Test with expected data volume
5. **Security:** Verify access controls work
6. **Monitoring:** Verify alerts trigger correctly

---

## 📈 Evolution Path

**Start with:**
→ Pattern 1 (Basic ETL) or Pattern 2 (DLT)

**Add:**
→ Pattern 3 (Quality Monitoring)

**Add:**
→ Pattern 5 (Quality Gate) & Pattern 6 (Lineage)

**Add:**
→ Patterns 4, 7, 8, 9 as needs grow

---

## 🔗 Related Folders

- **`05_Hands_On_Exercises/`** - Exercises teach fundamentals
- **`02_Cheatsheets/`** - Syntax reference while coding
- **`03_Guides_Best_Practices/`** - When to use which pattern
- **`06_Labs/`** - Step-by-step guided implementation
- **`01_Learning_Plan/`** - Understand when to use patterns

---

## 📚 Learning by Pattern

### Week 1-2: Start with Pattern 1 or 2
Choose based on your preference:
- **Pattern 1:** If you like SQL
- **Pattern 2:** If you like declarative approach

### Week 3: Add Pattern 3
Implement quality monitoring to your pipeline.

### Week 4: Add Patterns 5 & 6
Add validation gates and lineage tracking.

### Week 5+: Add Others as Needed
Patterns 4, 7, 8, 9 based on specific requirements.

---

**Use these patterns as starting templates for your production pipelines!** 🚀
