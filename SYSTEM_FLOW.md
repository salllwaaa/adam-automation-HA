# Hassan Allam Inventory Update System - Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INPUT FILES                                   │
├─────────────────────────────────────────────────────────────────────┤
│  New Availability.xlsx        │  The Current inv.xlsx               │
│  - Park Central Sheet         │  - default_code column              │
│  - The Valleys Sheet          │  - 107 existing units               │
│  - SLW-Villas Sheet          │                                      │
│  - SLW-Monos Sheet           │                                      │
│  - SLW-Solos Sheet           │                                      │
│  - SLW-Twains Sheet          │                                      │
│  - SLW-Shimmers Sheet        │                                      │
│  - SLW-Boomerang Sheet       │                                      │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 1: EXCEL LOADER                              │
│                  (processors/excel_loader.py)                        │
├─────────────────────────────────────────────────────────────────────┤
│  ✓ Load New Availability.xlsx with all sheets                       │
│  ✓ Smart header detection (finds "UNIT CODE" row)                   │
│  ✓ Load The Current inv.xlsx                                        │
│  ✓ Extract existing unit codes for comparison                       │
│  ✓ Clean data (remove NaN columns, empty rows)                      │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  STEP 2: PROJECT FILTERING                           │
│                     (main.py + excel_loader)                         │
├─────────────────────────────────────────────────────────────────────┤
│  Park Central  │  The Valleys   │  SLW (6 sheets combined)          │
│  - 1 sheet     │  - 1 sheet     │  - Boomerang                      │
│  - 29 units    │  - 25 units    │  - Villas                         │
│                │                │  - Monos                           │
│                │                │  - Solos                           │
│                │                │  - Twains                          │
│                │                │  - Shimmers                        │
│                │                │  Total: 66 units                   │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  STEP 3: UNIT COMPARISON                             │
│                 (processors/unit_comparator.py)                      │
├─────────────────────────────────────────────────────────────────────┤
│  For each project:                                                   │
│  ✓ Compare UNIT CODE against 107 existing codes                     │
│  ✓ Identify new units (not in current inventory)                    │
│  ✓ Filter out existing units                                        │
│  ✓ Return only truly new units                                      │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  STEP 4: DATA TRANSFORMATION                         │
│                (processors/data_transformer.py)                      │
├─────────────────────────────────────────────────────────────────────┤
│  For each new unit, transform:                                       │
│                                                                       │
│  UNIT CODE/UNIT CODES ────────────► default_code                    │
│  GROSS BUA/GROSS AREA ────────────► unit_area                       │
│  FLOOR (SECOND) ──────────────────► floor (2nd)                     │
│  Price/TOTAL PRICE ────────────────► list_price, unit_npv          │
│  UNIT TYPE (Three Bedrooms) ──────► number_of_rooms (3)             │
│  Unit Code Pattern ────────────────► project                         │
│  Logic (10% of price) ─────────────► maintenance_fee                │
│  Project + Unit Code ──────────────► finishing                       │
│  Generated Format ──────────────────► name                           │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                STEP 5: PROJECT IDENTIFICATION                        │
│              (utils/project_identifier.py)                           │
├─────────────────────────────────────────────────────────────────────┤
│  Unit Code Pattern → Project Name:                                  │
│                                                                       │
│  PC1-A3-06-LA-21 ──► Park Central - Mostakbal City                 │
│  VAL-V3-207-SV-G ──► VAL: The Valleys                              │
│  SLW-0500-... ─────► SLW: SwanLake West                            │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 STEP 6: FINISHING DETERMINATION                      │
│                  (utils/column_mapper.py)                            │
├─────────────────────────────────────────────────────────────────────┤
│  Park Central: Always "Fully Finished"                              │
│  The Valleys: Always "Fully Finished"                               │
│                                                                       │
│  SLW (based on unit number):                                        │
│  0100-0900 → Core and shell and near delivery                       │
│  1000-1999 → Serviced Apartments                                    │
│  2000-2999 → Fully Finished                                         │
│  3000-7000 → Core and shell, 4 years delivery                       │
│  8000+ ────→ Fully Finished                                         │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 7: NAME GENERATION                           │
│                  (utils/column_mapper.py)                            │
├─────────────────────────────────────────────────────────────────────┤
│  Format: {bedrooms}B {type} in {project} by Hassan Allam           │
│                                                                       │
│  Example Outputs:                                                    │
│  "3B Apartment in Park Central - Mostakbal City by Hassan Allam"   │
│  "2B Villa in VAL: The Valleys by Hassan Allam"                    │
│  "4B Penthouse in SLW: SwanLake West by Hassan Allam"              │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STEP 8: OUTPUT GENERATION                          │
│                          (main.py)                                   │
├─────────────────────────────────────────────────────────────────────┤
│  Generate Excel files in output/ directory:                          │
│                                                                       │
│  ✓ Park_Central_New_Units_20251216.xlsx                            │
│  ✓ The_Valleys_New_Units_20251216.xlsx                             │
│  ✓ SLW_New_Units_20251216.xlsx                                     │
│                                                                       │
│  Each with columns:                                                  │
│  1. default_code     6. unit_npv                                    │
│  2. unit_area        7. maintenance_fee                             │
│  3. finishing        8. number_of_rooms                             │
│  4. floor            9. project                                     │
│  5. list_price      10. name                                        │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STEP 9: LOGGING & REPORTING                        │
│                          (main.py)                                   │
├─────────────────────────────────────────────────────────────────────┤
│  ✓ Save processing log to logs/processing_YYYYMMDD_HHMMSS.log      │
│  ✓ Display summary in console                                       │
│  ✓ Show unit counts per project                                     │
│  ✓ List generated output files                                      │
│  ✓ Report any errors or warnings                                    │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FINAL OUTPUT                                 │
├─────────────────────────────────────────────────────────────────────┤
│  Ready-to-import Excel files with new units in standard format      │
│  Complete processing logs for audit trail                            │
│  Summary report with statistics                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### Input Data (New Availability):
```
UNIT CODE: PC1-A3-06-LA-21
UNIT TYPE: APARTMENT-Three Bedrooms
FLOOR: SECOND
GROSS AREA: 155
Price: 36715290.00
```

### Transformation Process:
```
1. Project Identification: PC → Park Central - Mostakbal City
2. Floor Conversion: SECOND → 2nd
3. Bedroom Extraction: Three Bedrooms → 3
4. Maintenance Calculation: 36715290 × 0.10 = 3671529
5. Finishing: Park Central → Fully Finished
6. Name Generation: 3B Apartment in Park Central - Mostakbal City by Hassan Allam
```

### Output Data (Standard Format):
```
default_code: PC1-A3-06-LA-21
unit_area: 155
finishing: Fully Finished
floor: 2nd
list_price: 36715290.00
unit_npv: 36715290.00
maintenance_fee: 3671529.00
number_of_rooms: 3
project: Park Central - Mostakbal City
name: 3B Apartment in Park Central - Mostakbal City by Hassan Allam
```

## Module Dependencies

```
main.py
  ├── config.py
  ├── processors/
  │   ├── excel_loader.py
  │   │   └── openpyxl, pandas
  │   ├── unit_comparator.py
  │   │   └── pandas
  │   └── data_transformer.py
  │       └── utils/column_mapper.py
  │       └── utils/project_identifier.py
  └── utils/
      ├── project_identifier.py
      │   └── config.py
      ├── column_mapper.py
      │   └── config.py
      │   └── utils/project_identifier.py
      └── validators.py
          └── pandas
```

## Execution Time

Typical processing time for current data:
- Load files: ~2 seconds
- Process Park Central (29 units): ~0.5 seconds
- Process The Valleys (25 units): ~0.5 seconds
- Process SLW (66 units): ~1.5 seconds
- Generate output: ~0.5 seconds

**Total: ~5 seconds**

## Error Handling Flow

```
Try to load file
  ├── Success → Continue processing
  └── Error → Log error, show message, exit gracefully

Try to find unit code column
  ├── Found → Continue comparison
  └── Not found → Log warning, skip sheet

Try to transform unit
  ├── All required fields present → Transform successfully
  └── Missing critical field → Log warning, skip unit
```

## Summary

The system provides a complete, automated solution for:
1. ✅ Loading multi-format Excel files
2. ✅ Identifying new units
3. ✅ Applying complex transformation rules
4. ✅ Generating properly formatted output
5. ✅ Comprehensive logging and reporting

All with minimal user interaction - just run `python main.py`!

