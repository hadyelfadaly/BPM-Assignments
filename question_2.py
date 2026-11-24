import pandas as pd
from itertools import combinations

# 1. Load clean event log
df = pd.read_csv("Q2_clean_event_log.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Map official activity names to their alphabetical letters (from README)
act_to_letter = {
    "Billing": "a",
    "Discharge Patient": "b",
    "Doctor Consultation": "c",
    "Order Lab Tests": "d",
    "Prescribe Treatment": "e",
    "Register Patient": "f",
    "Take Vitals": "g",
    "Triage": "h",
}
letters = sorted(act_to_letter.values())  # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
df["letter"] = df["activity"].map(act_to_letter)

# 2. Sort events per case chronologically (preserving file order on timestamp ties)
df = df.sort_values(["case_id", "timestamp"], kind="mergesort")

# Extract trace (tuple of letters) for every case
traces = df.groupby("case_id", sort=False)["letter"].apply(tuple)

# Q2.1: Number of distinct traces (variants)
distinct_traces = set(traces)
q2_1 = len(distinct_traces)

# 3. Compute directly-follows relation (>L) across all traces
directly_follows = set()
for trace in traces:
    for i in range(len(trace) - 1):
        directly_follows.add((trace[i], trace[i + 1]))

# Q2.2: Number of ordered pairs (x, y) with x >L y
q2_2 = len(directly_follows)

# 4. Classify all 28 unordered distinct pairs {x, y} (with x < y alphabetically)
causality_pairs = []   # x -> y or y -> x
parallel_pairs = []    # x || y
unrelated_pairs = []   # x # y
matrix_28 = {}         # relation for (x, y) where x < y

for x, y in combinations(letters, 2):
    xy = (x, y) in directly_follows
    yx = (y, x) in directly_follows

    if xy and not yx:
        rel = "→"
        causality_pairs.append((x, y))
    elif yx and not xy:
        rel = "←"
        causality_pairs.append((x, y))
    elif xy and yx:
        rel = "||"
        parallel_pairs.append((x, y))
    else:
        rel = "#"
        unrelated_pairs.append((x, y))

    matrix_28[(x, y)] = rel

# Check if any activity directly follows itself (x >L x)
self_loops = [x for x in letters if (x, x) in directly_follows]

# Q2.6 and Q2.7: Start activties
start_activities = df.groupby("case_id", sort=False).first()["letter"].unique()
q2_6 = len(start_activities)

# Q2.8 and Q2.9: End activities
end_activities = df.groupby("case_id", sort=False).last()["letter"].unique()
q2_8 = len(end_activities)

# Q2.10: XL
TL = sorted(set(df["letter"]))
# Helper checks built directly on your existing `directly_follows` set
def is_causal(x, y):
    return (x, y) in directly_follows and (y, x) not in directly_follows

def is_unrelated(x, y):
    return (x, y) not in directly_follows and (y, x) not in directly_follows

# 1. All non-empty subsets of TL whose members are pairwise '#'
valid_subsets = [
    frozenset(sub)
    for r in range(1, len(TL) + 1)
    for sub in combinations(TL, r)
    if all(is_unrelated(x, y) for x in sub for y in sub)
]

# 2. Q2.10: XL = all pairs (A, B) where every a in A -> every b in B
XL = [
    (A, B)
    for A in valid_subsets
    for B in valid_subsets
    if all(is_causal(a, b) for a in A for b in B)
]
q2_10 = len(XL)

# 3. Q2.11 – Q2.13 directly from XL, q2_6, and q2_8
YL = [
    (A, B)
    for (A, B) in XL
    if not any(
        (A != A2 or B != B2) and A.issubset(A2) and B.issubset(B2)
        for (A2, B2) in XL
    )
]
q2_11 = len(YL)
q2_12 = q2_11 + 2  # |YL| + source place iL + sink place oL
q2_13 = q2_6 + q2_8 + sum(len(A) + len(B) for A, B in YL)

print(f"Total cases: {len(traces)}")
print(f"Q2.1 (Distinct traces / variants):          {q2_1}")
print(f"Q2.2 (Ordered pairs x >L y):                {q2_2}")
print(f"Q2.3 (Unordered causality pairs):           {len(causality_pairs)}")
print(f"Q2.4 (Unordered parallel pairs x || y):     {len(parallel_pairs)}")
print(f"Q2.5 (Unordered unrelated pairs x # y):     {len(unrelated_pairs)}")
print(f"Sanity check (Q2.3 + Q2.4 + Q2.5 == 28):    {len(causality_pairs) + len(parallel_pairs) + len(unrelated_pairs)}")
print(f"Any self-loops (x >L x):                    {self_loops}\n")
print(f"Q2.6 (Distinct start activities):           {q2_6}")
print(f"Start activities: {start_activities}\n")
print(f"Q2.8 (Distinct end activities):             {q2_8}")
print(f"End activities: {end_activities}\n")
print(f"Q2.10 (|XL|):   {q2_10}")
print(f"Q2.11 (|YL|):   {q2_11}")
print(f"Q2.12 (Places): {q2_12}")
print(f"Q2.13 (Arcs):   {q2_13}")

# Optional: Print full 8x8 scratch worksheet matrix
print("\n--- Full 8x8 Footprint Matrix ---")
header = "    " + "  ".join(f"{col:>2}" for col in letters)
print(header)
for r in letters:
    row_cells = []
    for c in letters:
        if r == c:
            row_cells.append("||" if (r, r) in directly_follows else "#")
        elif (r, c) in directly_follows and (c, r) not in directly_follows:
            row_cells.append("→")
        elif (c, r) in directly_follows and (r, c) not in directly_follows:
            row_cells.append("←")
        elif (r, c) in directly_follows and (c, r) in directly_follows:
            row_cells.append("||")
        else:
            row_cells.append("#")
    print(f"{r:>2}  " + "  ".join(f"{cell:>2}" for cell in row_cells))