# SQL & Python Exercises - Complete Guide

## 📂 Files Generated

### 1. **Exercises_SQL.sql**
- **File Type:** SQL script for Databricks SQL editor/notebook
- **Exercises:** 40+ with progressive difficulty
- **Lines of Code:** 500+
- **Topics Covered:**
  - Basic SELECT, WHERE, ORDER BY
  - Aggregations and GROUP BY
  - JOINs (INNER, LEFT, FULL)
  - Subqueries and CTEs
  - Window functions
  - Delta Lake operations
  - Data quality checks
  - Business queries
  - Performance optimization

### 2. **Exercises_Python_PySpark.py**
- **File Type:** Python script for Databricks notebooks
- **Exercises:** 50+ with progressive difficulty
- **Lines of Code:** 700+
- **Topics Covered:**
  - DataFrame creation and selection
  - Filtering and transformations
  - Aggregations and GROUP BY
  - Window functions
  - JOINs (INNER, LEFT, FULL)
  - String operations
  - Type conversions
  - Data quality checks
  - File I/O (Delta, Parquet, CSV)
  - ETL patterns (Bronze/Silver/Gold)
  - Performance optimization
  - Business logic
  - RFM analysis, segmentation

---

## 🏃 Quick Start

### For SQL Exercises:
```
1. Open Databricks SQL editor or SQL notebook
2. Copy-paste Exercise sections
3. Run each exercise one at a time
4. Modify to test your understanding
5. Progress from Section 1 → Section 7
```

### For Python Exercises:
```
1. Create new Databricks notebook
2. Copy import statements from Section 11
3. Run each exercise cell
4. Expected output shown in comments
5. Challenges don't have solutions - write your own!
```

---

## 📊 Exercise Breakdown

### SQL Exercises (Exercises_SQL.sql)

#### Section 1: Basic SQL (8 exercises)
- SELECT, WHERE, ORDER BY
- COUNT, SUM, AVG, MIN, MAX
- GROUP BY with HAVING
- **Time:** 30-45 minutes
- **Prerequisites:** None

#### Section 2: Intermediate (6 exercises)
- INNER/LEFT JOIN
- Subqueries in WHERE and FROM
- Common Table Expressions (CTEs)
- Multiple CTEs
- **Time:** 1-2 hours
- **Prerequisites:** Section 1

#### Section 3: Advanced (5 exercises)
- ROW_NUMBER, RANK, DENSE_RANK
- Running totals and window functions
- LAG/LEAD functions
- PERCENT_RANK
- **Time:** 1-2 hours
- **Prerequisites:** Sections 1-2

#### Section 4: Delta Lake (5 exercises)
- Creating Delta tables
- UPDATE operations
- MERGE (upsert)
- DELETE operations
- Time travel
- **Time:** 1-2 hours
- **Prerequisites:** Sections 1-2

#### Section 5: Data Quality (4 exercises)
- Finding NULL values
- Duplicate detection
- Data type validation
- Completeness checks
- **Time:** 45-60 minutes
- **Prerequisites:** Sections 1-2

#### Section 6: Business Queries (3 exercises)
- Sales analysis
- Customer lifetime value
- Monthly trends
- **Time:** 1-2 hours
- **Prerequisites:** All previous

#### Section 7: Performance (2 exercises)
- EXPLAIN and query plans
- Partition pruning
- **Time:** 45-60 minutes
- **Prerequisites:** All previous

---

### Python/PySpark Exercises (Exercises_Python_PySpark.py)

#### Section 1: Basic DataFrames (8 exercises)
- DataFrame creation
- Column selection
- Filtering
- Adding/renaming columns
- Sorting and counting
- **Time:** 45-60 minutes
- **Prerequisites:** None

#### Section 2: Aggregations (6 exercises)
- GROUP BY operations
- Multiple aggregations
- Window functions (ROW_NUMBER, LAG/LEAD)
- Running totals
- **Time:** 1-2 hours
- **Prerequisites:** Section 1

#### Section 3: Joins (3 exercises)
- INNER JOIN
- LEFT JOIN
- Multiple joins
- **Time:** 45-60 minutes
- **Prerequisites:** Sections 1-2

#### Section 4: String & Types (4 exercises)
- String manipulation (upper, lower, substring)
- String concatenation
- Conditional logic (CASE/WHEN)
- Type conversions
- **Time:** 1 hour
- **Prerequisites:** Sections 1-2

#### Section 5: Data Quality (5 exercises)
- NULL value detection
- Filling NULLs
- Data validation
- Deduplication
- Completeness checks
- **Time:** 1-2 hours
- **Prerequisites:** Sections 1-3

#### Section 6: File I/O (4 exercises)
- Write to Delta
- Read from Delta
- Write Parquet
- Export CSV
- **Time:** 30-45 minutes
- **Prerequisites:** Section 5

#### Section 7: ETL Patterns (3 exercises)
- Bronze → Silver transformation
- Silver → Gold aggregation
- Data quality framework
- **Time:** 1-2 hours
- **Prerequisites:** Sections 1-5

#### Section 8: Optimization (4 exercises)
- Caching
- Repartitioning
- Broadcast joins
- Query plan analysis
- **Time:** 1 hour
- **Prerequisites:** All previous

#### Section 9: Business Logic (3 exercises)
- Customer segmentation
- Sales trend analysis
- RFM analysis
- **Time:** 1-2 hours
- **Prerequisites:** All previous

#### Sections 10: Challenges (5 challenges)
- No solutions provided
- Write your own implementations
- Apply all learned concepts
- **Time:** 3-5 hours
- **Prerequisites:** All sections

---

## 📈 Recommended Learning Path

### Week 1: SQL Fundamentals
```
Day 1-2: SQL Sections 1-2 (Basic & Intermediate)
Day 3-4: SQL Section 3 (Advanced)
Day 5: Practice and challenges from Sections 1-3
```

### Week 2: SQL Advanced
```
Day 1-2: SQL Sections 4-5 (Delta Lake & Quality)
Day 3-4: SQL Sections 6-7 (Business & Performance)
Day 5: Practice all sections
```

### Week 3: Python/PySpark Basics
```
Day 1-2: Python Sections 1-3 (DataFrames & Joins)
Day 3-4: Python Sections 4-5 (Strings & Quality)
Day 5: Practice Sections 1-5
```

### Week 4: Python/PySpark Advanced
```
Day 1: Python Sections 6-8 (I/O, ETL, Optimization)
Day 2-3: Python Section 9 (Business Logic)
Day 4-5: Python Section 10 (Challenges)
```

---

## 🎯 Learning Objectives by Exercise

### SQL Exercises

| Exercise | Objective | Difficulty |
|----------|-----------|-----------|
| 1.1-1.3 | Understand SELECT, WHERE, filtering | ⭐ |
| 1.4-1.7 | GROUP BY, aggregations, ORDER BY | ⭐⭐ |
| 2.1-2.2 | JOIN operations | ⭐⭐ |
| 2.3-2.6 | Subqueries and CTEs | ⭐⭐⭐ |
| 3.1-3.5 | Window functions | ⭐⭐⭐ |
| 4.1-4.5 | Delta Lake operations & time travel | ⭐⭐ |
| 5.1-5.4 | Data quality checks | ⭐⭐ |
| 6.1-6.3 | Business analytics queries | ⭐⭐⭐ |
| 7.1-7.2 | Query optimization | ⭐⭐⭐ |

### Python Exercises

| Exercise | Objective | Difficulty |
|----------|-----------|-----------|
| 1.1-1.8 | DataFrame basics | ⭐ |
| 2.1-2.6 | Aggregations & window functions | ⭐⭐ |
| 3.1-3.3 | JOIN operations | ⭐⭐ |
| 4.1-4.4 | String & type operations | ⭐⭐ |
| 5.1-5.5 | Data quality operations | ⭐⭐ |
| 6.1-6.4 | File I/O operations | ⭐⭐ |
| 7.1-7.3 | ETL patterns | ⭐⭐⭐ |
| 8.1-8.4 | Performance optimization | ⭐⭐⭐ |
| 9.1-9.3 | Business logic | ⭐⭐⭐ |
| 10.1-10.5 | Comprehensive challenges | ⭐⭐⭐⭐ |

---

## 💡 How to Use These Files

### Approach 1: Learn SQL First
```
Week 1-2: Complete all SQL exercises
Week 3-4: Complete all Python exercises
Week 5: Apply both to real projects
```

### Approach 2: Parallel Learning
```
Week 1: SQL Sections 1-2 + Python Sections 1-2
Week 2: SQL Sections 3-4 + Python Sections 3-5
Week 3: SQL Sections 5-7 + Python Sections 6-9
Week 4: Challenges for both
```

### Approach 3: Test-Driven
```
1. Read exercise description
2. Attempt to write solution
3. Check provided solution if stuck
4. Modify and experiment
5. Move to next exercise
```

---

## ✅ Self-Assessment Checklist

### After SQL Exercises
- [ ] Can write SELECT with WHERE and ORDER BY
- [ ] Understand GROUP BY and aggregations
- [ ] Can write complex JOINs
- [ ] Understand subqueries and CTEs
- [ ] Can use window functions
- [ ] Understand Delta Lake operations
- [ ] Can perform data quality checks
- [ ] Can write business analytics queries

### After Python Exercises
- [ ] Can create and manipulate DataFrames
- [ ] Understand PySpark aggregations
- [ ] Can write JOINs in PySpark
- [ ] Understand string and type operations
- [ ] Can perform data quality operations
- [ ] Can read/write different file formats
- [ ] Understand ETL patterns
- [ ] Can optimize PySpark code
- [ ] Can apply business logic
- [ ] Can solve challenges independently

---

## 🔗 Integration with Other Materials

These exercises are designed to work with:

1. **Learning Plan**
   - SQL exercises align with Phase 1-3
   - Python exercises align with Phase 1-3
   - Use together for comprehensive learning

2. **Sample Code Patterns**
   - Exercises teach fundamentals
   - Sample code shows production patterns
   - Challenges bridge the gap

3. **Cheatsheets**
   - Reference cheatsheet while coding
   - Use for syntax when stuck
   - Understand concepts more deeply

4. **Labs**
   - Labs provide step-by-step guidance
   - Exercises provide independent practice
   - Labs are more structured, exercises more open-ended

---

## 🚀 Tips for Success

### SQL Tips
```
✅ DO:
- Run each exercise one at a time
- Modify to test your understanding
- Write your own variations
- Check result expectations
- Use EXPLAIN to understand plans

❌ DON'T:
- Copy-paste without understanding
- Skip exercises
- Move to advanced before mastering basics
- Ignore error messages
```

### Python Tips
```
✅ DO:
- Run each code block separately
- Print intermediate results
- Use .display() to see DataFrames
- Experiment with transformations
- Build on previous exercises

❌ DON'T:
- Run entire file at once
- Skip import statements
- Ignore schema errors
- Copy without understanding
```

---

## 📝 Challenge Hints

### SQL Challenges
1. **Complex aggregation:** Group, aggregate, then filter results
2. **Multi-step transformation:** Use CTEs to break into steps
3. **Ranking with ties:** Use DENSE_RANK instead of RANK
4. **Data reconciliation:** Use EXCEPT or anti-join techniques
5. **Year-over-year:** Use window functions with DATE_TRUNC

### Python Challenges
1. **Multi-level aggregation:** Chain groupBy().agg() operations
2. **Anomaly detection:** Calculate mean/stddev, filter outliers
3. **Churn prediction:** Combine multiple conditions with &/|
4. **Data reconciliation:** Use leftanti joins to find differences
5. **Dynamic schema:** Use spark.read.csv with inferSchema

---

## 🎓 After Completing Exercises

### Next Steps
1. **Apply to Real Data:** Try these on actual company data
2. **Combine SQL & Python:** Solve same problem both ways
3. **Optimize:** Re-write exercises for performance
4. **Document:** Create comments explaining complex logic
5. **Share:** Show solutions to colleagues/team
6. **Extend:** Create variations and additional exercises

### Build Your Own
```
1. Take a business problem
2. Break into SQL queries
3. Implement in Python/PySpark
4. Optimize both
5. Document approach
6. Present findings
```

---

## 📞 Getting Help

### If You're Stuck:
1. **Read the comment:** Explains what to do
2. **Check expected output:** See what should happen
3. **Use EXPLAIN:** Understand query plan
4. **Reference cheatsheet:** Check syntax
5. **Modify incrementally:** Change one thing at a time
6. **Check data:** Verify input data is correct

### Common Issues:
- **Syntax errors:** Check cheatsheet for correct syntax
- **Wrong results:** Review WHERE/HAVING conditions
- **NULL issues:** Remember NULL != anything (use IS NULL)
- **Join problems:** Verify join keys and table relationships
- **Performance:** Check for full table scans vs partition pruning

---

## 📊 Progress Tracking

### Create a checklist:
```
Section 1: ☐☐☐☐☐☐☐☐ (8 exercises)
Section 2: ☐☐☐☐☐☐ (6 exercises)
Section 3: ☐☐☐☐☐ (5 exercises)
...
Challenges: ☐☐☐☐☐ (5 challenges)
```

### Track your speed:
```
Beginner: 15-20 min per exercise
Intermediate: 10-15 min per exercise
Advanced: 5-10 min per exercise
```

---

**Good luck with your SQL and Python learning! Remember: consistency beats intensity!** 💪
