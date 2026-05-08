# 🔬 Hands-On Labs

Structured, guided laboratories for practical learning.

## 📂 Files in This Folder

### **Lab_Hands_On_Exercises.md**
4 comprehensive labs (8-12 hours total) with step-by-step instructions.

---

## 🧪 Lab Overview

### Lab 1: Delta Lake Fundamentals (1-2 hours)
**Objective:** Master Delta Lake basics

**What you'll do:**
- Create Bronze table with raw data
- Explore Delta log and time travel
- Perform ACID operations (UPDATE, DELETE, MERGE)
- Test schema evolution
- Restore table to previous version

**Skills gained:**
- Creating Delta tables
- Time travel queries
- ACID transactions
- Schema changes
- Version management

**Prerequisites:** None

---

### Lab 2: Unity Catalog & Data Governance (2-3 hours)
**Objective:** Set up enterprise data governance

**What you'll do:**
- Create catalog/schema hierarchy
- Build Bronze/Silver/Gold tables
- Apply tags and classifications
- Configure access control (RBAC)
- Track lineage
- Implement row/column security

**Skills gained:**
- Catalog structure design
- Access management
- Data tagging
- Security policies
- Lineage tracking

**Prerequisites:** Lab 1

---

### Lab 3: Data Orchestration with Workflows (2-3 hours)
**Objective:** Build production pipelines

**What you'll do:**
- Create extraction notebook
- Create transformation notebook
- Create load notebook
- Define task dependencies
- Pass parameters between tasks
- Configure scheduling
- Monitor workflow runs

**Skills gained:**
- Workflow creation
- Task definitions
- Parameter passing
- Dependency management
- Monitoring and debugging

**Prerequisites:** Lab 1

---

### Lab 4: Delta Live Tables Pipeline (2-3 hours)
**Objective:** Build modern data pipelines with DLT

**What you'll do:**
- Create DLT pipeline notebook
- Define Bronze/Silver/Gold tables
- Set data quality expectations
- Deploy pipeline
- Monitor execution
- View lineage

**Skills gained:**
- DLT pipeline design
- Data quality expectations
- Incremental updates
- Pipeline monitoring
- Lineage visualization

**Prerequisites:** Labs 1-3

---

## 📈 Lab Progression

```
Lab 1: Understand Delta Lake
   ↓
Lab 2: Apply governance concepts
   ↓
Lab 3: Build end-to-end pipelines
   ↓
Lab 4: Master modern patterns
```

Each lab builds on previous ones.

---

## ⏱️ Time Commitment

- **Lab 1:** 1-2 hours
- **Lab 2:** 2-3 hours
- **Lab 3:** 2-3 hours
- **Lab 4:** 2-3 hours
- **Total:** 8-12 hours

---

## 🎯 Lab Completion Checklist

### Lab 1 Complete?
- [ ] Created Delta table with sample data
- [ ] Queried different versions with time travel
- [ ] Performed UPDATE, DELETE, MERGE operations
- [ ] Added new column (schema evolution)
- [ ] Restored to previous version
- [ ] Screenshots of results saved

### Lab 2 Complete?
- [ ] Created catalog/schema structure
- [ ] Built Bronze/Silver/Gold tables
- [ ] Applied tags to columns
- [ ] Configured RBAC permissions
- [ ] Tracked lineage
- [ ] Tested row/column security

### Lab 3 Complete?
- [ ] Created 3 notebooks (extract, transform, load)
- [ ] Set up multi-task workflow
- [ ] Passed parameters between tasks
- [ ] Configured schedule
- [ ] Triggered manual run
- [ ] Monitored execution successfully

### Lab 4 Complete?
- [ ] Created DLT pipeline notebook
- [ ] Deployed pipeline successfully
- [ ] Verified expectations working
- [ ] Monitored pipeline run
- [ ] Viewed lineage information
- [ ] Updated pipeline and ran again

---

## 💡 Lab Tips

### Before Starting Labs
✅ **DO:**
- Read the lab description
- Check prerequisites
- Gather requirements
- Plan your approach

❌ **DON'T:**
- Skip setup steps
- Assume you know what to do
- Skip reading instructions

### During Labs
✅ **DO:**
- Follow steps in order
- Test each step
- Take screenshots
- Document issues
- Ask questions

❌ **DON'T:**
- Jump ahead
- Skip verification
- Ignore error messages
- Copy-paste blindly

### After Each Lab
✅ **DO:**
- Review what you learned
- Document key takeaways
- Note challenges faced
- Save artifacts
- Celebrate progress!

---

## 🔗 Lab Integration

Labs work together with other materials:

| Lab | Related Learning |
|-----|-----------------|
| Lab 1 | `02_Cheatsheets/Cheatsheet_Databricks_Basics.md` |
| Lab 2 | `02_Cheatsheets/Cheatsheet_Unity_Catalog.md` |
| Lab 3 | `02_Cheatsheets/Cheatsheet_Workflows_Orchestration.md` |
| Lab 4 | `02_Cheatsheets/Cheatsheet_Workflows_Orchestration.md` |
| All | `03_Guides_Best_Practices/` |

---

## 🎓 Learning Outcomes

### After All Labs, You Can:

- ✅ Create and manage Delta tables
- ✅ Design enterprise catalog structure
- ✅ Implement governance and security
- ✅ Build multi-task workflows
- ✅ Create DLT pipelines
- ✅ Monitor and troubleshoot pipelines
- ✅ Track data lineage
- ✅ Handle errors and retries
- ✅ Understand Databricks architecture
- ✅ Speak with confidence about data engineering

---

## 📊 Difficulty Progression

```
Lab 1: ⭐ Beginner
Lab 2: ⭐⭐ Intermediate
Lab 3: ⭐⭐⭐ Advanced
Lab 4: ⭐⭐⭐ Advanced
```

Each lab assumes knowledge from previous labs.

---

## 🚀 What's Next After Labs?

1. **Create Capstone Project:**
   - Design complete data platform
   - Implement all concepts learned
   - 50+ tables, multiple pipelines

2. **Apply to Real Data:**
   - Use company data (if available)
   - Build production pipelines
   - Deploy to real environment

3. **Add Complexity:**
   - Implement additional patterns
   - Add advanced optimizations
   - Scale to larger data

4. **Share & Teach:**
   - Document your implementation
   - Train team members
   - Contribute best practices

---

## 📝 Lab Documentation Template

For each lab, document:

```
Lab #: [Name]
Date: [Date]
Duration: [Time spent]

What I Learned:
- [Key concept 1]
- [Key concept 2]
- [Key concept 3]

Challenges Faced:
- [Challenge 1] → Solution
- [Challenge 2] → Solution

Key Takeaways:
- [Important point 1]
- [Important point 2]

Next Steps:
- [What to do next]
```

---

## ✨ Success Criteria for Each Lab

### Lab 1 Success
✅ Can create Delta tables  
✅ Understand time travel  
✅ Know ACID operations  
✅ Can modify schema  

### Lab 2 Success
✅ Can design catalog structure  
✅ Understand governance patterns  
✅ Can implement security  
✅ Know lineage concepts  

### Lab 3 Success
✅ Can create workflows  
✅ Understand dependencies  
✅ Can pass parameters  
✅ Know orchestration patterns  

### Lab 4 Success
✅ Can build DLT pipelines  
✅ Understand data quality expectations  
✅ Can monitor pipelines  
✅ Know modern data patterns  

---

**Ready? Start with Lab 1!** 🧪
