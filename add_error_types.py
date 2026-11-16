import shutil
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

# Back up your ratings first, just in case
shutil.copy("review_sheet.xlsx", "review_sheet_backup.xlsx")

wb = load_workbook("review_sheet.xlsx")
ws = wb.active

# Add the new column header
ws["I1"] = "error_type"
ws["I1"].font = Font(bold=True)
ws.column_dimensions["I"].width = 38

# The error types to choose from
options = [
    "Wrong detail (side/type/specificity)",
    "Uncertain dx coded as confirmed",
    "Secondary condition coded",
    "Wrong encounter (7th character)",
    "Note unclear or multiple diagnoses",
    "Other",
]
dropdown = DataValidation(type="list",
                          formula1='"' + ",".join(options) + '"',
                          allow_blank=True)
ws.add_data_validation(dropdown)
dropdown.add("I2:I51")

# Highlight the rows that need an error type
yellow = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
count = 0
for row in range(2, 52):
    rating = ws[f"G{row}"].value
    if rating and rating != "Correct":
        ws[f"I{row}"].fill = yellow
        count += 1

wb.save("review_sheet.xlsx")
print("Added error_type column. Rows to fill in:", count)