import pandas as pd

df = pd.read_csv("mtsamples.csv")
print("Starting notes:", len(df))

# Remove extra spaces around specialty names
df["medical_specialty"] = df["medical_specialty"].str.strip()

# 1. Remove empty notes
df = df.dropna(subset=["transcription"])

# 2. Keep only the 8 specialties
keep = [
    "Cardiovascular / Pulmonary",
    "Orthopedic",
    "Gastroenterology",
    "Neurology",
    "Obstetrics / Gynecology",
    "Urology",
    "ENT - Otolaryngology",
    "Hematology - Oncology",
]
df = df[df["medical_specialty"].isin(keep)]

# 3. Remove notes that appear more than once
df = df.drop_duplicates(subset=["transcription"], keep=False)

# 4. Keep only the columns we need, and save
df = df[["medical_specialty", "sample_name", "transcription"]]
df.to_csv("clean_notes.csv", index=False)

print("Clean notes:", len(df))
print("\nNotes per specialty:")
print(df["medical_specialty"].value_counts())