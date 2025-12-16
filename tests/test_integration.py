"""
Integration tests for end-to-end workflows
"""
import pytest
import pandas as pd
from pathlib import Path
from processors.excel_loader import ExcelLoader
from processors.unit_comparator import UnitComparator
from processors.data_transformer import DataTransformer


class TestEndToEndWorkflow:
    """Integration tests for complete workflow"""
    
    @pytest.mark.integration
    def test_complete_transformation_pipeline(self):
        """Test complete data transformation pipeline"""
        # Sample input data
        source_data = pd.DataFrame({
            'UNIT CODE': ['PC1-A3-01-SA-24', 'PC1-A3-02-SA-25'],
            'UNIT TYPE': ['APARTMENT-Three Bedrooms', 'PENTHOUSE-Two Bedrooms'],
            'FLOOR': ['SECOND', 'FIFTH'],
            'GROSS BUA': [120, 150],
            'TOTAL PRICE': [1000000, 1500000],
            'NUMBER OF BEDROOMS': [3, 2]
        })
        
        # Transform
        transformer = DataTransformer()
        result = transformer.transform_units(source_data)
        
        # Verify output
        assert len(result) == 2
        assert all(col in result.columns for col in [
            'default_code', 'unit_area', 'finishing', 'floor',
            'list_price', 'unit_npv', 'name', 'number_of_rooms',
            'project', 'maintenance_fee', 'unit_type', 'state'
        ])
        
        # Check first unit
        first_unit = result.iloc[0]
        assert first_unit['default_code'] == 'PC1-A3-01-SA-24'
        assert first_unit['number_of_rooms'] == 3
        assert first_unit['floor'] == '2nd'
        assert first_unit['finishing'] == 'Fully Finished'
        assert first_unit['state'] == 'available'
        assert '3B' in first_unit['name']
        assert 'Hassan Allam' in first_unit['name']
        
    @pytest.mark.integration
    def test_valleys_transformation_with_mapping(self):
        """Test Valleys units use bedroom mapping"""
        source_data = pd.DataFrame({
            'UNIT CODE': ['VAL-V3-206-SV-G', 'VAL-V3-207-TV-A'],
            'UNIT TYPE': ['Standalone Villa G', 'Twin Villa A'],
            'FLOOR': ['', ''],
            'GROSS BUA': [300, 250],
            'Final Price': [5000000, 4000000]
        })
        
        transformer = DataTransformer()
        result = transformer.transform_units(source_data)
        
        # Check bedroom counts from mapping
        first_unit = result.iloc[0]
        second_unit = result.iloc[1]
        
        assert first_unit['number_of_rooms'] == 5  # Standalone Villa G
        assert second_unit['number_of_rooms'] == 4  # Twin Villa A
        assert '5B' in first_unit['name']
        assert '4B' in second_unit['name']
        
    @pytest.mark.integration
    def test_slw_transformation_with_finishing_rules(self):
        """Test SLW units apply correct finishing rules"""
        source_data = pd.DataFrame({
            'Unit Code': ['SLW-0500', 'SLW-2500', 'SLW-8500'],
            'UNIT TYPE': ['STANDALONE VILLA', 'TWIN VILLA', 'APARTMENT'],
            'GROSS BUA': [250, 200, 120],
            'TOTAL PRICE - 7 Years': [3000000, 2500000, 1500000]
        })
        
        transformer = DataTransformer()
        result = transformer.transform_units(source_data)
        
        # Check finishing based on unit code prefix
        villa_phase1 = result[result['default_code'] == 'SLW-0500'].iloc[0]
        twain = result[result['default_code'] == 'SLW-2500'].iloc[0]
        shimmers = result[result['default_code'] == 'SLW-8500'].iloc[0]
        
        assert villa_phase1['finishing'] == 'Core and shell and near delivery'
        assert twain['finishing'] == 'Fully Finished'
        assert shimmers['finishing'] == 'Fully Finished'
        
    @pytest.mark.integration
    def test_state_tracking_workflow(self):
        """Test complete state tracking workflow"""
        # Current inventory
        current_inv = pd.DataFrame({
            'default_code': ['PC1-01', 'PC1-02', 'PC1-03'],
            'unit_area': [100, 120, 150],
            'project': ['Park Central', 'Park Central', 'Park Central']
        })
        
        # New availability (PC1-02 is missing)
        new_avail = pd.DataFrame({
            'UNIT CODE': ['PC1-01', 'PC1-03', 'PC1-04']  # PC1-04 is new
        })
        
        existing_codes = set(current_inv['default_code'])
        comparator = UnitComparator(existing_codes)
        
        # Find new units
        new_units = comparator.find_new_units(new_avail)
        assert len(new_units) == 1
        new_units_df = pd.DataFrame(new_units)
        assert new_units_df.iloc[0]['UNIT CODE'] == 'PC1-04'
        
        # Generate updated inventory
        updated_inv = comparator.generate_updated_inventory(current_inv, new_avail)
        
        assert updated_inv[updated_inv['default_code'] == 'PC1-01']['state'].values[0] == 'available'
        assert updated_inv[updated_inv['default_code'] == 'PC1-02']['state'].values[0] == 'unavailable'
        assert updated_inv[updated_inv['default_code'] == 'PC1-03']['state'].values[0] == 'available'


class TestOutputFormat:
    """Test output file format compliance"""
    
    @pytest.mark.integration
    def test_output_has_all_required_columns(self):
        """Test that output has all 12 required columns"""
        expected_columns = [
            'default_code', 'unit_area', 'finishing', 'floor',
            'list_price', 'unit_npv', 'name', 'number_of_rooms',
            'project', 'maintenance_fee', 'unit_type', 'state'
        ]
        
        source_data = pd.DataFrame({
            'UNIT CODE': ['PC1-01'],
            'UNIT TYPE': ['APARTMENT-Three Bedrooms'],
            'FLOOR': ['SECOND'],
            'GROSS BUA': [120],
            'TOTAL PRICE': [1000000],
            'NUMBER OF BEDROOMS': [3]
        })
        
        transformer = DataTransformer()
        result = transformer.transform_units(source_data)
        
        assert list(result.columns) == expected_columns
        
    @pytest.mark.integration
    def test_new_units_always_available(self):
        """Test that all new units have state='available'"""
        source_data = pd.DataFrame({
            'UNIT CODE': ['PC1-01', 'PC1-02', 'PC1-03'],
            'UNIT TYPE': ['APARTMENT-Three Bedrooms'] * 3,
            'GROSS BUA': [120, 130, 140],
            'TOTAL PRICE': [1000000, 1100000, 1200000],
            'NUMBER OF BEDROOMS': [3, 3, 3]
        })
        
        transformer = DataTransformer()
        result = transformer.transform_units(source_data)
        
        assert (result['state'] == 'available').all()
        
    @pytest.mark.integration
    def test_maintenance_fee_calculation(self):
        """Test maintenance fee is 10% of list price"""
        source_data = pd.DataFrame({
            'UNIT CODE': ['PC1-01'],
            'UNIT TYPE': ['APARTMENT-Three Bedrooms'],
            'GROSS BUA': [120],
            'TOTAL PRICE': [1000000],
            'NUMBER OF BEDROOMS': [3]
        })
        
        transformer = DataTransformer()
        result = transformer.transform_units(source_data)
        
        assert result.iloc[0]['maintenance_fee'] == 100000  # 10% of 1000000


@pytest.mark.smoke
class TestSmokeTests:
    """Quick smoke tests for basic functionality"""
    
    def test_system_imports(self):
        """Test that all modules can be imported"""
        try:
            from processors.excel_loader import ExcelLoader
            from processors.unit_comparator import UnitComparator
            from processors.data_transformer import DataTransformer
            from utils.project_identifier import identify_project
            from utils.column_mapper import (
                extract_bedroom_count,
                convert_floor,
                determine_finishing,
                generate_unit_name
            )
            from utils.validators import (
                validate_required_columns,
                validate_unit_code
            )
            assert True
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
            
    def test_config_accessible(self):
        """Test that configuration is accessible"""
        try:
            from config import (
                OUTPUT_COLUMNS,
                PROJECT_PATTERNS,
                VALLEYS_UNIT_TYPE_BEDROOMS,
                SLW_UNIT_TYPE_BEDROOMS
            )
            assert len(OUTPUT_COLUMNS) == 12
            assert 'PC' in PROJECT_PATTERNS
            assert 'STANDALONE VILLA G' in [k.upper() for k in VALLEYS_UNIT_TYPE_BEDROOMS.keys()]
        except ImportError as e:
            pytest.fail(f"Config import failed: {e}")

