"""
Project Identifier Module
Determines project name based on unit code patterns
"""

from config import PROJECT_PATTERNS


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


def get_project_short_name(unit_code: str) -> str:
    """
    Get short project name for file naming.
    
    Args:
        unit_code: The unit code
    
    Returns:
        Short project name (e.g., 'Park_Central', 'The_Valleys', 'SLW')
    """
    project = identify_project(unit_code)
    
    if 'Park Central' in project:
        return 'Park_Central'
    elif 'Valleys' in project:
        return 'The_Valleys'
    elif 'SwanLake' in project or 'SLW' in project:
        return 'SLW'
    
    return 'Unknown'
