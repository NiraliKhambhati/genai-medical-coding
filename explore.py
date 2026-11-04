import pandas as pd

# Load the data
df = pd.read_csv("mtsamples.csv")

# How big is it?
print("Rows and columns:", df.shape)

# What columns does it have?
print("\nColumn names:", list(df.columns))

# How many notes are empty?
print("\nEmpty notes:", df["transcription"].isna().sum())

# Which specialties appear most?
print("\nTop 15 specialties:")
print(df["medical_specialty"].value_counts().head(15))