"""
Data Transformer Module
Transforms units from source format to target standard format
"""

import pandas as pd
import logging
from typing import Dict, Optional
from utils.column_mapper import (
    convert_floor,
    extract_bedroom_count,
    generate_unit_name,
    calculate_maintenance_fee,
    determine_finishing,
    clean_numeric_value
)
from utils.project_identifier import identify_project
from config import OUTPUT_COLUMNS, MAINTENANCE_FEE_PERCENTAGE


logger = logging.getLogger(__name__)


class DataTransformer:
    """Transforms unit data from source to target format"""
    
    def __init__(self):
        """Initialize DataTransformer"""
        pass
    
    def transform_units(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform units from source format to standard target format.
        
        Args:
            df: DataFrame with source data (New Availability format)
        
        Returns:
            DataFrame in target format (Current Inventory standard)
        """
        if df.empty:
            logger.warning("Empty DataFrame provided for transformation")
            return pd.DataFrame(columns=OUTPUT_COLUMNS)
        
        logger.info(f"Transforming {len(df)} units to standard format")
        
        # Create output DataFrame
        output_data = []
        
        for idx, row in df.iterrows():
            try:
                transformed_row = self._transform_single_unit(row)
                if transformed_row:
                    output_data.append(transformed_row)
            except Exception as e:
                logger.error(f"Error transforming row {idx}: {e}")
                continue
        
        if not output_data:
            logger.warning("No units were successfully transformed")
            return pd.DataFrame(columns=OUTPUT_COLUMNS)
        
        # Create DataFrame with output columns in correct order
        result_df = pd.DataFrame(output_data, columns=OUTPUT_COLUMNS)
        
        logger.info(f"Successfully transformed {len(result_df)} units")
        return result_df
    
    def _transform_single_unit(self, row: pd.Series) -> Optional[Dict]:
        """
        Transform a single unit row.
        
        Args:
            row: Series containing source data
        
        Returns:
            Dictionary with transformed data or None if transformation fails
        """
        # Extract source values with column name variations
        unit_code = row.get('UNIT CODE') or row.get('UNIT CODES') or row.get('UNIT_CODE') or row.get('Unit Code') or row.get('Unit code') or ''
        unit_type = row.get('UNIT TYPE') or row.get('UNIT_TYPE') or row.get('Unit Type') or ''
        floor_value = row.get('FLOOR') or row.get('Floor') or ''
        gross_bua = row.get('GROSS BUA') or row.get('GROSS AREA') or row.get('GROSS_BUA') or row.get('BUA') or row.get('Gross BUA') or 0
        # Prioritize Final Price (for Valleys), then TOTAL PRICE (for Park Central and SLW)
        total_price = row.get('Final Price') or row.get('FINAL PRICE') or row.get('TOTAL PRICE') or row.get('Price') or row.get('PRICE') or row.get('UNIT PRICE') or row.get('TOTAL PRICE - 7 Years') or row.get('TOTAL PRICE - 10 Years') or 0
        num_bedrooms = row.get('NUMBER OF BEDROOMS') or row.get('Number of Bedrooms') or ''
        
        # Validate required fields
        if not unit_code or pd.isna(unit_code):
            logger.warning("Missing UNIT CODE, skipping row")
            return None
        
        # Identify project
        project = identify_project(str(unit_code))
        
        # Transform fields
        default_code = str(unit_code).strip()
        unit_area = clean_numeric_value(gross_bua) or 0
        finishing = determine_finishing(project, default_code)
        floor = convert_floor(floor_value)
        list_price = clean_numeric_value(total_price) or 0
        unit_npv = list_price  # Same as list_price
        maintenance_fee = calculate_maintenance_fee(list_price, MAINTENANCE_FEE_PERCENTAGE)
        
        # Try to get bedroom count from dedicated column first, then from unit type, then from mapping
        number_of_rooms = 0
        if num_bedrooms:
            number_of_rooms = extract_bedroom_count(str(num_bedrooms), project)
        if number_of_rooms == 0:  # If not found in dedicated column, try unit type
            number_of_rooms = extract_bedroom_count(str(unit_type), project)
        
        # Generate name using the extracted bedroom count
        name = generate_unit_name(str(unit_type), default_code, number_of_rooms)
        
        # Extract unit type (Apartment, Penthouse, Duplex, etc.)
        unit_type_extracted = ''
        if unit_type:
            # Split by hyphen or space and get first part
            parts = str(unit_type).split('-')
            if parts:
                unit_type_extracted = parts[0].strip().title()  # Convert to title case
        
        # Create output dictionary
        transformed = {
            'default_code': default_code,
            'unit_area': unit_area,
            'finishing': finishing,
            'floor': floor,
            'list_price': list_price,
            'unit_npv': unit_npv,
            'name': name,
            'number_of_rooms': number_of_rooms,
            'project': project,
            'maintenance_fee': maintenance_fee,
            'unit_type': unit_type_extracted,
            'state': 'available',  # New units are always available
        }
        
        return transformed
    
    def transform_by_project(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Transform units and group by project.
        
        Args:
            df: DataFrame with source data
        
        Returns:
            Dictionary of {project_short_name: transformed_df}
        """
        if df.empty:
            return {}
        
        # First transform all units
        transformed_df = self.transform_units(df)
        
        if transformed_df.empty:
            return {}
        
        # Group by project
        grouped = {}
        for project_name in transformed_df['project'].unique():
            project_df = transformed_df[transformed_df['project'] == project_name].copy()
            
            # Determine short name for output file (case-insensitive check)
            project_name_lower = project_name.lower()
            if 'park' in project_name_lower and 'central' in project_name_lower:
                short_name = 'Park_Central'
            elif 'valleys' in project_name_lower:
                short_name = 'The_Valleys'
            elif 'slw' in project_name_lower or 'swanlake' in project_name_lower:
                short_name = 'SLW'
            else:
                short_name = 'Unknown'
            
            grouped[short_name] = project_df
            logger.info(f"Grouped {len(project_df)} units for project: {short_name}")
        
        return grouped
    
    def validate_transformed_data(self, df: pd.DataFrame) -> bool:
        """
        Validate transformed data for completeness.
        
        Args:
            df: Transformed DataFrame
        
        Returns:
            True if validation passes, False otherwise
        """
        if df.empty:
            logger.error("Validation failed: Empty DataFrame")
            return False
        
        # Check for required columns
        missing_cols = [col for col in OUTPUT_COLUMNS if col not in df.columns]
        if missing_cols:
            logger.error(f"Validation failed: Missing columns: {missing_cols}")
            return False
        
        # Check for missing critical values
        critical_columns = ['default_code', 'project', 'list_price']
        for col in critical_columns:
            null_count = df[col].isna().sum()
            if null_count > 0:
                logger.warning(f"Validation warning: {null_count} null values in {col}")
        
        logger.info("Validation passed")
        return True
