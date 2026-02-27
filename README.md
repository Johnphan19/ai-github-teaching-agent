# AI-Assisted GitHub Monitoring for Computational Courses

This project explores how AI-driven analytics can support computational teaching by analyzing GitHub repository activity. The goal is to help instructors identify patterns in student progress, such as steady work, inactivity, procrastination, or potential struggle—based on commit behavior over time.

**Independent Study Project** | University of Minnesota | Spring 2026

---

## Motivation

GitHub is widely used in computer science courses, but instructors often lack visibility into how students are progressing between deadlines. Students may be struggling for weeks before it shows up in assignment submissions or exam performance.

By analyzing commit histories and repository activity, this project aims to provide lightweight, interpretable signals that can help instructors offer support earlier and better understand student engagement and contribution patterns. The system automatically flags concerning behaviors like extended inactivity, procrastination, declining engagement, and unequal team contributions.

---

## Project Goals

- Analyze GitHub repository and commit activity over time
- Identify patterns such as steady progress, inactivity, procrastination, or sudden changes in behavior
- Detect team contribution imbalances in collaborative projects
- Prototype an AI-assisted monitoring agent for educational use
- Generate actionable recommendations for instructor intervention
- Produce a working prototype and accompanying documentation

---

## Pattern Detection

The monitoring agent identifies several key behavioral patterns:

| Pattern | Indicator | Action Level |
|---------|-----------|--------------|
| **Consistent Progress** | Regular commits (2-4/week), steady activity | ✅ Healthy - Continue monitoring |
| **Inactivity** | 14+ days between commits | 🚨 High - Immediate outreach needed |
| **Procrastination** | 60%+ commits in final third of course | ⚠️ Medium - Encourage earlier work |
| **Declining Activity** | Significant decrease over time | ⚠️ Medium - Check in with student |
| **Struggling Behavior** | Many small commits, irregular patterns | ⚠️ Medium - Review understanding |
| **Team Imbalance** | One member doing 60%+ or <10% of work | ⚠️ Medium - Address workload distribution |

---

## Technical Approach

**Pattern Detection Algorithms:**
- Activity pattern analysis (frequency, consistency, gaps)
- Commit quality metrics (size distribution, message quality)
- Temporal pattern analysis (work timing, deadline clustering)
- Weekly progress tracking with trend detection
- Team contribution balance analysis

**Configurable Thresholds:**
```
min_commits_per_week: 2
inactivity_days: 14
procrastination_threshold: 0.6 (60% in final third)
low_progress_threshold: 0.3 (30% of weeks active)
```

---

## Data Sources

This project uses multiple data sources for development and testing:

**Synthetic Data (Primary for Development):**
- Programmatically generated student commit patterns
- Includes 4 behavior types: consistent workers, procrastinators, struggling students, inactive students
- Realistic commit timing, sizes, and messages
- Safe for testing without privacy concerns

To keep the repository lightweight and reproducible, only sampled synthetic datasets are included. Raw data dumps are not committed to the repository.

---

## Research Foundation

This project builds on educational analytics research:

**"Analysis of Student Pair Teamwork Using GitHub Activities"** (Gitinabard et al.)
- Key insight: GitHub activity patterns correlate with team collaboration quality and individual engagement
- Application: Team contribution analysis and free rider detection

**"Explaining Explainability: Early Performance Prediction with Student Programming Pattern Profiling"** (Hoq et al.)
- Key insight: Programming patterns in early weeks predict final performance
- Application: Early warning system based on first 3-4 weeks of activity

These papers demonstrate that commit behavior is a reliable indicator of student engagement and can enable earlier intervention than traditional assessment methods.

---

## Privacy & Ethics

**Privacy Considerations:**
- Analyzes only commit metadata (timestamps, sizes, messages)
- Does not access code content or grades
- No personal information beyond GitHub username

**Ethical Use:**
- Students should be informed about monitoring
- Data used for support and intervention, not grading
- Instructor maintains final decision-making authority
- System provides insights to guide human judgment

---

## Technology Stack

- **Language:** Python 3.8+
- **Data Analysis:** statistics, datetime, collections
- **API Integration:** requests (GitHub REST API)
- **Testing:** pytest

---

## Future Work

- Visualization dashboard for instructors
- Machine learning for performance prediction
- Real-time monitoring and email alerts
- Multi-semester trend analysis
- Integration with learning management systems

---

## References

1. Gitinabard, N., et al. "Analysis of Student Pair Teamwork Using GitHub Activities"
2. Hoq, M., et al. "Explaining Explainability: Early Performance Prediction with Student Programming Pattern Profiling"

---

## Contact

**Author:** John Phan  
**Email:** [phan0282@umn.edu]  
**Advisor:** [Liia Butler]  
**Institution:** University of Minnesota  
**Semester:** Spring 2026

---

*This project aims to support better CS education through data-driven insights while respecting student privacy and promoting early intervention.*
