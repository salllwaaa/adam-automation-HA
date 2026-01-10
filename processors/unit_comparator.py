"""
Unit Comparator Module
Compares new availability against current inventory to identify new units
"""

import pandas as pd
import logging
from typing import List, Set


logger = logging.getLogger(__name__)


class UnitComparator:
    """Handles comparison between new availability and current inventory"""
    
    def __init__(self, existing_unit_codes: List[str]):
        """
        Initialize comparator with existing unit codes.
        
        Args:
            existing_unit_codes: List of unit codes from current inventory
        """
        # Convert to set for faster lookup and normalize
        self.existing_codes = set(str(code).strip().upper() for code in existing_unit_codes if pd.notna(code))
        logger.info(f"Initialized comparator with {len(self.existing_codes)} existing unit codes")
    
    def find_new_units(self, df: pd.DataFrame, unit_code_column: str = 'UNIT CODE') -> pd.DataFrame:
        """
        Find units in DataFrame that are not in existing inventory.
        
        Args:
            df: DataFrame with new availability data
            unit_code_column: Name of column containing unit codes
        
        Returns:
            DataFrame containing only new units
        """
        # Try to find the unit code column with variations
        actual_column = None
        for col in df.columns:
            if isinstance(col, str) and col.upper() in ['UNIT CODE', 'UNIT CODES', 'UNIT_CODE', 'UNIT_CODES']:
                actual_column = col
                break
        
        if actual_column is None:
            logger.error(f"Unit code column not found. Available columns: {df.columns.tolist()}")
            return pd.DataFrame()
        
        unit_code_column = actual_column
        
        # Create a copy to avoid modifying original
        df_copy = df.copy()
        
        # Remove rows with missing unit codes
        df_copy = df_copy[df_copy[unit_code_column].notna()]
        
        if len(df_copy) == 0:
            logger.warning("No valid unit codes found in DataFrame")
            return pd.DataFrame()
        
        # Normalize unit codes for comparison
        df_copy['_normalized_code'] = df_copy[unit_code_column].astype(str).str.strip().str.upper()
        
        # Filter for new units (not in existing inventory)
        new_units_mask = ~df_copy['_normalized_code'].isin(self.existing_codes)
        new_units = df_copy[new_units_mask].copy()
        
        # Remove temporary column
        new_units = new_units.drop(columns=['_normalized_code'])
        
        logger.info(f"Found {len(new_units)} new units out of {len(df_copy)} total units")
        
        return new_units
    
    def find_unavailable_units(self, df: pd.DataFrame, unit_code_column: str = 'UNIT CODE') -> List[str]:
        """
        Find units that exist in current inventory but not in new availability.
        These units have become unavailable.
        
        Args:
            df: DataFrame with new availability data
            unit_code_column: Name of column containing unit codes
        
        Returns:
            List of unit codes that are no longer available
        """
        if unit_code_column not in df.columns:
            logger.error(f"Column '{unit_code_column}' not found in DataFrame")
            return []
        
        # Get normalized unit codes from new availability
        new_codes = set()
        for code in df[unit_code_column].dropna():
            normalized = str(code).strip().upper()
            new_codes.add(normalized)
        
        # Find codes in existing but not in new
        unavailable = self.existing_codes - new_codes
        
        logger.info(f"Found {len(unavailable)} units that became unavailable")
        
        return list(unavailable)
    
    def get_comparison_summary(self, df: pd.DataFrame, unit_code_column: str = 'UNIT CODE') -> dict:
        """
        Get summary statistics of comparison.
        
        Args:
            df: DataFrame with new availability data
            unit_code_column: Name of column containing unit codes
        
        Returns:
            Dictionary with summary statistics
        """
        new_units = self.find_new_units(df, unit_code_column)
        unavailable = self.find_unavailable_units(df, unit_code_column)
        
        total_in_new_availability = df[unit_code_column].notna().sum()
        
        summary = {
            'total_existing_inventory': len(self.existing_codes),
            'total_in_new_availability': total_in_new_availability,
            'new_units_count': len(new_units),
            'unavailable_units_count': len(unavailable),
            'common_units_count': total_in_new_availability - len(new_units)
        }
        
        return summary
    
    def generate_updated_inventory(
        self, 
        current_inventory_df: pd.DataFrame, 
        new_availability_df: pd.DataFrame,
        unit_code_column_current: str = 'default_code',
        unit_code_column_new: str = 'UNIT CODE'
    ) -> pd.DataFrame:
        """
        Generate updated inventory with state column showing availability.
        
        Args:
            current_inventory_df: Current inventory DataFrame
            new_availability_df: New availability DataFrame
            unit_code_column_current: Column name in current inventory
            unit_code_column_new: Column name in new availability
        
        Returns:
            Updated DataFrame with state column
        """
        logger.info("Generating updated inventory with state column")
        
        # Create a copy of current inventory
        updated_df = current_inventory_df.copy()
        
        # Get normalized unit codes from new availability
        # Find ALL unit code columns (there might be multiple with different names)
        unit_code_columns = []
        for col in new_availability_df.columns:
            if isinstance(col, str) and col.upper() in ['UNIT CODE', 'UNIT CODES', 'UNIT_CODE', 'UNIT_CODES']:
                unit_code_columns.append(col)
        
        new_codes = set()
        if unit_code_columns:
            logger.info(f"Found {len(unit_code_columns)} unit code columns: {unit_code_columns}")
            for col in unit_code_columns:
                for code in new_availability_df[col].dropna():
                    normalized = str(code).strip().upper()
                    new_codes.add(normalized)
        else:
            logger.warning("Could not find any unit code columns in new availability")
        
        # Create normalized column for comparison
        updated_df['_normalized_code'] = updated_df[unit_code_column_current].astype(str).str.strip().str.upper()
        
        # Set state based on availability
        updated_df['state'] = updated_df['_normalized_code'].apply(
            lambda code: 'available' if code in new_codes else 'unavailable'
        )
        
        # Remove temporary column
        updated_df = updated_df.drop(columns=['_normalized_code'])
        
        available_count = (updated_df['state'] == 'available').sum()
        unavailable_count = (updated_df['state'] == 'unavailable').sum()
        
        logger.info(f"State summary: {available_count} available, {unavailable_count} unavailable")
        
        return updated_df
