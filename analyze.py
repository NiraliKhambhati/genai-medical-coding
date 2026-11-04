import pandas as pd

# Load the official code list
valid_codes = set()
with open("icd10cm_codes_2027.txt") as f:
    for line in f:
        valid_codes.add(line.split()[0])

df = pd.read_csv("results_baseline.csv")

# 1. Did any notes fail?
if "error" in df.columns:
    print("Failed notes:", df["error"].notna().sum())
else:
    print("Failed notes: 0")

# 2. Specialty accuracy
df["specialty_correct"] = df["specialty"] == df["true_specialty"]
print(f"\nSpecialty accuracy: {df['specialty_correct'].mean():.1%}")
print("\nAccuracy by specialty:")
print(df.groupby("true_specialty")["specialty_correct"].mean().round(2))

# 3. Code validity
df["code_clean"] = (
    df["icd10_code"].astype(str)
    .str.replace(".", "", regex=False)
    .str.strip()
    .str.upper()
)
df["code_valid"] = df["code_clean"].isin(valid_codes)
print(f"\nValid codes: {df['code_valid'].sum()} out of {len(df)} ({df['code_valid'].mean():.1%})")

# 4. Confidence vs. code validity
print("\nCode validity by confidence level:")
print(pd.crosstab(df["confidence"], df["code_valid"], margins=True))

# Save for Power BI later
df.to_csv("results_baseline_checked.csv", index=False)
print("\nSaved: results_baseline_checked.csv")