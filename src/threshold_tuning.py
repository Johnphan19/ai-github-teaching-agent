import json
import pandas as pd
import numpy as np

DATA_PATH = "analysis_results.json"

with open(DATA_PATH, "r") as f:
    data = json.load(f)

students = data["individual_analyses"]

rows = []

for s in students:
    m = s["metrics"]

    row = {
        "student_id": s["student_id"],
        "severity": s["severity"],

        # Activity
        "consistency": m["activity_pattern"]["consistency_score"],
        "avg_gap": m["activity_pattern"]["average_days_between_commits"],
        "max_gap": m["activity_pattern"]["longest_gap_days"],

        # Temporal
        "late_night": m["temporal_analysis"]["late_night_work_ratio"],
        "procrastination": m["temporal_analysis"]["procrastination_indicator"],

        # Progress
        "active_ratio": m["progress_tracking"]["active_weeks_ratio"],
        "commits_per_week": m["progress_tracking"]["average_commits_per_week"],

        # Quality
        "quality": m["commit_quality"]["quality_score"],
        "message_quality": m["commit_quality"]["message_quality_ratio"]
    }

    rows.append(row)

df = pd.DataFrame(rows)

# Convert severity → numeric
severity_map = {"none": 0, "low": 1, "medium": 2, "high": 3}
df["label"] = df["severity"].map(severity_map)

# -----------------------------
# Threshold tuning
# -----------------------------

def evaluate_threshold(feature, thresholds):
    best_thresh = None
    best_score = -1

    for t in thresholds:
        preds = (df[feature] > t).astype(int)

        # We treat high severity (>=2) as "at risk"
        actual = (df["label"] >= 2).astype(int)

        accuracy = (preds == actual).mean()

        if accuracy > best_score:
            best_score = accuracy
            best_thresh = t

    return best_thresh, best_score


# Try tuning important features
features_to_tune = {
    "max_gap": np.arange(2, 15, 1),
    "procrastination": np.arange(0.1, 0.9, 0.05),
    "late_night": np.arange(0.05, 0.6, 0.05),
    "consistency": np.arange(0.3, 1.0, 0.05)
}

results = {}

for feature, thresholds in features_to_tune.items():
    best_t, score = evaluate_threshold(feature, thresholds)
    results[feature] = {"threshold": best_t, "accuracy": score}

print("\nBest Thresholds:")
for k, v in results.items():
    print(f"{k}: {v}")