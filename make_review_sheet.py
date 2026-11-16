import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.datavalidation import DataValidation

# Load the official code descriptions
descriptions = {}
with open("icd10cm_codes_2027.txt") as f:
    for line in f:
        parts = line.strip().split(maxsplit=1)
        descriptions[parts[0]] = parts[1] if len(parts) > 1 else ""

# Keep only improved-run notes with valid codes
results = pd.read_csv("all_results.csv")
improved = results[(results["version"] == "Improved") & (results["code_valid"] == True)]

# Add the original clinical note text
notes = pd.read_csv("sample_notes.csv")[["note_id", "transcription"]]
improved = improved.merge(notes, on="note_id")

# Pick 50 notes at random (repeatable)
review = improved.sample(n=50, random_state=42)
review["official_description"] = review["code_clean"].map(descriptions)

# Choose the columns to show, plus empty columns for your ratings
review = review[["note_id", "transcription", "primary_diagnosis",
                 "icd10_code", "official_description", "evidence"]]
review["my_rating"] = ""
review["my_comment"] = ""
review.to_excel("review_sheet.xlsx", index=False)

# Make the spreadsheet easy to read
wb = load_workbook("review_sheet.xlsx")
ws = wb.active
widths = {"A": 10, "B": 80, "C": 30, "D": 12, "E": 40, "F": 30, "G": 18, "H": 40}
for col, width in widths.items():
    ws.column_dimensions[col].width = width
for row in ws.iter_rows(min_row=2):
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, vertical="top")
for cell in ws[1]:
    cell.font = Font(bold=True)
ws.freeze_panes = "A2"

# Add a dropdown menu for your ratings
dropdown = DataValidation(type="list",
                          formula1='"Correct,Partially correct,Incorrect,Unclear"',
                          allow_blank=True)
ws.add_data_validation(dropdown)
dropdown.add("G2:G51")

wb.save("review_sheet.xlsx")
print("Created review_sheet.xlsx with", len(review), "notes")