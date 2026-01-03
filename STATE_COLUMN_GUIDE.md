# State Column Feature Guide

## 📋 Overview

The **state column** tracks the availability status of units across both output files:
1. **New Units Output** - Units being added to inventory
2. **Updated Inventory Output** - All existing units with current availability

---

## 🎯 State Values

| State | Description | When Applied |
|-------|-------------|--------------|
| `available` | Unit is currently available for sale | Unit code found in New Availability data |
| `unavailable` | Unit is no longer available | Unit code NOT found in New Availability data |

---

## 📊 Output Files

### 1. New Units Output
**Files:** `{Project}_New_Units_YYYYMMDD.xlsx`

**State Behavior:**
- ✅ **Always `'available'`**
- These are NEW units being added to inventory
- By definition, they are available (they came from New Availability sheet)

**Example:**
```
default_code        | name                                    | state
--------------------|-----------------------------------------|----------
PC1-A4-03-LB-42     | 1B Apartment in Park Central...         | available
VAL-V1-009-TH-A     | 4B Townhouse Corner in The Valleys...   | available
```

### 2. Updated Inventory Output
**File:** `Current_Inventory_Updated_YYYYMMDD.xlsx`

**State Behavior:**
- ✅ **Dynamic** - Based on comparison with New Availability
- `available` - Unit code exists in New Availability
- `unavailable` - Unit code does NOT exist in New Availability

**Example:**
```
default_code        | project                       | state
--------------------|-------------------------------|------------
PC1-A3-06-LA-21     | Park Central - Mostakbal City | available
PC1-A6-02-SA-41     | Park Central - Mostakbal City | available
VAL-V1-001-TH-A     | VAL: The Valleys              | unavailable
SLW-1234            | SLW: SwanLake West            | unavailable
```

---

## 🔄 How State is Determined

### Process Flow:

```
1. Load Current Inventory (107 units)
   ↓
2. Load New Availability (all sheets, all projects)
   ↓
3. Extract ALL unit codes from New Availability
   - Checks multiple column name variations:
     * UNIT CODE
     * UNIT CODES
     * Unit Code
     * UNIT_CODE
   ↓
4. Compare:
   - If current inventory unit code IN new availability → available
   - If current inventory unit code NOT IN new availability → unavailable
   ↓
5. Generate Updated Inventory with state column
```

---

## 💡 Use Cases

### Business Scenarios:

1. **Track Sold Units**
   - Units marked `unavailable` may have been sold
   - Review unavailable units for status updates

2. **Identify New Inventory**
   - New units output shows fresh additions
   - All marked `available` and ready for import

3. **Inventory Reconciliation**
   - Compare available vs unavailable counts
   - Ensure data consistency across systems

4. **Reporting**
   - Generate availability reports by project
   - Track inventory turnover over time

---

## 📈 Statistics Example

From a typical run:

```
Current Inventory: 107 units
├── Available: 101 units (94.4%)
└── Unavailable: 6 units (5.6%)

New Units Found: 12 units
├── Park Central: 1 unit
├── The Valleys: 11 units
└── SLW: 0 units
```

---

## 🔍 Verification

To verify state column is working:

1. **Check New Units Files:**
   ```python
   import pandas as pd
   df = pd.read_excel('output/Park_Central_New_Units_20260103.xlsx')
   print(df['state'].unique())  # Should show: ['available']
   ```

2. **Check Updated Inventory:**
   ```python
   df = pd.read_excel('output/Current_Inventory_Updated_20260103.xlsx')
   print(df['state'].value_counts())
   # Output:
   # available      101
   # unavailable      6
   ```

---

## ⚙️ Configuration

**Location:** `config.py`

```python
# Output columns in order (including state)
OUTPUT_COLUMNS = [
    'default_code',
    'unit_area',
    'finishing',
    'floor',
    'list_price',
    'unit_npv',
    'name',
    'number_of_rooms',
    'project',
    'maintenance_fee',
    'unit_type',
    'state',  # ← State column
]
```

**Implementation:** `processors/data_transformer.py`

```python
# New units are always available
transformed = {
    # ... other fields ...
    'state': 'available',  # Always available for new units
}
```

**Implementation:** `processors/unit_comparator.py`

```python
# Dynamic state for updated inventory
updated_df['state'] = updated_df['_normalized_code'].apply(
    lambda code: 'available' if code in new_codes else 'unavailable'
)
```

---

## 🎯 Key Points

✅ **State column is ALWAYS included** in both output types  
✅ **New units** → Always `'available'`  
✅ **Updated inventory** → Dynamic (`'available'` or `'unavailable'`)  
✅ **Case-insensitive comparison** - Unit codes normalized before comparison  
✅ **Multiple column support** - Checks all variations of unit code columns  

---

## 📝 Notes

- State is determined at runtime based on current data
- Historical state changes are not tracked (use version control for history)
- State reflects availability at the time of processing
- Archive old outputs to track state changes over time

---

**Last Updated:** 2026-01-03  
**Feature Status:** ✅ Fully Implemented and Tested

