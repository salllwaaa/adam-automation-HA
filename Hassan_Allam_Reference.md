# Hassan Allam (HA) Automation Reference Guide
## Complete Knowledge Base for Inventory Cleaning & Updating

---

## 📋 Overview

**Developer:** Hassan Allam Properties (HAP)  
**Purpose:** Automate inventory updates, track unit availability, and standardize data format  
**Input:** Raw Excel availability data → **Output:** Cleaned, standardized inventory

---

## 🏗️ Projects & Identification

### Project Detection from Unit Codes

Unit codes follow a pattern where the **prefix identifies the project**:

| Unit Code Prefix | Project Name | Full Name |
|------------------|--------------|-----------|
| `PC`, `PC1`, `PC-` | Park_Central | Park Central - Mostakbal City |
| `VAL`, `VALL` | The_Valleys | VAL: The Valleys |
| `SLW`, `SLO` | SwanLake_October | SLW: SwanLake West (October) |
| `SLN` | SwanLake_North | SwanLake North Coast |
| `SLG`, `SLE` | SwanLake_ElGouna | SwanLake El Gouna |
| `HPT`, `HAPTOWN` | Haptown | Haptown Master Development |
| `PARKVIEW`, `PARK VIEW` | Haptown_PARKVIEW | Haptown Park View |
| `PARK226`, `PARK 226` | Haptown_Park_226 | Haptown Park 226 |
| `SEASONS` | Haptown_SEASONS | Haptown Seasons |
| `LV` | Little_Venice | Little Venice |
| `LVG` | Little_Venice_Gardens | Little Venice Gardens |
| `KEYS`, `KEY` | Keys_52 | Keys 52 |
| `SLR` | SLR | Swan Lake Residences |
| `PHOENIX` | SLR_The_Phoenix | SLR The Phoenix |
| `SELINA` | SLR_The_Selina | SLR The Selina |
| `AMAIA` | SLR_The_AMAIA | SLR The AMAIA |
| `ENCORE` | SLG_ENCORE | SLG Encore |

### Example Unit Codes
```
PC1-A3-06-LA-21     → Park Central
VALL-V3-207-SV-G    → The Valleys
SLW-0500-ABC        → SwanLake October
SLN-1234            → SwanLake North
```

---

## 🎨 Finishing Rules

### Rule: Finishing is determined by PROJECT + UNIT NUMBER

#### Park Central & The Valleys
```
Rule: ALWAYS "Fully Finished"
```

#### SwanLake West (SLW) - Complex Rules by Unit Number

| Unit Number Range | Finishing Type | Description |
|-------------------|----------------|-------------|
| **0100 - 0900** | `Core and shell and near delivery` | Villas Phase 1 |
| **1000 - 1999** | `Serviced Apartments` | Monos Serviced Apartments |
| **2000 - 2999** | `Fully Finished` | Twain Apartments |
| **3000 - 7000** | `Core and shell, 4 years delivery` | Villas Phase 2 |
| **8000+** | `Fully Finished` | Shimmers Lagoon Apartments |

**How to extract unit number from SLW code:**
```
SLW-0500-XXX → Extract "0500" → 500 → Villas Phase 1
SLW-2500-XXX → Extract "2500" → 2500 → Twains (Fully Finished)
SLW-8500-XXX → Extract "8500" → 8500 → Shimmers (Fully Finished)
```

#### Other Projects
```
Rule: Leave EMPTY (no finishing value)
Reason: Rules not yet defined - to be filled manually
```

---

## 🛏️ Bedroom Extraction Rules

### Priority Order
1. First check `NUMBER OF BEDROOMS` column (if exists)
2. Then extract from `UNIT TYPE` column
3. Finally, use mapping tables for villa types

### Text-to-Number Mapping
| Text Pattern | Bedrooms |
|--------------|----------|
| `STUDIO` | 0 |
| `ONE BEDROOM` | 1 |
| `TWO BEDROOMS` | 2 |
| `THREE BEDROOMS` | 3 |
| `FOUR BEDROOMS` | 4 |
| `FIVE BEDROOMS` | 5 |
| `SIX BEDROOMS` | 6 |

### Pattern Extraction (Regex)

| Pattern Format | Example | Result |
|----------------|---------|--------|
| `X Beds` | "Villa / 3 Beds" | 3 |
| `X BEDROOM` | "3 Bedrooms Apt" | 3 |
| `X+living` | "3+living room" | 3 (excludes living) |
| `XBR` or `XB ` | "2BR Unit" | 2 |
| Digit only | "3" (in bedroom column) | 3 |

### ⚠️ Important: Exclude These Rooms
When extracting bedrooms, **DO NOT count**:
- Living rooms
- Maid rooms
- Driver rooms
- Nanny rooms

Example: `"3+living room"` → **3 bedrooms** (not 4)

### Villa Type Mappings (When No Bedroom Column)

#### The Valleys - Villa Types
| Unit Type | Bedrooms |
|-----------|----------|
| TOWNHOUSE (M), TOWNHOUSE M, TOWNHOUSE B | 3 |
| TOWNHOUSE (C), TOWNHOUSE C, TOWNHOUSE A, TOWNHOUSE D | 4 |
| TWIN HOUSE, TWIN VILLA A, TWIN VILLA B | 4 |
| TWIN LOFT VILLA | 3 |
| STANDALONE VILLA D, STANDALONE VILLA F, STANDALONE VILLA A | 4 |
| STANDALONE VILLA G, STANDALONE VILLA B, STANDALONE VILLA C | 5 |
| STANDALONE SV - D, STANDALONE SV - E, STANDALONE SV - L | 5 |

#### SwanLake West (SLW) - Villa Types
| Unit Type | Bedrooms |
|-----------|----------|
| TOWNHOUSE (M), TOWNHOUSE M, TWIN LOFT VILLA | 3 |
| TWIN HOUSE, TWIN VILLA | 3 |
| STANDALONE SV - A, STANDALONE SV - I | 3 |
| STANDALONE SV - X, STANDALONE VILLA | 4 |
| STANDALONE SV - D, STANDALONE SV - E, STANDALONE SV - L | 5 |
| All TWAINS units | 3 |

---

## 🏢 Floor Conversion

### Input → Output Mapping
| Input Format | Output |
|--------------|--------|
| `GROUND` | Ground |
| `FIRST` | 1st |
| `SECOND` | 2nd |
| `THIRD` | 3rd |
| `FOURTH` | 4th |
| `FIFTH` | 5th |
| `SIXTH` | 6th |
| `1ST`, `2ND`, `3RD`, etc. | 1st, 2nd, 3rd (as-is) |

---

## 📊 Column Mapping (Source → Target)

### Input Columns (New Availability Excel)
| Source Column Names (variations) | Target Column |
|----------------------------------|---------------|
| `UNIT CODE`, `UNIT CODES`, `Unit Code` | `default_code` |
| `GROSS BUA`, `GROSS AREA`, `BUA` | `unit_area` |
| `FLOOR`, `Floor` | `floor` |
| `TOTAL PRICE`, `Final Price`, `Price`, `UNIT PRICE` | `list_price`, `unit_npv` |
| `UNIT TYPE`, `Unit Type` | `unit_type`, `number_of_rooms` (extracted) |
| `NUMBER OF BEDROOMS` | `number_of_rooms` |

### Output Columns (Standard Format - 12 Columns)
```
1.  default_code      - Unit identifier (from UNIT CODE)
2.  unit_area         - Square meters (from GROSS BUA)
3.  finishing         - Finishing type (calculated by rules)
4.  floor             - Floor number (converted format)
5.  list_price        - Unit price
6.  unit_npv          - Net Present Value (same as list_price)
7.  name              - Generated unit name
8.  number_of_rooms   - Bedroom count (extracted)
9.  project           - Project name (identified from code)
10. maintenance_fee   - 10% of list_price
11. unit_type         - Apartment, Villa, Townhouse, etc.
12. state             - 'available' or 'unavailable'
```

---

## 💰 Calculated Fields

### Maintenance Fee
```
maintenance_fee = list_price × 0.10 (10%)
```

### Unit NPV
```
unit_npv = list_price (same value)
```

### Unit Name Generation
```
Format: "{bedrooms}B {type} in {project} by Hassan Allam"

Examples:
- "3B Apartment in Park Central - Mostakbal City by Hassan Allam"
- "4B Villa in VAL: The Valleys by Hassan Allam"
- "2B Penthouse in SLW: SwanLake West by Hassan Allam"
```

---

## 🔄 State Tracking Logic

### How State is Determined
```
For each unit in CURRENT inventory:
    IF unit_code EXISTS in NEW availability:
        state = "available"
    ELSE:
        state = "unavailable"

For NEW units (not in current inventory):
    state = "available" (always)
```

### Comparison Process
1. Load current inventory → extract all `default_code` values
2. Load new availability → extract all `UNIT CODE` values
3. Normalize both (uppercase, trim whitespace)
4. Compare sets to determine:
   - **New units**: in new availability BUT NOT in current inventory
   - **Available**: in BOTH new availability AND current inventory
   - **Unavailable**: in current inventory BUT NOT in new availability

---

## 🏷️ Unit Type Classification

### Townhouse Variants
| Contains | Classification |
|----------|----------------|
| `(C)`, ` C`, `TOWNHOUSE C/A/D` | Townhouse Corner |
| `(M)`, ` M`, `TOWNHOUSE M/B` | Townhouse Middle |
| Just `TOWNHOUSE` | Townhouse |

### Other Types
- `APARTMENT` → Apartment
- `PENTHOUSE` → Penthouse
- `DUPLEX` → Duplex
- `VILLA` → Villa
- `TWIN HOUSE` / `TWIN VILLA` → Twin House

---

## 📁 File Structure

### Input Files
```
Input/
├── New Availability.xlsx    # Multi-sheet: one sheet per project/sub-project
└── Current adam inv.xlsx    # Current inventory database
```

### Output Files
```
output/
├── Current_Inventory_Updated_YYYYMMDD.xlsx   # Updated inventory with states
├── {Project}_New_Units_YYYYMMDD.xlsx         # New units per project
└── processing_summary.txt                     # Summary report
```

---

## 📋 Processing Steps

### Complete Workflow
```
1. LOAD
   └── Load all sheets from New Availability.xlsx
   └── Load Current Inventory
   └── Extract existing unit codes

2. PROCESS (for each sheet)
   └── Find new units (not in current inventory)
   └── Transform each unit:
       ├── Identify project from unit code
       ├── Convert floor format
       ├── Extract bedroom count
       ├── Determine finishing
       ├── Calculate maintenance fee
       └── Generate unit name

3. COMPARE
   └── Mark existing units as available/unavailable
   └── Group new units by project

4. OUTPUT
   └── Save updated inventory with states
   └── Save new units files per project
   └── Generate summary report
```

---

## ⚠️ Edge Cases & Special Handling

### Missing Data
| Field | If Missing |
|-------|------------|
| `UNIT CODE` | Skip the row entirely |
| `GROSS BUA` | Set to 0 |
| `TOTAL PRICE` | Set to 0 |
| `FLOOR` | Leave empty |
| `NUMBER OF BEDROOMS` | Try to extract from UNIT TYPE, else 0 |

### Price Column Priority
When multiple price columns exist, use this priority:
1. `Final Price` (for Valleys)
2. `TOTAL PRICE`
3. `Price`
4. `UNIT PRICE`
5. `TOTAL PRICE - 7 Years`
6. `TOTAL PRICE - 10 Years`

### Unknown Projects
If a unit code doesn't match any known pattern:
1. Try to extract prefix (letters before first number/dash)
2. Use sheet name as project name
3. If all else fails, mark as "Unknown"

---

## 🔧 Configuration Reference

### Key Settings
```python
# Maintenance fee percentage
MAINTENANCE_FEE_PERCENTAGE = 0.10  # 10%

# Developer name (for unit name generation)
DEVELOPER = 'Hassan Allam'

# File paths
NEW_AVAILABILITY_FILE = 'Input/New Availability.xlsx'
CURRENT_INVENTORY_FILE = 'Input/Current adam inv.xlsx'
OUTPUT_DIRECTORY = 'output'
```

---

## 📝 Summary Table

| Aspect | Hassan Allam Rule |
|--------|-------------------|
| **Developer** | Hassan Allam Properties |
| **Finishing (PC, Valleys)** | Always "Fully Finished" |
| **Finishing (SLW)** | Based on unit number range |
| **Finishing (Others)** | Empty (undefined) |
| **Maintenance Fee** | 10% of list_price |
| **NPV** | Same as list_price |
| **Name Format** | `{beds}B {type} in {project} by Hassan Allam` |
| **State** | available / unavailable |
| **Bedrooms** | Extract from column or unit type |
| **Project ID** | From unit code prefix |

---

## 🎯 Quick Reference for Generic Agent

To adapt for another developer:
1. **Update PROJECT_PATTERNS** - Map unit code prefixes to project names
2. **Update FINISHING_RULES** - Define finishing logic per project
3. **Update BEDROOM_MAPPINGS** - Villa/unit type to bedroom mappings
4. **Update DEVELOPER name** - For name generation
5. **Update MAINTENANCE_FEE_PERCENTAGE** - If different
6. **Review PRICE_COLUMNS** - Which price column to use

---

*This document serves as the complete reference for Hassan Allam Properties inventory automation rules and logic.*

