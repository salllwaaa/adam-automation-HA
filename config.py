"""
Configuration file for Hassan Allam Inventory Automation
Contains all mappings, transformation rules, and project settings
"""

# Floor conversion mapping
FLOOR_MAPPING = {
    'GROUND': 'Ground',
    'FIRST': '1st',
    'SECOND': '2nd',
    'THIRD': '3rd',
    'FOURTH': '4th',
    'FIFTH': '5th',
    'SIXTH': '6th',
    'SEVENTH': '7th',
    'EIGHTH': '8th',
    'NINTH': '9th',
    'TENTH': '10th',
    '1ST': '1st',
    '2ND': '2nd',
    '3RD': '3rd',
    '4TH': '4th',
    '5TH': '5th',
    '6TH': '6th',
    '7TH': '7th',
    '8TH': '8th',
    '9TH': '9th',
    '10TH': '10th',
}

# Bedroom text to number conversion
BEDROOM_MAPPING = {
    'STUDIO': 0,
    'ONE BEDROOM': 1,
    'TWO BEDROOMS': 2,
    'THREE BEDROOMS': 3,
    'FOUR BEDROOMS': 4,
    'FIVE BEDROOMS': 5,
    'SIX BEDROOMS': 6,
    'SEVEN BEDROOMS': 7,
    'EIGHT BEDROOMS': 8,
}

# Project identification patterns
PROJECT_PATTERNS = {
    'PC': 'Park Central - Mostakbal City',
    'VALL': 'VAL: The Valleys',
    'SLW': 'SLW: SwanLake West',
}

# Project finishing rules
PROJECT_FINISHING = {
    'Park Central - Mostakbal City': 'Fully Finished',
    'VAL: The Valleys': 'Fully Finished',
    'SLW: SwanLake West': 'TBD',  # Will be updated based on unit code rules
}

# Developer name
DEVELOPER = 'Hassan Allam'

# Column mapping from source (New Availability) to target (Current Inv)
COLUMN_MAPPING = {
    'UNIT CODE': 'default_code',
    'UNIT TYPE': None,  # Used for extraction, not direct mapping
    'FLOOR': 'floor',
    'GROSS BUA': 'unit_area',
    'TOTAL PRICE': ['list_price', 'unit_npv'],  # Maps to multiple columns
}

# Columns to skip from source
SKIP_COLUMNS = [
    'Zone',
    'Cluster',
    'Total Garden Area',
    'Open Roof Terrace',
    'GARDEN',
    'Roof Terrace Area',
    '5% Reservation',
    '5% Reservation 2',
    'TOTAL PRICE 2',
    'TOTAL PRICE 3',
]

# Output columns in order (matching "The Current inv.xlsx" format)
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
    'state',
]

# Sheet name patterns for each project
SHEET_PATTERNS = {
    'Park Central': ['Park Central'],
    'The Valleys': ['The Valleys'],
    'SLW': ['SLW-Villas', 'SLW-Monos', 'SLW-Solos', 'SLW-Twains', 'SLW-Shi'],  # All sheets containing SLW
}

# File paths
NEW_AVAILABILITY_FILE = 'New Availability.xlsx'
CURRENT_INVENTORY_FILE = 'The Current inv.xlsx'
OUTPUT_DIRECTORY = 'output'
LOG_DIRECTORY = 'logs'

# Maintenance fee calculation
MAINTENANCE_FEE_PERCENTAGE = 0.10  # 10% of price

# Unit Type to Bedroom Count Mappings (from marketing materials)
# Used when NUMBER OF BEDROOMS column is not available

# The Valleys - Villa Types
VALLEYS_UNIT_TYPE_BEDROOMS = {
    'TOWNHOUSE (M)': 3,
    'TOWNHOUSE M': 3,
    'TOWN HOUSE (M)': 3,
    'TOWN HOUSE M': 3,
    'TOWNHOUSE (C)': 4,
    'TOWNHOUSE C': 4,
    'TOWN HOUSE (C)': 4,
    'TOWN HOUSE C': 4,
    'TWIN HOUSE': 4,
    'TWIN VILLA A': 4,
    'TWIN VILLA B': 4,
    'TWIN LOFT VILLA': 3,
    'STANDALONE VILLA D': 4,
    'STANDALONE VILLA F': 4,
    'STANDALONE VILLA G': 5,
    'STANDALONE VILLA A': 4,
    'STANDALONE VILLA B': 5,
    'STANDALONE VILLA C': 5,
    'STANDALONE SV - D': 5,
    'STANDALONE SV - E': 5,
    'STANDALONE SV - L': 5,
}

# SLW - Villa Types
SLW_UNIT_TYPE_BEDROOMS = {
    'TOWNHOUSE (M)': 3,
    'TOWNHOUSE M': 3,
    'TOWN HOUSE (M)': 3,
    'TWIN LOFT VILLA': 3,
    'TWIN HOUSE': 3,
    'TWIN VILLA': 3,
    'STANDALONE SV - A': 3,
    'STANDALONE SV - I': 3,
    'STANDALONE SV - X': 4,
    'STANDALONE SV - D': 5,
    'STANDALONE SV - E': 5,
    'STANDALONE SV - L': 5,
    'STANDALONE VILLA': 4,  # Default
    'STANDALONE LOFT VILLA': 3,
}

# SLW Twains - All units are 3 bedrooms
SLW_TWAINS_BEDROOMS = 3

# SLW Finishing Rules (SwanLake West - October)
SLW_FINISHING_RULES = {
    'range_0100_0900': {
        'range': (100, 900),
        'finishing': 'Core and shell and near delivery',
        'description': 'Villas phase 1'
    },
    'range_1000s': {
        'range': (1000, 1999),
        'finishing': 'Serviced Apartments',
        'description': 'Monos Serviced Apartments'
    },
    'range_2000s': {
        'range': (2000, 2999),
        'finishing': 'Fully Finished',
        'description': 'Twain fully finished apartments'
    },
    'range_3000_7000': {
        'range': (3000, 7000),
        'finishing': 'Core and shell, 4 years delivery',
        'description': 'Villas Phase 2'
    },
    'range_8000s': {
        'range': (8000, 99999),
        'finishing': 'Fully Finished',
        'description': 'Shimmers lagoon apartments'
    }
}