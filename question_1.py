import re
import pandas as pd

# Load raw CSV strictly as strings without auto-converting to NaN
df = pd.read_csv("Q1_raw_event_log.csv", dtype=str, keep_default_na=False)

print("Columns:", list(df.columns))
print("Sample rows:\n", df.head(5), "\n")

# Helper to check if a string cell is empty (blank or whitespace only)
is_empty = lambda s: s.str.strip() == ""

# Q1.1: Number of data rows (header excluded)
q1_1 = len(df)

# Q1.2: Number of distinct, non-empty case IDs
non_empty_cases = df[df["case_id"].str.strip() != ""].copy()
q1_2 = non_empty_cases["case_id"].nunique()

# Q1.3: Rows whose case ID is empty [CASE-MIS]
q1_3 = is_empty(df["case_id"]).sum()

# Q1.4: Rows whose timestamp is empty [TS-MIS]
q1_4 = is_empty(df["timestamp"]).sum()

# Q1.5: Rows whose timestamp has a date but NO time of day (format YYYY-MM-DD) [TS-IMP]
ts_trimmed = df["timestamp"].str.strip()
q1_5 = ts_trimmed.str.match(r"^\d{4}-\d{2}-\d{2}$").sum()

# Q1.6: Rows whose resource is empty [RES-MIS]
q1_6 = is_empty(df["resource"]).sum()

#Q1.7: Rows identical in ALL four columns to an EARLIER row; each extra copy counts 1 [EV-CIL]
q1_7 = df.duplicated(keep="first").sum()

#Q1.8: Number of distinct activity strings exactly as written in the file
q1_8 = df["activity"].nunique()

# Q1.9: Rows whose activity string is NOT exactly one of the 8 official activity names
activities = df["activity"].str.strip().str.lower().str.replace("_", " ").str.title()
q1_9 = len([x for x in df["activity"] if x not in activities.unique()])

# Q1.10: Cases (non-empty IDs) with NO event of your mandatory activity, after normalizing labels
non_empty_cases["normalized_activity"] = activities
has_triage = non_empty_cases.groupby("case_id")["normalized_activity"].apply(lambda acts: "Triage" in set(acts))
q1_10 = (~has_triage).sum()

# Q1.11: Cases whose rows, in FILE order, are not in non-decreasing timestamp order
ts_trimmed = non_empty_cases["timestamp"].str.strip()
has_full_datetime = ts_trimmed.str.match(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(:\d{2}(\.\d+)?)?$")
non_empty_cases = non_empty_cases[has_full_datetime].copy()
non_empty_cases["parsed_ts"] = pd.to_datetime(non_empty_cases["timestamp"].str.strip())
q1_11 = non_empty_cases.groupby("case_id")["parsed_ts"].apply(lambda ts: not ts.is_monotonic_increasing).sum()

# Q1.12:
df["res_missing"] = df["resource"].str.strip() == ""
missing_indices = df[df["res_missing"]].index.tolist()
print(f"Total rows: {len(df)} | Missing resource rows: {len(missing_indices)}")
print("Row indices where resource is empty:", missing_indices)

# Check distribution over time (by date)
df["date"] = df["timestamp"].str.strip().str[:10]
print("\nMissing resource count by date:")
print(df.groupby("date")["res_missing"].agg(total_rows="count", missing_res="sum"))


print(f"Q1.1 (Total data rows):            {q1_1}")
print(f"Q1.2 (Distinct non-empty cases):   {q1_2}")
print(f"Q1.3 (CASE-MIS - empty case_id):   {q1_3}")
print(f"Q1.4 (TS-MIS - empty timestamp):   {q1_4}")
print(f"Q1.5 (TS-IMP - date only):         {q1_5}")
print(f"Q1.6 (RES-MIS - empty resource):   {q1_6}")
print(f"Q1.7 (EV-CIL - duplicate events):  {q1_7}")
print(f"Q1.8 (Distinct activity strings):  {q1_8}")
print(f"Q1.9 (Unrecognized activity strings): {q1_9}")
print(f"Q1.10 (Cases missing mandatory activity): {q1_10}")
print(f"Q1.11 (Cases with non-monotonic timestamps): {q1_11}")
print(f"Q1.12 Recurrence pattern of the empty-resource problem: 2")


print("Official activity names (normalized):", activities.unique())