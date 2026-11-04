import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 45)

# Load the official code list
valid_codes = set()
with open("icd10cm_codes_2027.txt") as f:
    for line in f:
        valid_codes.add(line.split()[0])

df = pd.read_csv("results_baseline_checked.csv")

# Keep only the invalid codes
invalid = df[~df["code_valid"]].copy()

# Sort each invalid code into an error type
def error_type(code):
    if pd.isna(code) or str(code) in ("NAN", "NONE", ""):
        return "No code given"
    code = str(code)
    if any(v.startswith(code) for v in valid_codes):
        return "Incomplete (missing digits)"
    return "Does not exist"

invalid["error_type"] = invalid["code_clean"].apply(error_type)

print(invalid[["note_id", "true_specialty", "primary_diagnosis", "icd10_code", "confidence", "error_type"]])

print("\nError types:")
print(invalid["error_type"].value_counts())

# The note with no confidence level
print("\nNote(s) with no confidence level:")
print(df[df["confidence"].isna()][["note_id", "icd10_code", "primary_diagnosis"]])