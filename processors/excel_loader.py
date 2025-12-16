"""
Excel Loader Module
Handles loading and parsing of Excel files
"""

import pandas as pd
import logging
from typing import Dict, List, Optional
from pathlib import Path
import openpyxl


logger = logging.getLogger(__name__)


class ExcelLoader:
    """Handles loading Excel files for Hassan Allam inventory processing"""
    
    def __init__(self, new_availability_path: str, current_inventory_path: str):
        """
        Initialize ExcelLoader with file paths.
        
        Args:
            new_availability_path: Path to New Availability Excel file
            current_inventory_path: Path to Current Inventory Excel file
        """
        self.new_availability_path = Path(new_availability_path)
        self.current_inventory_path = Path(current_inventory_path)
        
        # Validate files exist
        if not self.new_availability_path.exists():
            raise FileNotFoundError(f"New Availability file not found: {new_availability_path}")
        if not self.current_inventory_path.exists():
            raise FileNotFoundError(f"Current Inventory file not found: {current_inventory_path}")
    
    def get_sheet_names(self, file_path: Path) -> List[str]:
        """
        Get all sheet names from an Excel file.
        
        Args:
            file_path: Path to Excel file
        
        Returns:
            List of sheet names
        """
        try:
            workbook = openpyxl.load_workbook(file_path, read_only=True)
            sheet_names = workbook.sheetnames
            workbook.close()
            return sheet_names
        except Exception as e:
            logger.error(f"Error reading sheet names from {file_path}: {e}")
            return []
    
    def _find_header_row(self, df_raw: pd.DataFrame) -> int:
        """
        Find the row containing column headers by looking for 'UNIT' keyword.
        
        Args:
            df_raw: Raw DataFrame loaded without header
        
        Returns:
            Index of header row
        """
        for idx, row in df_raw.iterrows():
            row_str = ' '.join([str(val).upper() for val in row if pd.notna(val)])
            if 'UNIT' in row_str and ('CODE' in row_str or 'TYPE' in row_str):
                return int(idx)
        return 0  # Default to first row
    
    def load_new_availability(self, sheet_name: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """
        Load New Availability Excel file.
        
        Args:
            sheet_name: Specific sheet to load, or None to load all sheets
        
        Returns:
            Dictionary of {sheet_name: DataFrame}
        """
        logger.info(f"Loading New Availability from: {self.new_availability_path}")
        
        try:
            if sheet_name:
                # First load to find header row
                df_raw = pd.read_excel(self.new_availability_path, sheet_name=sheet_name, header=None, nrows=20)
                header_row = self._find_header_row(df_raw)
                
                # Load again with correct header
                df = pd.read_excel(self.new_availability_path, sheet_name=sheet_name, header=header_row)
                # Drop rows with all NaN values
                df = df.dropna(how='all')
                # Clean column names and drop columns with NaN names
                df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
                df = df.loc[:, df.columns.notna()]  # Remove columns with NaN names
                logger.info(f"Loaded sheet '{sheet_name}' with {len(df)} rows (header at row {header_row})")
                return {sheet_name: df}
            else:
                # Load all sheets
                all_sheets = {}
                sheet_names = self.get_sheet_names(self.new_availability_path)
                for name in sheet_names:
                    try:
                        df_raw = pd.read_excel(self.new_availability_path, sheet_name=name, header=None, nrows=20)
                        header_row = self._find_header_row(df_raw)
                        
                        df = pd.read_excel(self.new_availability_path, sheet_name=name, header=header_row)
                        df = df.dropna(how='all')
                        df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
                        df = df.loc[:, df.columns.notna()]  # Remove columns with NaN names
                        all_sheets[name] = df
                        logger.info(f"Loaded sheet '{name}' with {len(df)} rows")
                    except Exception as e:
                        logger.warning(f"Could not load sheet '{name}': {e}")
                        continue
                return all_sheets
        
        except Exception as e:
            logger.error(f"Error loading New Availability: {e}")
            raise
    
    def load_current_inventory(self) -> pd.DataFrame:
        """
        Load Current Inventory Excel file.
        
        Returns:
            DataFrame containing current inventory
        """
        logger.info(f"Loading Current Inventory from: {self.current_inventory_path}")
        
        try:
            # Try to load first sheet
            df = pd.read_excel(self.current_inventory_path)
            logger.info(f"Loaded current inventory with {len(df)} rows")
            return df
        
        except Exception as e:
            logger.error(f"Error loading Current Inventory: {e}")
            raise
    
    def get_existing_unit_codes(self) -> List[str]:
        """
        Get list of existing unit codes from current inventory.
        
        Returns:
            List of unit codes (default_code column)
        """
        try:
            df = self.load_current_inventory()
            
            # Look for unit code column (could be 'default_code', 'UNIT CODE', etc.)
            unit_code_column = None
            for col in df.columns:
                if col.lower() in ['default_code', 'unit code', 'unit_code', 'code']:
                    unit_code_column = col
                    break
            
            if unit_code_column is None:
                logger.warning("Could not find unit code column in current inventory")
                return []
            
            # Get unique unit codes, excluding NaN values
            unit_codes = df[unit_code_column].dropna().unique().tolist()
            logger.info(f"Found {len(unit_codes)} existing unit codes")
            
            return unit_codes
        
        except Exception as e:
            logger.error(f"Error extracting unit codes: {e}")
            return []
    
    def filter_project_sheets(self, project_type: str) -> List[str]:
        """
        Get sheet names for a specific project type.
        
        Args:
            project_type: 'Park Central', 'The Valleys', or 'SLW'
        
        Returns:
            List of matching sheet names
        """
        all_sheets = self.get_sheet_names(self.new_availability_path)
        matching_sheets = []
        
        for sheet in all_sheets:
            sheet_upper = sheet.upper()
            
            if project_type == 'Park Central':
                if 'PARK' in sheet_upper and 'CENTRAL' in sheet_upper:
                    matching_sheets.append(sheet)
            
            elif project_type == 'The Valleys':
                if 'VALLE' in sheet_upper:
                    matching_sheets.append(sheet)
            
            elif project_type == 'SLW':
                if 'SLW' in sheet_upper:
                    matching_sheets.append(sheet)
        
        logger.info(f"Found {len(matching_sheets)} sheets for {project_type}: {matching_sheets}")
        return matching_sheets
