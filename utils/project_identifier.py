"""
Project Identifier Module
Determines project name based on unit code patterns
Auto-detects projects from unit code prefixes
"""

import re


# Extended project patterns mapping (prefix -> project name)
PROJECT_PATTERNS = {
    # Original projects
    'PC': 'Park_Central',
    'VAL': 'The_Valleys',
    'VALL': 'The_Valleys',
    'SLW': 'SwanLake_October',
    
    # Haptown projects
    'HPT': 'Haptown',
    'HAPTOWN': 'Haptown',
    'PARK226': 'Haptown_Park_226',
    'PARK 226': 'Haptown_Park_226',
    'PARKVIEW': 'Haptown_PARKVIEW',
    'PARK VIEW': 'Haptown_PARKVIEW',
    'SEASONS': 'Haptown_SEASONS',
    
    # Little Venice
    'LV': 'Little_Venice',
    'LVG': 'Little_Venice_Gardens',
    
    # SwanLake variants
    'SLN': 'SwanLake_North',
    'SLG': 'SwanLake_ElGouna',
    'SLE': 'SwanLake_ElGouna',
    'SLO': 'SwanLake_October',
    
    # SLR projects (Swan Lake Residences)
    'SLR': 'SLR',
    'PHOENIX': 'SLR_The_Phoenix',
    'SELINA': 'SLR_The_Selina',
    'AMAIA': 'SLR_The_AMAIA',
    
    # Other projects
    'KEYS': 'Keys_52',
    'KEY': 'Keys_52',
    'ENCORE': 'SLG_ENCORE',
}


def identify_project(unit_code: str, sheet_name: str = None) -> str:
    """
    Identify project based on unit code pattern or sheet name.
    Auto-detects project from unit code prefix.
    
    Args:
        unit_code: The unit code (e.g., 'PC1-A3-06-LA-21', 'VALL-123', 'SLW-ABC')
        sheet_name: Optional sheet name to help identify project
    
    Returns:
        Project name as string (formatted for file naming)
    """
    if not unit_code or not isinstance(unit_code, str):
        # Try to use sheet name if unit code is invalid
        if sheet_name:
            return _clean_project_name(sheet_name)
        return 'Unknown'
    
    unit_code_upper = unit_code.upper().strip()
    
    # Try to match known patterns
    for pattern, project_name in PROJECT_PATTERNS.items():
        if unit_code_upper.startswith(pattern) or pattern in unit_code_upper:
            return project_name
    
    # Auto-extract prefix from unit code (before first dash or number)
    prefix_match = re.match(r'^([A-Za-z]+)', unit_code_upper)
    if prefix_match:
        prefix = prefix_match.group(1)
        if len(prefix) >= 2:
            return _clean_project_name(prefix)
    
    # If still unknown, try using sheet name
    if sheet_name:
        return _clean_project_name(sheet_name)
    
    return 'Unknown'


def _clean_project_name(name: str) -> str:
    """
    Clean and format project name for file naming.
    
    Args:
        name: Raw project/sheet name
    
    Returns:
        Cleaned project name (spaces replaced with underscores)
    """
    if not name:
        return 'Unknown'
    
    # Remove special characters, replace spaces with underscores
    cleaned = re.sub(r'[^\w\s-]', '', str(name))
    cleaned = re.sub(r'\s+', '_', cleaned.strip())
    
    return cleaned or 'Unknown'


def get_project_short_name(unit_code: str, sheet_name: str = None) -> str:
    """
    Get short project name for file naming.
    
    Args:
        unit_code: The unit code
        sheet_name: Optional sheet name
    
    Returns:
        Short project name for file naming
    """
    return identify_project(unit_code, sheet_name)
