# ai-github-teaching-agent

This project explores how AI-driven analytics can support computational teaching by analyzing GitHub repository activity. The goal is to help instructors identify patterns in student progress—such as steady work, inactivity, or potential struggle—based on commit behavior over time.

The project is developed as part of an independent study at the University of Minnesota.

--- 

## Motivation

GitHub is widely used in computer science courses, but instructors often lack visibility into how students are progressing between deadlines. By analyzing commit histories and repository activity, this project aims to provide lightweight, interpretable signals that can help instructors offer support earlier and better understand contribution patterns.

---

## Project Goals

- Analyze GitHub repository and commit activity over time
- Identify patterns such as steady progress, inactivity, or sudden changes in behavior
- Prototype an AI-assisted monitoring agent for educational use
- Compare data storage approaches using SQL and NoSQL systems
- Produce a working prototype and accompanying documentation

---

## Data Sources

This project uses **publicly available GitHub data**, including:

- **GH Archive** (sampled subsets of GitHub event data, filtered for commit-related activity)
- Small, preprocessed GitHub commit datasets for prototyping

To keep the repository lightweight and reproducible, only **sampled datasets (≤25MB)** are included. Raw data dumps are not committed to the repository.
