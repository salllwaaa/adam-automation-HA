"""
Create a test unit in New Availability to demonstrate the system works
"""

import pandas as pd
from openpyxl import load_workbook

# Read the current New Availability file
file_path = 'New Availability.xlsx'

# Load Park Central sheet
df = pd.read_excel(file_path, sheet_name='Park Central', header=5, engine='openpyxl')

print(f"Original Park Central units: {len(df)}")
print(f"\nFirst unit code: {df.iloc[0]['UNIT CODE']}")

# Create a new test unit by modifying the first unit's code
test_unit = df.iloc[0:1].copy()
original_code = test_unit.iloc[0]['UNIT CODE']

# Modify the unit code to make it "new"
if isinstance(original_code, str):
    test_unit.loc[test_unit.index[0], 'UNIT CODE'] = original_code + '-TEST-NEW'
else:
    test_unit.loc[test_unit.index[0], 'UNIT CODE'] = 'PC1-TEST-NEW-21'

print(f"\nCreated test unit with code: {test_unit.iloc[0]['UNIT CODE']}")

# Append to the dataframe
df_with_test = pd.concat([df, test_unit], ignore_index=True)

print(f"New total: {len(df_with_test)} units")

# Save back to Excel
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_with_test.to_excel(writer, sheet_name='Park Central', index=False, startrow=5)

print("\n✓ Test unit added successfully!")
print("Now run: python main.py")

