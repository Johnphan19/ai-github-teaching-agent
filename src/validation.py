import json
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

DATA_PATH = "analysis_results.json"

with open(DATA_PATH, "r") as f:
    data = json.load(f)

students = data["individual_analyses"]

rows = []

for s in students:
    m = s["metrics"]

    row = {
        "severity": s["severity"],
        "consistency": m["activity_pattern"]["consistency_score"],
        "max_gap": m["activity_pattern"]["longest_gap_days"],
        "procrastination": m["temporal_analysis"]["procrastination_indicator"],
        "late_night": m["temporal_analysis"]["late_night_work_ratio"],
    }

    rows.append(row)

df = pd.DataFrame(rows)

# Convert labels
severity_map = {"none": 0, "low": 1, "medium": 2, "high": 3}
df["actual"] = df["severity"].map(severity_map)

# -----------------------------
# APPLY THRESHOLDS (edit these after tuning)
# -----------------------------
THRESHOLDS = {
    "max_gap": 7,
    "procrastination": 0.5,
    "late_night": 0.4,
    "consistency": 0.6
}

def predict(row):
    score = 0

    if row["max_gap"] > THRESHOLDS["max_gap"]:
        score += 1
    if row["procrastination"] > THRESHOLDS["procrastination"]:
        score += 1
    if row["late_night"] > THRESHOLDS["late_night"]:
        score += 1
    if row["consistency"] < THRESHOLDS["consistency"]:
        score += 1

    # Convert score → severity
    if score >= 3:
        return 3  # high
    elif score == 2:
        return 2  # medium
    elif score == 1:
        return 1  # low
    else:
        return 0  # none

df["predicted"] = df.apply(predict, axis=1)

# -----------------------------
# Evaluation
# -----------------------------
print("Confusion Matrix:")
print(confusion_matrix(df["actual"], df["predicted"]))

print("\nClassification Report:")
print(classification_report(df["actual"], df["predicted"]))