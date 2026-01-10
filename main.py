"""
Hassan Allam Inventory Update Automation - Main Script
Automatically processes multi-project Excel inventory, identifies new units,
and generates reformatted output files per project.

Usage:
    python main.py
"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

from config import (
    NEW_AVAILABILITY_FILE,
    CURRENT_INVENTORY_FILE,
    OUTPUT_DIRECTORY,
    LOG_DIRECTORY
)
from processors.excel_loader import ExcelLoader
from processors.unit_comparator import UnitComparator
from processors.data_transformer import DataTransformer


def setup_logging():
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    Path(LOG_DIRECTORY).mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = Path(LOG_DIRECTORY) / f'processing_{timestamp}.log'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def save_output_files(project_dataframes: Dict[str, pd.DataFrame], output_dir: Path) -> Dict[str, str]:
    """
    Save transformed data to Excel files by project.
    
    Args:
        project_dataframes: Dictionary of {project_name: dataframe}
        output_dir: Output directory path
    
    Returns:
        Dictionary of {project_name: output_file_path}
    """
    output_files = {}
    
    for project_name, df in project_dataframes.items():
        if df.empty:
            logging.warning(f"No data to save for {project_name}")
            continue
        
        # Create output filename
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"{project_name}_New_Units_{timestamp}.xlsx"
        filepath = output_dir / filename
        
        # Save to Excel
        try:
            df.to_excel(filepath, index=False, sheet_name='New Units')
            output_files[project_name] = str(filepath)
            logging.info(f"Saved {len(df)} units to {filepath}")
        except Exception as e:
            logging.error(f"Error saving {project_name}: {e}")
    
    return output_files


def create_summary_report(
    all_new_units: Dict[str, pd.DataFrame],
    output_files: Dict[str, str],
    output_dir: Path,
    updated_inventory_path: str = None,
    availability_stats: dict = None
):
    """
    Create a summary report of the processing.
    
    Args:
        all_new_units: Dictionary of new units by project
        output_files: Dictionary of output file paths
        output_dir: Output directory
        updated_inventory_path: Path to updated inventory file
        availability_stats: Statistics on availability changes
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    summary_file = output_dir / f'processing_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    
    with open(summary_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("Hassan Allam Inventory Update - Processing Summary\n")
        f.write("=" * 80 + "\n")
        f.write(f"Processed at: {timestamp}\n\n")
        
        # Updated Inventory Section
        if updated_inventory_path:
            f.write("Updated Current Inventory:\n")
            f.write("-" * 80 + "\n")
            f.write(f"  File: {updated_inventory_path}\n")
            if availability_stats:
                f.write(f"  Available units: {availability_stats.get('available', 0)}\n")
                f.write(f"  Unavailable units: {availability_stats.get('unavailable', 0)}\n")
                f.write(f"  Total units: {availability_stats.get('available', 0) + availability_stats.get('unavailable', 0)}\n")
            f.write("\n")
        
        f.write("New Units by Project:\n")
        f.write("-" * 80 + "\n")
        
        total_new_units = 0
        for project_name, df in all_new_units.items():
            count = len(df)
            total_new_units += count
            f.write(f"  {project_name}: {count} new units\n")
        
        f.write(f"\nTotal New Units: {total_new_units}\n\n")
        
        f.write("Output Files Generated (New Units):\n")
        f.write("-" * 80 + "\n")
        for project_name, filepath in output_files.items():
            f.write(f"  {project_name}: {filepath}\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    logging.info(f"Summary report saved to {summary_file}")
    print(f"\n>> Summary report: {summary_file}")


def main():
    """Main execution function"""
    logger = setup_logging()
    logger.info("=" * 80)
    logger.info("Starting Hassan Allam Inventory Update Automation")
    logger.info("=" * 80)
    
    try:
        # Create output directory
        output_dir = Path(OUTPUT_DIRECTORY)
        output_dir.mkdir(exist_ok=True)
        
        # Step 1: Initialize Excel Loader
        print("\n[1/5] Loading Excel files...")
        logger.info("Initializing Excel Loader")
        loader = ExcelLoader(NEW_AVAILABILITY_FILE, CURRENT_INVENTORY_FILE)
        
        # Step 2: Get existing unit codes and load current inventory
        print("[2/6] Extracting existing unit codes from current inventory...")
        logger.info("Extracting existing unit codes")
        existing_codes = loader.get_existing_unit_codes()
        print(f"  >> Found {len(existing_codes)} existing units")
        
        # Load full current inventory for state tracking
        logger.info("Loading current inventory for state update")
        current_inventory_df = loader.load_current_inventory()
        
        # Step 3: Initialize comparator
        print("[3/6] Initializing unit comparator...")
        comparator = UnitComparator(existing_codes)
        
        # Step 4: Process each project
        print("[4/6] Processing projects and identifying new units...")
        logger.info("Processing projects")
        
        projects = ['Park Central', 'The Valleys', 'SLW']
        all_new_units = {}
        all_new_availability_dfs = []  # Collect all new availability data for state tracking
        
        for project in projects:
            print(f"\n  Processing: {project}")
            logger.info(f"Processing project: {project}")
            
            # Get sheets for this project
            sheets = loader.filter_project_sheets(project)
            
            if not sheets:
                logger.warning(f"No sheets found for {project}")
                print(f"    [!] No sheets found")
                continue
            
            print(f"    Found {len(sheets)} sheet(s): {', '.join(sheets)}")
            
            # Combine all sheets for this project
            project_dfs = []
            for sheet in sheets:
                sheet_data = loader.load_new_availability(sheet)
                if sheet in sheet_data:
                    df = sheet_data[sheet]
                    if not df.empty:
                        project_dfs.append(df)
                        all_new_availability_dfs.append(df)  # Collect for state tracking
            
            if not project_dfs:
                logger.warning(f"No data found for {project}")
                print(f"    [!] No data available")
                continue
            
            # Combine all data for this project
            combined_df = pd.concat(project_dfs, ignore_index=True)
            print(f"    Total units: {len(combined_df)}")
            
            # Find new units
            new_units_df = comparator.find_new_units(combined_df)
            print(f"    New units: {len(new_units_df)}")
            
            if not new_units_df.empty:
                # Transform to standard format
                transformer = DataTransformer()
                transformed_by_project = transformer.transform_by_project(new_units_df)
                
                # Add to results
                all_new_units.update(transformed_by_project)
                
                for proj_name, proj_df in transformed_by_project.items():
                    print(f"    >> Transformed {len(proj_df)} units for {proj_name}")
        
        # Step 5: Generate updated current inventory with state column
        print("\n[5/6] Generating updated inventory with availability states...")
        logger.info("Generating updated current inventory")
        
        updated_inventory_path = None
        availability_stats = {}
        
        if all_new_availability_dfs:
            # Combine all new availability data
            combined_new_availability = pd.concat(all_new_availability_dfs, ignore_index=True)
            
            # Generate updated inventory with state
            updated_inventory = comparator.generate_updated_inventory(
                current_inventory_df,
                combined_new_availability
            )
            
            # Save updated inventory
            timestamp = datetime.now().strftime('%Y%m%d')
            updated_inv_filename = f"Current_Inventory_Updated_{timestamp}.xlsx"
            updated_inv_filepath = output_dir / updated_inv_filename
            
            updated_inventory.to_excel(updated_inv_filepath, index=False, sheet_name='Updated Inventory')
            updated_inventory_path = str(updated_inv_filepath)
            logger.info(f"Saved updated inventory to {updated_inv_filepath}")
            print(f"  >> Updated inventory saved: {updated_inv_filename}")
            
            # Calculate statistics
            available_count = (updated_inventory['state'] == 'available').sum()
            unavailable_count = (updated_inventory['state'] == 'unavailable').sum()
            availability_stats = {
                'available': available_count,
                'unavailable': unavailable_count
            }
            print(f"     - Available: {available_count} units")
            print(f"     - Unavailable: {unavailable_count} units")
        else:
            logger.warning("No new availability data to compare against")
            print("  [!] No new availability data found")
        
        # Step 6: Save output files
        print("\n[6/6] Saving new units output files...")
        logger.info("Saving new units output files")
        
        if not all_new_units:
            print("\n[!] No new units found. No output files generated.")
            logger.info("No new units found")
        else:
            output_files = save_output_files(all_new_units, output_dir)
            
            print(f"\n{'='*80}")
            print("Processing Complete!")
            print(f"{'='*80}")
            
            total_units = sum(len(df) for df in all_new_units.values())
            print(f"\nTotal new units processed: {total_units}")
            print(f"\nOutput files generated ({len(output_files)}):")
            for project_name, filepath in output_files.items():
                unit_count = len(all_new_units[project_name])
                print(f"  - {project_name}: {unit_count} units -> {filepath}")
            
            # Create summary report
            create_summary_report(all_new_units, output_files, output_dir, updated_inventory_path, availability_stats)
        
        logger.info("Processing completed successfully")
        print(f"\n[SUCCESS] All done! Check the '{OUTPUT_DIRECTORY}' directory for output files.")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\n[ERROR] File not found: {e}")
        print("Please ensure both Excel files are in the current directory:")
        print(f"  - {NEW_AVAILABILITY_FILE}")
        print(f"  - {CURRENT_INVENTORY_FILE}")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n[ERROR] Error occurred: {e}")
        print(f"Check log file in '{LOG_DIRECTORY}' directory for details.")


if __name__ == "__main__":
    main()
