"""
Project Identifier Module
Determines project name based on unit code patterns or sheet names
"""

from config import PROJECT_PATTERNS, SHEET_TO_PROJECT_MAPPING


def identify_project(unit_code: str) -> str:
    """
    Identify project based on unit code pattern.
    
    Args:
        unit_code: The unit code (e.g., 'PC1-A3-06-LA-21', 'VALL-123', 'SLW-ABC')
    
    Returns:
        Project name as string
    
    Examples:
        >>> identify_project('PC1-A3-06-LA-21')
        'Park Central - Mostakbal City'
        >>> identify_project('VALL-A01-12')
        'VAL: The Valleys'
        >>> identify_project('SLW-M-01-23')
        'SLW: SwanLake West'
    """
    if not unit_code or not isinstance(unit_code, str):
        return 'Unknown'
    
    unit_code_upper = unit_code.upper().strip()
    
    # Check for each project pattern
    if unit_code_upper.startswith('PC') or 'PC1' in unit_code_upper or 'PC-' in unit_code_upper:
        return PROJECT_PATTERNS['PC']
    elif 'VALL' in unit_code_upper or unit_code_upper.startswith('VAL'):
        return PROJECT_PATTERNS['VALL']
    elif unit_code_upper.startswith('SLW') or 'SLW-' in unit_code_upper:
        return PROJECT_PATTERNS['SLW']
    
    return 'Unknown'


def identify_project_from_sheet(sheet_name: str) -> str:
    """
    Identify project from sheet name.
    
    Args:
        sheet_name: The Excel sheet name
    
    Returns:
        Project name as string
    
    Examples:
        >>> identify_project_from_sheet('Park Central')
        'Park central - Mostakbal City'
        >>> identify_project_from_sheet('The Phoenix')
        'SLR: SwanLake Residences - The Phoenix'
    """
    return SHEET_TO_PROJECT_MAPPING.get(sheet_name, f'Unknown: {sheet_name}')


def get_project_short_name(project_name: str) -> str:
    """
    Get short project name for file naming.
    
    Args:
        project_name: The full project name
    
    Returns:
        Short project name for file naming
    """
    # Case-insensitive check for Park Central
    if 'Park' in project_name and 'central' in project_name.lower():
        return 'Park_Central'
    elif 'Valleys' in project_name:
        return 'The_Valleys'
    elif 'SLW' in project_name and 'SwanLake West' in project_name:
        return 'SLW'
    elif 'SLN' in project_name:
        return 'SwanLake_North'
    elif 'SLR' in project_name:
        # Extract sub-project name (e.g., "The Phoenix" from "SLR: SwanLake Residences - The Phoenix")
        if ' - ' in project_name:
            sub_project = project_name.split(' - ')[-1].replace(' ', '_')
            return f'SLR_{sub_project}'
        return 'SwanLake_Residences'
    elif 'SLG' in project_name:
        if 'ENCORE' in project_name:
            return 'SLG_ENCORE'
        return 'SwanLake_ElGouna'
    elif 'Haptown' in project_name:
        # Extract sub-project (e.g., "PARKVIEW" from "Haptown - PARKVIEW")
        if ' - ' in project_name:
            sub_project = project_name.split(' - ')[-1].replace(' ', '_')
            return f'Haptown_{sub_project}'
        return 'Haptown'
    elif 'Keys 52' in project_name:
        return 'Keys_52'
    elif 'Little Venice Gardens' in project_name:
        return 'Little_Venice_Gardens'
    elif 'SwanLake October' in project_name:
        return 'SwanLake_October'
    elif 'Little Venice' in project_name:
        return 'Little_Venice'
    
    # Default: replace spaces with underscores
    return project_name.replace(' ', '_').replace(':', '').replace('-', '_')
