import pandas as pd

# Show wide columns without cutting them off
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 50)

df = pd.read_csv("test_results.csv")

print(df[["note_id", "primary_diagnosis", "icd10_code", "confidence"]])