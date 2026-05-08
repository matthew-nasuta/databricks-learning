# 📖 Guides & Best Practices

Strategic guidance for making the right technical decisions.

## 📂 Files in This Folder

### **BestPractices_Troubleshooting_Guide.md**

**When:** Making architectural decisions, debugging issues  
**Contains:** 3,000+ lines of guidance for:

#### Part 1: Best Practices
- **Data Modeling:** Medallion architecture, partitioning, bucketing
- **Code Quality:** Comments, naming conventions, versioning
- **Performance:** Caching, joins, filter pushdown optimization
- **Data Governance:** Tagging, security, documentation
- **Orchestration:** Error handling, monitoring, patterns

#### Part 2: Troubleshooting
- **8 Common Issues** with solutions:
  1. RESOURCE_NOT_FOUND
  2. PERMISSION_DENIED
  3. Out of Memory
  4. Query Timeout
  5. Schema Mismatch
  6. External Location Invalid
  7. Circular Dependency
  8. Task Values Not Accessible

- **Debugging Techniques:**
  - Using EXPLAIN
  - Enabling verbose logging
  - Profiling data processing
  - Testing incrementally
  - Monitoring cluster performance

- **Monitoring & Performance Tuning Checklists**

---

## 🎯 How to Use This Folder

### When Making Decisions
→ Reference **Best Practices** section  
*Example: "How should I structure my data lake?" → Read Data Modeling Best Practices*

### When Something Goes Wrong
→ Check **Troubleshooting** section  
*Example: "Got PERMISSION_DENIED error" → Find that error & solution*

### When Optimizing
→ Check **Performance Best Practices**  
*Example: "Query is slow" → Use optimization checklist*

### When Setting Up Governance
→ Check **Data Governance Best Practices**  
*Example: "How to tag sensitive data?" → Follow governance guidelines*

---

## 📋 Best Practices Checklist

### Data Modeling
- [ ] Using medallion architecture (bronze/silver/gold)
- [ ] All tables are Delta format
- [ ] Partitions chosen strategically
- [ ] Z-order applied where needed
- [ ] Naming conventions documented

### Code Quality
- [ ] Code is commented (especially complex logic)
- [ ] Naming conventions followed consistently
- [ ] Version info in code headers
- [ ] No magic numbers (use named constants)
- [ ] Error handling implemented

### Performance
- [ ] Expensive DataFrames cached
- [ ] Small tables broadcast in joins
- [ ] Filters pushed down early
- [ ] Appropriate partitioning used
- [ ] Query plans analyzed with EXPLAIN

### Governance
- [ ] All sensitive data tagged
- [ ] Row/column security configured
- [ ] Table documentation complete
- [ ] Lineage tracking enabled
- [ ] Audit logs reviewed

### Orchestration
- [ ] Tasks have clear dependencies
- [ ] Error handling and retries configured
- [ ] Parameters used for flexibility
- [ ] Job health monitored
- [ ] Runbooks documented

---

## 🔧 Troubleshooting Quick Reference

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| RESOURCE_NOT_FOUND | Wrong path or object doesn't exist | Use full path: catalog.schema.table |
| PERMISSION_DENIED | Insufficient access | Ask admin to grant permissions |
| Out of Memory | Too much data or inefficient code | Optimize queries, add workers, partition data |
| Query Timeout | Query too slow | Add filters, use partitions, check join strategy |
| Schema Mismatch | Column types don't match | Verify types, use CAST, enable mergeSchema |
| Invalid External Location | Bad path format or credentials | Check S3/ADLS path, verify IAM permissions |
| Circular Dependency | Tasks reference each other | Redraw dependency chain, use separate jobs |
| Task Values Not Accessible | Wrong task key or value not set | Verify task_key matches, ensure value was set |

---

## 💡 Decision Trees

### "My query is slow. What do I do?"

1. Run EXPLAIN
   ├─ Check for full table scans → Add partition filter
   ├─ Check join strategy → Use broadcast for small tables
   └─ Check shuffle → Repartition data

2. Profile the data
   ├─ Row count acceptable? → Look at join/aggregation
   └─ Row count huge? → Add more aggressive filters

3. Optimize
   ├─ Add Z-order → Recreate index
   ├─ Cache results → Use for repeated operations
   └─ Repartition → Match query patterns

---

### "What governance should I implement?"

1. **Immediate:**
   - [ ] Tag all sensitive columns
   - [ ] Document all tables
   - [ ] Set up RBAC

2. **Short-term:**
   - [ ] Enable row/column security
   - [ ] Set up audit logging
   - [ ] Create data quality checks

3. **Long-term:**
   - [ ] Implement data contracts
   - [ ] Automate lineage tracking
   - [ ] Set up compliance monitoring

---

## 🚨 Red Flags

Watch for these issues:

❌ **Architecture:**
- Single flat table structure
- No partitioning
- Everything in one cluster
- No data quality checks

❌ **Code Quality:**
- Hardcoded values
- No comments
- No error handling
- Copy-pasted code

❌ **Performance:**
- Full table scans everywhere
- No caching
- Inefficient joins
- Skewed data

❌ **Governance:**
- No data tagging
- Everyone has admin access
- No audit logging
- Missing documentation

---

## ✅ Green Flags

These indicate good practices:

✅ **Architecture:**
- Medallion pattern implemented
- Strategic partitioning
- Auto-scaling configured
- Data quality frameworks

✅ **Code Quality:**
- Clear comments
- Consistent naming
- Version tracked
- Error handling

✅ **Performance:**
- Query plans reviewed
- Caching implemented
- Broadcasts used
- Optimized joins

✅ **Governance:**
- All sensitive data tagged
- RBAC configured
- Audit logs reviewed
- Documentation complete

---

## 🔗 Related Folders

- **`02_Cheatsheets/`** - Syntax reference
- **`01_Learning_Plan/`** - Strategic concepts
- **`04_Sample_Code_Patterns/`** - Implementation examples
- **`05_Hands_On_Exercises/`** - Practice applying principles
- **`06_Labs/`** - Guided implementations

---

## 📚 When to Reference This Guide

**Phase 1-3:** Focus on data modeling and code quality  
**Phase 4-6:** Focus on governance and optimization  
**Before production:** Full troubleshooting checklist  
**When stuck:** Troubleshooting section  
**For reviews:** Best practices checklist

---

**Use this guide to make better technical decisions and solve problems faster!** 🎯
