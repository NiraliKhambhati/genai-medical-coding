import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 70)

# Load your ratings
review = pd.read_excel("review_sheet.xlsx")
print("Notes rated:", review["my_rating"].notna().sum(), "of", len(review))

# 1. Overall ratings
print("\n=== Your ratings ===")
counts = review["my_rating"].value_counts()
percent = review["my_rating"].value_counts(normalize=True).mul(100).round(1)
print(pd.DataFrame({"count": counts, "percent": percent}))

# Add Claude's confidence and the specialty (hidden during your review)
results = pd.read_csv("all_results.csv")
improved = results[results["version"] == "Improved"]
review = review.merge(improved[["note_id", "confidence", "true_specialty"]], on="note_id")

# 2. Did Claude's confidence match your ratings?
print("\n=== Ratings by Claude's confidence ===")
print(pd.crosstab(review["confidence"], review["my_rating"], margins=True))

# 3. Ratings by specialty
print("\n=== Ratings by specialty ===")
print(pd.crosstab(review["true_specialty"], review["my_rating"], margins=True))

# 4. Your comments on codes that weren't fully correct
print("\n=== Your comments ===")
print(review.loc[review["my_rating"] != "Correct",
                 ["note_id", "icd10_code", "my_rating", "my_comment"]])

# 5. Overall estimate: valid AND correct
valid_rate = improved["code_valid"].mean()
correct_rate = (review["my_rating"] == "Correct").mean()
print(f"\nValid codes: {valid_rate:.1%}")
print(f"Correct (among valid, your review): {correct_rate:.1%}")
print(f"Estimated fully correct overall: {valid_rate * correct_rate:.1%}")

# 6. Error types
print("\n=== Error types ===")
missing = review[(review["my_rating"] != "Correct") & (review["error_type"].isna())]
print("Rows still missing an error type:", len(missing))
print(review["error_type"].value_counts())

print("\n=== Error types by rating ===")
print(pd.crosstab(review["error_type"], review["my_rating"]))

# Save for Power BI
review.to_csv("review_results.csv", index=False)
print("\nSaved: review_results.csv")