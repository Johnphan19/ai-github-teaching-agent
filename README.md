# AI-Assisted GitHub Monitoring for Computational Courses

This project explores how AI-driven analytics can support computational teaching by analyzing GitHub repository activity. The system identifies behavioral patterns in student development workflows to detect early signs of struggle, disengagement, or imbalance in collaboration.

**Independent Study Project**
University of Minnesota | Spring 2026

---

## 📌 Overview

In many computer science courses, GitHub is heavily used for assignments and projects. However, instructors often lack visibility into how students are progressing between deadlines. As a result, struggling students may go unnoticed until it is too late for meaningful intervention.

This project introduces an **AI-assisted monitoring agent** that analyzes commit histories and repository activity to generate interpretable insights about student behavior. The system detects patterns such as inactivity, procrastination, declining engagement, and uneven team contributions, enabling earlier and more targeted instructor support.

---

## 🎯 Project Goals

* Analyze GitHub repository and commit activity over time
* Identify behavioral patterns such as steady progress, inactivity, and procrastination
* Detect team contribution imbalances in collaborative environments
* Build an interpretable, rule-based AI monitoring system
* Generate actionable recommendations for instructor intervention
* Validate model performance and analyze feature effectiveness
* Provide visual insights into student behavior patterns

---

## 🧠 System Architecture

The monitoring agent consists of three main components:

### 1. Student Analysis Engine

* Activity pattern analysis (commit frequency, gaps, consistency)
* Temporal behavior (late-night work, procrastination)
* Progress tracking (weekly engagement trends)
* Commit quality evaluation

### 2. Team Analysis Engine

* Contribution distribution across members
* Detection of free-riding or dominant contributors
* Collaboration pattern analysis

### 3. Risk Classification System

* Rule-based scoring using configurable thresholds
* Severity levels: **none, low, medium, high**
* Flag-based explanations and recommendations for each student

---

## 🚨 Pattern Detection

The system identifies several key behavioral patterns:

| Pattern             | Indicator                       | Action Level |
| ------------------- | ------------------------------- | ------------ |
| Consistent Progress | Regular commits (2–4/week)      | ✅ Healthy    |
| Inactivity          | 14+ days between commits        | 🚨 High      |
| Procrastination     | 60%+ commits near deadline      | ⚠️ Medium    |
| Declining Activity  | Reduced activity over time      | ⚠️ Medium    |
| Struggling Behavior | Many small or irregular commits | ⚠️ Medium    |
| Team Imbalance      | >60% or <10% contribution       | ⚠️ Medium    |

---

## ⚙️ Technical Approach

### Feature Engineering

* **Activity Metrics:** consistency, average gap, max gap
* **Temporal Metrics:** late-night work ratio, procrastination indicator
* **Progress Metrics:** active weeks, commits per week
* **Quality Metrics:** commit size distribution, message quality

### Threshold-Based Modeling

* Tuned thresholds for key features:

  * max_gap ≈ 9 days (strongest predictor)
  * late_night ≈ 0.2
  * procrastination ≈ 0.4
* Used to classify students into severity levels

### Validation Framework

* Confusion matrix and classification report
* Accuracy: **~69%**
* Strong performance on:

  * High severity (precision: 0.95)
  * No-risk students (recall: 1.00)
* Weak performance on:

  * Low and medium severity (class overlap)

---

## 📊 Visualization & Insights

The project includes multiple visualizations to analyze feature behavior and model performance:

* **Feature Correlation Heatmap**

  * Strong negative correlation between consistency and inactivity (-0.81)
* **Max Gap vs Severity**

  * Clear separation between high-risk and low-risk students
* **Late-Night Work Patterns**

  * Higher severity students exhibit more irregular working hours
* **Procrastination Trends**

  * Moderate signal with overlap across severity levels

### Key Insight:

> Prolonged inactivity (max gap) is the most reliable indicator of student risk.

---

## 📂 Data Sources

### Synthetic Data (Primary)

* Generated realistic commit histories
* Includes multiple behavioral archetypes:

  * consistent workers
  * procrastinators
  * struggling students
  * inactive students
* Safe for experimentation and reproducibility

---

## 📚 Research Foundation

This project builds on established educational data mining research:

* **Gitinabard et al.**

  * GitHub activity correlates with teamwork and engagement
* **Hoq et al.**

  * Early programming patterns predict final performance

These works support the use of commit behavior as an early indicator of student outcomes.

---

## 🔐 Privacy & Ethics

### Privacy

* Only commit metadata is analyzed (timestamps, sizes, messages)
* No access to code content or grades
* No sensitive personal data collected

### Ethical Use

* Designed for **support, not grading**
* Requires transparency with students
* Human instructors make final decisions

---

## 🛠 Technology Stack

* **Language:** Python 3.8+
* **Data Processing:** pandas, numpy
* **Analysis:** statistics, datetime
* **Visualization:** matplotlib, seaborn
* **API Integration:** requests (GitHub REST API)
* **Evaluation:** scikit-learn
* **Testing:** pytest

---

## 🚀 Future Work

* Interactive dashboard (Streamlit or web app)
* Machine learning models for improved prediction
* Early-warning system (first 3–4 weeks)
* Real-time monitoring and alerts
* Integration with learning management systems (Canvas, Moodle)
* Multi-semester trend analysis

---

## 📌 Conclusion

This project demonstrates that GitHub activity patterns can serve as meaningful indicators of student engagement and risk. By combining interpretable analytics with behavioral insights, the system enables earlier intervention and supports more data-driven teaching practices.

---

## 👤 Contact

**John Phan**
University of Minnesota
Email: [phan0282@umn.edu](mailto:phan0282@umn.edu)

Advisor: Liia Butler

---
