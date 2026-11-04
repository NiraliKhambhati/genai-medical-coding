import pandas as pd

df = pd.read_csv("clean_notes.csv")

# Pick 320 notes at random
sample = df.sample(n=320, random_state=42)

# Give each note a simple ID number
sample = sample.reset_index(drop=True)
sample["note_id"] = sample.index + 1

sample.to_csv("sample_notes.csv", index=False)

print("Sample size:", len(sample))
print("\nNotes per specialty:")
print(sample["medical_specialty"].value_counts())