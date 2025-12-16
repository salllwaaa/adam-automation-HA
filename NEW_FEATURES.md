# New Feature: Updated Inventory with State Tracking

## Overview

The system now generates an **Updated Current Inventory** file that shows the availability status of all units by comparing them against the new availability data.

## New Output File

### `Current_Inventory_Updated_YYYYMMDD.xlsx`

This file contains:
- **All units** from "The Current inv.xlsx"
- **New "state" column** with availability status
- All original columns preserved

## State Column Values

| State | Meaning | Description |
|-------|---------|-------------|
| `available` | Unit is still available | Unit code exists in "New Availability.xlsx" |
| `unavailable` | Unit became unavailable | Unit code does NOT exist in "New Availability.xlsx" |

## How It Works

```
┌─────────────────────────────────────────┐
│  The Current inv.xlsx                   │
│  - 107 existing units                   │
│  - All columns preserved                │
└─────────────────────────────────────────┘
              ▼
         Compare with
              ▼
┌─────────────────────────────────────────┐
│  New Availability.xlsx                  │
│  - Park Central: 29 units               │
│  - The Valleys: 25 units                │
│  - SLW: 66 units                        │
│  - Total: 120 units                     │
└─────────────────────────────────────────┘
              ▼
         Add "state" column
              ▼
┌─────────────────────────────────────────┐
│  Current_Inventory_Updated_YYYYMMDD.xlsx│
│  - Same 107 units                       │
│  - Added "state" column:                │
│    • 29 units: "available"              │
│    • 78 units: "unavailable"            │
└─────────────────────────────────────────┘
```

## Example Output

### Sample Data:

| default_code | project | finishing | list_price | state |
|--------------|---------|-----------|------------|-------|
| PC1-A3-06-LA-21 | Park Central | Fully Finished | 8,775,379 | available |
| PC1-A6-02-SA-41 | Park Central | Fully Finished | 9,663,000 | available |
| VAL-V3-230-TF-C | The Valleys | Fully Finished | 15,044,200 | unavailable |
| VAL-V3-285-TF-C | The Valleys | Fully Finished | 13,695,100 | unavailable |
| SLW-V-0500-... | SLW | Core and shell | 12,118,800 | unavailable |

## Processing Steps

The system now follows these steps:

1. Load "The Current inv.xlsx" (107 units)
2. Load "New Availability.xlsx" (all project sheets)
3. Compare unit codes
4. Generate updated inventory with state column
5. Save to `Current_Inventory_Updated_YYYYMMDD.xlsx`
6. Identify new units (as before)
7. Generate new units output files (as before)

## Console Output

During processing, you'll see:

```
[5/6] Generating updated inventory with availability states...
  >> Updated inventory saved: Current_Inventory_Updated_20251216.xlsx
     - Available: 29 units
     - Unavailable: 78 units
```

## Summary Report

The summary report now includes availability statistics:

```
================================================================================
Hassan Allam Inventory Update - Processing Summary
================================================================================
Processed at: 2025-12-16 12:06:17

Updated Current Inventory:
--------------------------------------------------------------------------------
  File: output\Current_Inventory_Updated_20251216.xlsx
  Available units: 29
  Unavailable units: 78
  Total units: 107

New Units by Project:
--------------------------------------------------------------------------------
  Park_Central: 0 new units
  The_Valleys: 0 new units
  SLW: 0 new units

Total New Units: 0
================================================================================
```

## Complete Output Files

After running `python main.py`, you get:

### 1. Updated Inventory (NEW!)
- `Current_Inventory_Updated_20251216.xlsx`
  - All existing units with state column
  - Shows which units are still available
  - Shows which units became unavailable

### 2. New Units (Existing Feature)
- `Park_Central_New_Units_20251216.xlsx`
- `The_Valleys_New_Units_20251216.xlsx`
- `SLW_New_Units_20251216.xlsx`

## Use Cases

### 1. Track Availability Changes
Quickly identify which units from your inventory are no longer available in the new data.

### 2. Update Your System
Use the "state" column to:
- Mark unavailable units in your database
- Send notifications about sold units
- Update your website/listings

### 3. Audit Trail
Keep historical record of when units became unavailable.

## Technical Implementation

### New Function: `generate_updated_inventory()`

Located in `processors/unit_comparator.py`:

```python
def generate_updated_inventory(
    self, 
    current_inventory_df: pd.DataFrame, 
    new_availability_df: pd.DataFrame,
    unit_code_column_current: str = 'default_code',
    unit_code_column_new: str = 'UNIT CODE'
) -> pd.DataFrame
```

**Logic:**
1. Extracts all unit codes from new availability
2. Normalizes codes (uppercase, trim whitespace)
3. Compares each current inventory unit code
4. Sets state = "available" if found in new availability
5. Sets state = "unavailable" if NOT found in new availability
6. Returns updated DataFrame with new "state" column

### Updated Step Numbers

The processing now has 6 steps (was 5):
1. Load Excel files
2. Extract existing unit codes
3. Initialize comparator
4. Process projects and identify new units
5. **Generate updated inventory with states (NEW!)**
6. Save output files

## Statistics

From the latest test run:
- **Total units in current inventory**: 107
- **Available** (found in new availability): 29 units (27%)
- **Unavailable** (not found in new availability): 78 units (73%)

This means 78 units from your current inventory are no longer available in the new data.

## Future Enhancements (Optional)

Potential additions:
1. **Historical tracking** - Compare multiple versions over time
2. **Change notifications** - Email alerts when units become unavailable
3. **Detailed change report** - Show what changed for each unit
4. **State timestamps** - Track when units became unavailable
5. **Filtering options** - Generate separate files for available/unavailable

---

**Feature Status**: ✅ Complete and Tested  
**Added**: December 16, 2025  
**Version**: 1.1

