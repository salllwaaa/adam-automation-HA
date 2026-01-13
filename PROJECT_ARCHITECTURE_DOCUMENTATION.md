# 🏗️ Hassan Allam Inventory Automation System
## Complete Project Documentation & Architecture Guide

---

## 📋 Executive Summary

The **Hassan Allam Inventory Update Automation** is a Python-based automated system designed to streamline the management and tracking of real estate unit inventory across multiple Hassan Allam Properties (HAP) development projects. The system automatically processes Excel files containing new unit availability data, compares them against existing inventory, identifies new units, transforms data into a standardized format, and tracks unit availability states.

### Core Capabilities
| Feature | Description |
|---------|-------------|
| **Multi-Project Support** | Handles 3+ real estate projects with 8+ Excel sheets |
| **Automated State Tracking** | Identifies available/unavailable units automatically |
| **Smart Data Extraction** | 10+ bedroom format patterns supported |
| **Standardized Output** | 12-column standardized Excel output format |
| **Intelligent Rules Engine** | Project-specific finishing and pricing rules |
| **Comprehensive Logging** | Full audit trail with timestamped logs |

---

## 🎯 What the System Does

### Primary Functions

1. **Inventory Comparison**
   - Loads the current inventory database (`Current adam inv.xlsx`)
   - Loads new availability data (`New Availability.xlsx`)
   - Compares unit codes to identify **new units** not in current inventory
   - Flags existing units as `available` or `unavailable` based on presence in new availability

2. **Data Transformation**
   - Converts raw availability data from various formats to a standardized 12-column format
   - Applies project-specific business rules (finishing type, pricing, bedroom counts)
   - Generates calculated fields (maintenance fees, unit names)

3. **Multi-Project Processing**
   - Processes multiple HAP real estate projects simultaneously:
     - **Park Central** - Mostakbal City
     - **The Valleys (VAL)** - Luxury villas and townhouses
     - **SwanLake West (SLW)** - October City development
     - Additional projects (Phoenix, Selina, Little Venice, El Gouna, etc.)

4. **Output Generation**
   - Creates updated inventory files with state columns
   - Generates separate Excel files for new units per project
   - Produces processing summary reports

---

## 🏛️ System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INPUT LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  📁 Input/                                                                   │
│  ├── New Availability.xlsx          (Multi-sheet: Park Central, Valleys,   │
│  │                                    SLW-Villas, SLW-Monos, SLW-Twains...) │
│  └── Current adam inv.xlsx          (Current inventory database)            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PROCESSING LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │   ExcelLoader    │───▶│  UnitComparator  │───▶│ DataTransformer  │      │
│  │  (excel_loader)  │    │ (unit_comparator)│    │(data_transformer)│      │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘      │
│         │                        │                        │                  │
│         │                        │                        │                  │
│         ▼                        ▼                        ▼                  │
│  • Load Excel files      • Compare unit codes     • Apply transformations   │
│  • Smart header detect   • Find new units         • Extract bedrooms        │
│  • Filter by project     • Track availability     • Determine finishing     │
│  • Clean data            • Generate states        • Calculate fees          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            UTILITIES LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐    │
│  │ project_identifier │  │   column_mapper    │  │    validators      │    │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘    │
│  • Identify project      • Floor conversion      • Data validation         │
│    from unit code        • Bedroom extraction    • Type checking           │
│  • Pattern matching      • Name generation       • Required fields         │
│                          • Finishing rules                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OUTPUT LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  📁 output/                                                                  │
│  ├── Current_Inventory_Updated_YYYYMMDD.xlsx    (Updated with states)       │
│  ├── Park_Central_New_Units_YYYYMMDD.xlsx       (New units by project)      │
│  ├── The_Valleys_New_Units_YYYYMMDD.xlsx                                    │
│  ├── SLW_New_Units_YYYYMMDD.xlsx                                            │
│  └── processing_summary.txt                      (Summary report)           │
│                                                                              │
│  📁 logs/                                                                    │
│  └── processing_YYYYMMDD_HHMMSS.log             (Detailed processing log)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
Automate Updating HA/
│
├── 📄 main.py                      # Main orchestration script
├── 📄 config.py                    # All configurations & mappings
├── 📄 requirements.txt             # Python dependencies
│
├── 📁 processors/                  # Core processing modules
│   ├── excel_loader.py            # Excel file I/O operations
│   ├── unit_comparator.py         # Unit comparison logic
│   └── data_transformer.py        # Data transformation engine
│
├── 📁 utils/                       # Utility modules
│   ├── project_identifier.py      # Project detection from unit codes
│   ├── column_mapper.py           # Field transformation functions
│   └── validators.py              # Data validation utilities
│
├── 📁 tests/                       # Test suite (63 tests)
│   ├── conftest.py                # Shared test fixtures
│   ├── test_bedroom_extraction.py # Bedroom parsing tests
│   ├── test_transformations.py    # Transformation tests
│   ├── test_unit_comparator.py    # Comparison logic tests
│   ├── test_validation.py         # Validation tests
│   ├── test_project_identifier.py # Project ID tests
│   └── test_integration.py        # End-to-end tests
│
├── 📁 Input/                       # Input files location
│   ├── New Availability.xlsx      # Latest availability data
│   └── Current adam inv.xlsx      # Current inventory database
│
├── 📁 output/                      # Generated output files
├── 📁 logs/                        # Processing logs
└── 📁 Project_Docs/                # Project documentation
```

---

## 🔄 Detailed Processing Flow

### Step-by-Step Execution

```
┌────────────────────────────────────────────────────────────────────┐
│  STEP 1: INITIALIZATION                                            │
│  main.py → setup_logging()                                         │
├────────────────────────────────────────────────────────────────────┤
│  • Create timestamped log file                                     │
│  • Configure console + file logging                                │
│  • Create output directory if needed                               │
└────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│  STEP 2: EXCEL LOADING                                             │
│  ExcelLoader.__init__() + get_existing_unit_codes()                │
├────────────────────────────────────────────────────────────────────┤
│  • Validate input files exist                                      │
│  • Load Current Inventory → Extract existing unit codes            │
│  • Smart header detection (finds "UNIT CODE" row automatically)    │
│  • Clean data: remove NaN columns, empty rows                      │
└────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│  STEP 3: PROJECT FILTERING                                         │
│  ExcelLoader.filter_project_sheets()                               │
├────────────────────────────────────────────────────────────────────┤
│  For each project (Park Central, The Valleys, SLW):                │
│  • Match sheet names to project patterns                           │
│  • Load relevant sheets                                            │
│  • Combine multi-sheet projects (SLW has 6+ sheets)                │
└────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│  STEP 4: UNIT COMPARISON                                           │
│  UnitComparator.find_new_units()                                   │
├────────────────────────────────────────────────────────────────────┤
│  • Normalize unit codes (uppercase, trim whitespace)               │
│  • Compare against existing inventory set                          │
│  • Identify NEW units (not in current inventory)                   │
│  • Track units that became UNAVAILABLE                             │
└────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│  STEP 5: DATA TRANSFORMATION                                       │
│  DataTransformer.transform_units()                                 │
├────────────────────────────────────────────────────────────────────┤
│  For each new unit:                                                │
│  • Map source columns to standard output columns                   │
│  • Convert floor values (SECOND → 2nd)                             │
│  • Extract bedroom count (10+ format patterns)                     │
│  • Determine finishing based on project rules                      │
│  • Calculate maintenance fee (10% of price)                        │
│  • Generate standardized unit name                                 │
│  • Identify project from unit code prefix                          │
└────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│  STEP 6: STATE TRACKING                                            │
│  UnitComparator.generate_updated_inventory()                       │
├────────────────────────────────────────────────────────────────────┤
│  • Copy current inventory                                          │
│  • Add 'state' column                                              │
│  • Mark units as 'available' if in new availability               │
│  • Mark units as 'unavailable' if not found                       │
└────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│  STEP 7: OUTPUT GENERATION                                         │
│  save_output_files() + create_summary_report()                     │
├────────────────────────────────────────────────────────────────────┤
│  • Save updated inventory with states                              │
│  • Save new units files per project                                │
│  • Generate processing summary report                              │
│  • Log all operations with timestamps                              │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 Module Details

### 1. ExcelLoader (`processors/excel_loader.py`)

**Purpose**: Handles all Excel file I/O operations with intelligent parsing.

| Method | Description |
|--------|-------------|
| `__init__(new_path, current_path)` | Initialize with file paths, validate existence |
| `get_sheet_names(file_path)` | Get all sheet names from Excel file |
| `_find_header_row(df_raw)` | Smart detection of header row by finding "UNIT" keyword |
| `load_new_availability(sheet_name)` | Load new availability data with auto-header detection |
| `load_current_inventory()` | Load current inventory database |
| `get_existing_unit_codes()` | Extract list of existing unit codes |
| `filter_project_sheets(project_type)` | Filter sheets by project name pattern |

**Key Features**:
- **Smart Header Detection**: Automatically finds the row containing column headers
- **Multi-Sheet Support**: Handles Excel files with multiple project sheets
- **Data Cleaning**: Removes NaN columns and empty rows automatically

---

### 2. UnitComparator (`processors/unit_comparator.py`)

**Purpose**: Compares new availability against current inventory to identify changes.

| Method | Description |
|--------|-------------|
| `__init__(existing_codes)` | Initialize with existing unit codes set |
| `find_new_units(df, column)` | Find units not in existing inventory |
| `find_unavailable_units(df, column)` | Find units no longer in availability |
| `get_comparison_summary(df, column)` | Generate comparison statistics |
| `generate_updated_inventory(current, new)` | Add state column to inventory |

**State Logic**:
```python
state = 'available' if unit_code in new_availability else 'unavailable'
```

---

### 3. DataTransformer (`processors/data_transformer.py`)

**Purpose**: Transforms unit data from source format to standardized output format.

| Method | Description |
|--------|-------------|
| `transform_units(df)` | Transform all units in DataFrame |
| `_transform_single_unit(row)` | Transform individual unit row |
| `transform_by_project(df)` | Transform and group by project |
| `validate_transformed_data(df)` | Validate transformation output |

**Transformation Pipeline**:
```
Source Column          →    Target Column
──────────────────────────────────────────
UNIT CODE/UNIT CODES   →    default_code
GROSS BUA/GROSS AREA   →    unit_area
FLOOR                  →    floor (converted)
TOTAL PRICE            →    list_price, unit_npv
UNIT TYPE              →    unit_type, number_of_rooms
(calculated)           →    maintenance_fee (10%)
(generated)            →    name
(detected)             →    project
(always)               →    state = 'available'
```

---

### 4. Project Identifier (`utils/project_identifier.py`)

**Purpose**: Identifies project name from unit code patterns.

**Pattern Matching**:
| Unit Code Pattern | Identified Project |
|-------------------|-------------------|
| `PC1-...`, `PC-...` | Park Central - Mostakbal City |
| `VALL-...`, `VAL-...` | VAL: The Valleys |
| `SLW-...` | SLW: SwanLake West |

---

### 5. Column Mapper (`utils/column_mapper.py`)

**Purpose**: Handles all field-level transformations and business rules.

#### Floor Conversion
```
GROUND → Ground
FIRST → 1st
SECOND → 2nd
THIRD → 3rd
... and so on
```

#### Bedroom Extraction (10+ Patterns)
```
"Three Bedrooms"        → 3
"Town House / 3 Beds"   → 3
"TOWNHOUSE - 3 BED"     → 3
"3+living room"         → 3 (excludes living room)
"Standalone Villa G"    → 5 (via mapping table)
"2BR"                   → 2
```

#### Finishing Determination Rules

**Park Central & The Valleys**:
```
Always → "Fully Finished"
```

**SLW (SwanLake West) - By Unit Number**:
| Unit Number Range | Finishing Type | Description |
|-------------------|----------------|-------------|
| 0100-0900 | Core and shell and near delivery | Villas Phase 1 |
| 1000-1999 | Serviced Apartments | Monos |
| 2000-2999 | Fully Finished | Twains |
| 3000-7000 | Core and shell, 4 years delivery | Villas Phase 2 |
| 8000+ | Fully Finished | Shimmers Lagoon |

**All Other Projects** (Haptown, Little Venice, SLG, SLR, Keys, etc.):
```
→ Empty (no finishing value assigned)
```
> ⚠️ Projects without defined rules will have an empty finishing column. Add specific rules to `determine_finishing()` when finishing requirements are known.

---

## 📊 Output Format

### Standardized 12-Column Output

| Column | Description | Example |
|--------|-------------|---------|
| `default_code` | Unit identifier | PC1-A3-06-LA-21 |
| `unit_area` | Area in square meters | 155 |
| `finishing` | Finishing type | Fully Finished |
| `floor` | Floor number (formatted) | 2nd |
| `list_price` | Unit price | 36,715,290.00 |
| `unit_npv` | Net present value | 36,715,290.00 |
| `name` | Generated name | "3B Apartment in Park Central..." |
| `number_of_rooms` | Bedroom count | 3 |
| `project` | Project name | Park Central - Mostakbal City |
| `maintenance_fee` | 10% of price | 3,671,529.00 |
| `unit_type` | Type (Apartment, Villa, etc.) | Apartment |
| `state` | Availability state | available |

### Example Transformation

**Input (New Availability)**:
```
UNIT CODE: PC1-A3-06-LA-21
UNIT TYPE: APARTMENT-Three Bedrooms
FLOOR: SECOND
GROSS AREA: 155
Price: 36715290.00
```

**Output (Standard Format)**:
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
unit_type: Apartment
state: available
```

---

## ⚙️ Configuration (`config.py`)

### Key Configuration Mappings

```python
# File Paths
NEW_AVAILABILITY_FILE = 'Input/New Availability.xlsx'
CURRENT_INVENTORY_FILE = 'Input/Current adam inv.xlsx'
OUTPUT_DIRECTORY = 'output'
LOG_DIRECTORY = 'logs'

# Maintenance Fee
MAINTENANCE_FEE_PERCENTAGE = 0.10  # 10%

# Project Identification Patterns
PROJECT_PATTERNS = {
    'PC': 'Park central - Mostakbal City',
    'VALL': 'VAL: The Valleys',
    'SLW': 'SLW: SwanLake West',
}

# Sheet Name Patterns
SHEET_PATTERNS = {
    'Park Central': ['Park Central'],
    'The Valleys': ['The Valleys'],
    'SLW': ['SLW-Villas', 'SLW-Monos', 'SLW-Twains', ...],
}
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
```bash
pip install -r requirements.txt
```

### Execution
```bash
python main.py
```

### Required Input Files
1. `Input/New Availability.xlsx` - Latest availability data from HAP
2. `Input/Current adam inv.xlsx` - Current inventory database

### Output Files
Located in `output/` directory:
- `Current_Inventory_Updated_YYYYMMDD.xlsx`
- `{Project}_New_Units_YYYYMMDD.xlsx` (per project)
- `processing_summary.txt`

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Processing Speed | ~107 units in ~2 seconds |
| Test Suite | 63 tests (100% passing) |
| Test Execution Time | 0.83 seconds |
| Supported Projects | 3+ primary, 10+ total |
| Bedroom Patterns | 10+ formats |
| Memory Efficient | Handles 10,000+ rows |

---

## 🔧 Error Handling

The system implements graceful error handling at multiple levels:

1. **File Level**: Validates file existence before processing
2. **Sheet Level**: Skips problematic sheets with warnings
3. **Row Level**: Skips invalid rows, logs warnings
4. **Field Level**: Uses defaults for missing non-critical fields

All errors are logged to timestamped log files in `logs/` directory.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Quick run
python run_tests.py
```

**Test Coverage**: 63 tests covering:
- Bedroom extraction (all 10+ patterns)
- Floor conversion
- Project identification
- Unit comparison logic
- Data transformation
- Integration tests

---

## 📝 Summary

The Hassan Allam Inventory Automation System is a **production-ready** solution that:

1. ✅ Automates manual inventory comparison work
2. ✅ Handles complex multi-project, multi-sheet Excel files
3. ✅ Applies sophisticated business rules per project
4. ✅ Produces standardized, ready-to-import output
5. ✅ Maintains complete audit trail via logging
6. ✅ Is fully tested with 100% test pass rate

**Version**: 1.3  
**Last Updated**: January 2026  
**Status**: Production Ready

---

*Documentation generated for Metrics-eg Organization*


