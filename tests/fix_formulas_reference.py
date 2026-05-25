import openpyxl
from openpyxl.styles import Font

# Load the workbook
wb = openpyxl.load_workbook('/home/ubuntu/real_estate_guide/Real_Estate_Investment_Toolkit.xlsx')

print("Fixing Formulas Reference sheet properly...")

# Fix Formulas Reference sheet - the Excel Syntax column should be TEXT examples, not formulas
ws10 = wb["Formulas Reference"]

# These are example formulas that should display as text, not calculate
example_formulas = [
    "=ARV - Fixed - Rehab - Profit",
    "=AVERAGE(Comp1,Comp2,Comp3)",
    "=(ARV*0.7) - Rehab",
    "=GrossRent - OpEx",
    "=NOI/Value*100",
    "=CashFlow/Investment*100",
    "=Price/GrossRent",
    "=MonthlyRent/Value",
    "=NOI/DebtService",
    "=(OpEx+Debt)/GrossRent",
    "=(Profit/Cost)*100",
    "=Rent-Mortgage-OpEx/12",
    "=Cash+Appreciation+Principal",
    "=Loan/Value*100",
    "=OpEx/GrossIncome"
]

# Replace column D (Excel Syntax) with plain text strings
for idx, formula_text in enumerate(example_formulas, start=4):
    cell = ws10.cell(row=idx, column=4)
    # Set as string value explicitly
    cell.value = formula_text
    # Make sure it's treated as text by setting data_type
    cell.data_type = 'str'
    # Keep the Courier New font
    cell.font = Font(name='Courier New')
    print(f"Row {idx}: Set as text: {formula_text}")

# Save the workbook
wb.save('/home/ubuntu/real_estate_guide/Real_Estate_Investment_Toolkit.xlsx')
print("\n✅ Formulas Reference sheet fixed - all example formulas are now text!")
