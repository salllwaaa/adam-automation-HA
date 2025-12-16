"""
Column Mapper Module
Handles transformation of data fields from source to target format
"""

import re
from typing import Optional
from config import (
    FLOOR_MAPPING, 
    BEDROOM_MAPPING, 
    DEVELOPER,
    VALLEYS_UNIT_TYPE_BEDROOMS,
    SLW_UNIT_TYPE_BEDROOMS,
    SLW_TWAINS_BEDROOMS
)
from utils.project_identifier import identify_project


def convert_floor(floor_value) -> str:
    """
    Convert floor value from source format to target format.
    
    Args:
        floor_value: Floor value (e.g., 'SECOND', 'FIRST', 'GROUND')
    
    Returns:
        Converted floor (e.g., '2nd', '1st', 'Ground')
    
    Examples:
        >>> convert_floor('SECOND')
        '2nd'
        >>> convert_floor('GROUND')
        'Ground'
    """
    if not floor_value:
        return ''
    
    floor_str = str(floor_value).upper().strip()
    
    # Direct mapping lookup
    if floor_str in FLOOR_MAPPING:
        return FLOOR_MAPPING[floor_str]
    
    # Try to extract number from strings like '2nd', '3rd', etc.
    # Already in correct format
    if any(suffix in floor_str for suffix in ['ST', 'ND', 'RD', 'TH']):
        return floor_str.title()
    
    return floor_str


def lookup_bedroom_by_unit_type(unit_type: str, project: str) -> int:
    """
    Look up bedroom count from predefined mappings based on unit type and project.
    Used when bedroom info is not in the data itself.
    
    Args:
        unit_type: Unit type (e.g., 'Standalone Villa G', 'Twin House')
        project: Project name
    
    Returns:
        Number of bedrooms from mapping, or 0 if not found
    """
    if not unit_type:
        return 0
    
    unit_type_upper = str(unit_type).upper().strip()
    
    # The Valleys - use Valleys mapping
    if 'VALLE' in project.upper():
        for key, bedrooms in VALLEYS_UNIT_TYPE_BEDROOMS.items():
            if key.upper() in unit_type_upper:
                return bedrooms
    
    # SLW - use SLW mapping
    elif 'SLW' in project.upper() or 'SWANLAKE' in project.upper():
        # Check if it's Twains (all 3 bedrooms)
        if 'TWAIN' in unit_type_upper:
            return SLW_TWAINS_BEDROOMS
        
        # Otherwise check SLW mapping
        for key, bedrooms in SLW_UNIT_TYPE_BEDROOMS.items():
            if key.upper() in unit_type_upper:
                return bedrooms
    
    return 0


def extract_bedroom_count(unit_type: str, project: str = None) -> int:
    """
    Extract number of bedrooms from unit type string.
    
    Args:
        unit_type: Unit type with various formats:
        - 'PENTHOUSE-Three Bedrooms'
        - 'Town House (M) / 3 Beds'
        - 'Standalone Villa G / 5 Beds'
        - 'TOWNHOUSE (M) - 3 BED'
        - 'STANDALONE SV - A 3+living room'
    
    Returns:
        Number of bedrooms as integer
    
    Examples:
        >>> extract_bedroom_count('PENTHOUSE-Three Bedrooms')
        3
        >>> extract_bedroom_count('Town House (M) / 3 Beds')
        3
        >>> extract_bedroom_count('Standalone Villa G / 5 Beds')
        5
    """
    if not unit_type:
        return 0
    
    unit_type_upper = str(unit_type).upper().strip()
    
    # Check bedroom mapping (text to number: "Three Bedrooms" -> 3)
    for bedroom_text, count in BEDROOM_MAPPING.items():
        if bedroom_text in unit_type_upper:
            return count
    
    # Pattern 1: "/ 3 Beds", "/ 4 Beds", "- 3 BED", "5 beds+living"
    number_match = re.search(r'(\d+)\s*BEDS?', unit_type_upper)
    if number_match:
        return int(number_match.group(1))
    
    # Pattern 2: "3 bedrooms", "4 Bedrooms" (anywhere in string)
    number_match = re.search(r'(\d+)\s*BEDROOM', unit_type_upper)
    if number_match:
        return int(number_match.group(1))
    
    # Pattern 3: "3+living room", "3+ living", "3+MAID", "3+driver", "3+nanny"
    # Extract ONLY the bedroom number before the "+"
    number_match = re.search(r'(\d+)\s*\+', unit_type_upper)
    if number_match:
        return int(number_match.group(1))  # Returns only the bedrooms, excludes living/maid/driver/nanny
    
    # Pattern 4: "2BR", "3B " (with space after B)
    number_match = re.search(r'(\d+)\s*(?:BR|B\s)', unit_type_upper)
    if number_match:
        return int(number_match.group(1))
    
    # Pattern 5: Just a number in the NUMBER OF BEDROOMS column
    if unit_type_upper.strip().isdigit():
        num = int(unit_type_upper.strip())
        if 0 <= num <= 10:
            return num
    
    # Pattern 6: Last resort - find any single digit number (but be careful)
    # Only use if unit type contains villa/house/apartment keywords
    if any(keyword in unit_type_upper for keyword in ['VILLA', 'HOUSE', 'APARTMENT', 'PENTHOUSE', 'DUPLEX', 'TWIN', 'TOWN']):
        number_match = re.search(r'\b(\d)\b', unit_type_upper)
        if number_match:
            num = int(number_match.group(1))
            if 1 <= num <= 10:  # Must be reasonable bedroom count
                return num
    
    # Pattern 7: Lookup from predefined mappings (Valleys & SLW)
    if project:
        mapped_bedrooms = lookup_bedroom_by_unit_type(unit_type, project)
        if mapped_bedrooms > 0:
            return mapped_bedrooms
    
    return 0


def generate_unit_name(unit_type: str, unit_code: str, bedrooms: int = None) -> str:
    """
    Generate unit name in format: "{rooms}B {type} in {project} by {developer}"
    
    Args:
        unit_type: Unit type string
        unit_code: Unit code for project identification
        bedrooms: Number of bedrooms (if already extracted, otherwise will extract from unit_type)
    
    Returns:
        Formatted unit name
    
    Examples:
        >>> generate_unit_name('APARTMENT-Three Bedrooms', 'PC1-A3-06-LA-21')
        '3B Apartment in Park Central - Mostakbal City by Hassan Allam'
        >>> generate_unit_name('APARTMENT', 'PC1-A3-06-LA-21', 3)
        '3B Apartment in Park Central - Mostakbal City by Hassan Allam'
    """
    # Use provided bedroom count or extract from unit_type
    if bedrooms is None:
        bedrooms = extract_bedroom_count(unit_type)
    
    project = identify_project(unit_code)
    
    # Extract unit type (APARTMENT, PENTHOUSE, DUPLEX, etc.)
    type_name = 'Unit'
    if unit_type:
        # Split by hyphen or space and get first part
        parts = str(unit_type).split('-')
        if parts:
            type_name = parts[0].strip().title()
    
    return f"{bedrooms}B {type_name} in {project} by {DEVELOPER}"


def calculate_maintenance_fee(price: float, percentage: float = 0.10) -> float:
    """
    Calculate maintenance fee as percentage of price.
    
    Args:
        price: Unit price
        percentage: Percentage (default 0.10 for 10%)
    
    Returns:
        Maintenance fee amount
    """
    if not price or price <= 0:
        return 0.0
    
    return float(price) * percentage


def determine_finishing(project: str, unit_code: str = '') -> str:
    """
    Determine finishing based on project and unit code.
    
    Args:
        project: Project name
        unit_code: Unit code (used for SLW specific rules)
    
    Returns:
        Finishing status
    
    SLW Finishing Rules (SwanLake West - October):
    - 0100s to 0900s: Villas phase 1 (Core and shell and near delivery)
    - 1000s: Monos Serviced Apartments
    - 2000s: Twain fully finished apartments
    - 3000s up to 7000s: Villas Phase 2 (Core and shell, 4 years delivery)
    - 8000s: Shimmers lagoon apartments fully finished
    """
    if 'Park Central' in project or 'Valleys' in project:
        return 'Fully Finished'
    
    elif 'SLW' in project or 'SwanLake' in project:
        # Extract number from unit code for SLW projects
        import re
        
        # Try to find a 4-digit number in the unit code
        number_match = re.search(r'(\d{4})', unit_code)
        if number_match:
            unit_number = int(number_match.group(1))
            
            # Apply SLW finishing rules based on unit number ranges (October)
            if 100 <= unit_number <= 900:
                return 'Core and shell and near delivery'  # Villas phase 1
            elif 1000 <= unit_number <= 1999:
                return 'Serviced Apartments'  # Monos
            elif 2000 <= unit_number <= 2999:
                return 'Fully Finished'  # Twain fully finished apartments
            elif 3000 <= unit_number <= 7000:
                return 'Core and shell, 4 years delivery'  # Villas Phase 2
            elif unit_number >= 8000:
                return 'Fully Finished'  # Shimmers lagoon apartments
        
        # If no number found or doesn't match ranges, return default
        return 'Fully Finished'
    
    return 'Fully Finished'


def clean_numeric_value(value) -> Optional[float]:
    """
    Clean and convert numeric values, handling various formats.
    
    Args:
        value: Value to clean (may have commas, spaces, etc.)
    
    Returns:
        Float value or None
    """
    if value is None or value == '':
        return None
    
    try:
        # Remove commas and spaces
        if isinstance(value, str):
            cleaned = value.replace(',', '').replace(' ', '').strip()
            return float(cleaned)
        return float(value)
    except (ValueError, TypeError):
        return None
