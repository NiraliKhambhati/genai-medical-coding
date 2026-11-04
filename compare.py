import pandas as pd

# Load the official code list
valid_codes = set()
with open("icd10cm_codes_2027.txt") as f:
    for line in f:
        valid_codes.add(line.split()[0])

# Sort each code into a result type
def error_type(code):
    if pd.isna(code) or str(code) in ("NAN", "NONE", ""):
        return "No code given"
    code = str(code)
    if code in valid_codes:
        return "Valid"
    if any(v.startswith(code) for v in valid_codes):
        return "Incomplete (missing digits)"
    return "Does not exist"

# Check one results file
def check(filename, version):
    df = pd.read_csv(filename)
    df["version"] = version
    df["specialty_correct"] = df["specialty"] == df["true_specialty"]
    df["code_clean"] = (
        df["icd10_code"].astype(str)
        .str.replace(".", "", regex=False)
        .str.strip()
        .str.upper()
    )
    df["code_result"] = df["code_clean"].apply(error_type)
    df["code_valid"] = df["code_result"] == "Valid"
    return df

base = check("results_baseline_checked.csv", "Baseline")
imp = check("results_improved.csv", "Improved")

# Show results side by side
for df in [base, imp]:
    print(f"\n=== {df['version'].iloc[0]} ===")
    print(f"Specialty accuracy: {df['specialty_correct'].mean():.1%}")
    print(f"Valid codes: {df['code_valid'].sum()} of {len(df)} ({df['code_valid'].mean():.1%})")
    print(df["code_result"].value_counts())

# Save one combined file for Power BI
pd.concat([base, imp]).to_csv("all_results.csv", index=False)
print("\nSaved: all_results.csv")