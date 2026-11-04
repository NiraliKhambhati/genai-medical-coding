import pandas as pd

# Load the official code list (first word on each line is the code)
valid_codes = set()
with open("icd10cm_codes_2027.txt") as f:
    for line in f:
        valid_codes.add(line.split()[0])

print("Official codes loaded:", len(valid_codes))

# Load Claude's answers
df = pd.read_csv("test_results.csv")

# Remove dots and spaces so "I25.10" becomes "I2510"
df["code_clean"] = (
    df["icd10_code"].astype(str)
    .str.replace(".", "", regex=False)
    .str.strip()
    .str.upper()
)

# Check each code against the official list
df["code_valid"] = df["code_clean"].isin(valid_codes)

print(df[["note_id", "icd10_code", "code_valid"]])
print("\nValid codes:", df["code_valid"].sum(), "out of", len(df))