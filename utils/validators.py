"""
Validators Module
Data validation and quality checks
"""

import pandas as pd
from typing import List, Tuple
import logging


def validate_required_columns(df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, List[str]]:
    """
    Check if DataFrame contains all required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
    
    Returns:
        Tuple of (is_valid, missing_columns)
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    is_valid = len(missing_columns) == 0
    
    return is_valid, missing_columns


def validate_unit_code(unit_code) -> bool:
    """
    Validate unit code format.
    
    Args:
        unit_code: Unit code to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not unit_code or pd.isna(unit_code):
        return False
    
    unit_code_str = str(unit_code).strip()
    return len(unit_code_str) > 0


def log_data_quality_issues(df: pd.DataFrame, sheet_name: str = '') -> None:
    """
    Log data quality issues found in DataFrame.
    
    Args:
        df: DataFrame to check
        sheet_name: Name of sheet for logging context
    """
    logger = logging.getLogger(__name__)
    
    if sheet_name:
        context = f"[{sheet_name}] "
    else:
        context = ""
    
    # Check for missing unit codes
    if 'UNIT CODE' in df.columns:
        missing_codes = df['UNIT CODE'].isna().sum()
        if missing_codes > 0:
            logger.warning(f"{context}Found {missing_codes} rows with missing UNIT CODE")
    
    # Check for missing prices
    if 'TOTAL PRICE' in df.columns:
        missing_prices = df['TOTAL PRICE'].isna().sum()
        if missing_prices > 0:
            logger.warning(f"{context}Found {missing_prices} rows with missing TOTAL PRICE")
    
    # Check for duplicates
    if 'UNIT CODE' in df.columns:
        duplicates = df['UNIT CODE'].duplicated().sum()
        if duplicates > 0:
            logger.warning(f"{context}Found {duplicates} duplicate UNIT CODEs")

