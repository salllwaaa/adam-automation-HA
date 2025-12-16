"""
Unit tests for unit comparison and state tracking
"""
import pytest
import pandas as pd
from processors.unit_comparator import UnitComparator


class TestUnitComparator:
    """Test suite for unit comparison logic"""
    
    @pytest.fixture
    def sample_existing_codes(self):
        """Sample existing unit codes"""
        return {'PC1-01', 'PC1-02', 'PC1-03', 'VALL-01', 'VALL-02', 'SLW-01'}
    
    @pytest.mark.unit
    def test_initialization(self, sample_existing_codes):
        """Test comparator initialization"""
        comparator = UnitComparator(sample_existing_codes)
        assert len(comparator.existing_codes) == 6
        
    @pytest.mark.unit
    def test_find_new_units(self, sample_existing_codes):
        """Test identification of new units"""
        comparator = UnitComparator(sample_existing_codes)
        
        new_availability = pd.DataFrame({
            'UNIT CODE': ['PC1-01', 'PC1-04', 'PC1-05', 'VALL-01']
        })
        
        new_units = comparator.find_new_units(new_availability)
        
        # new_units is a list of dictionaries (DataFrame rows)
        assert len(new_units) == 2
        # Convert to dataframe to check codes
        new_units_df = pd.DataFrame(new_units)
        assert 'PC1-04' in new_units_df['UNIT CODE'].values
        assert 'PC1-05' in new_units_df['UNIT CODE'].values
        
    @pytest.mark.unit
    def test_no_new_units(self, sample_existing_codes):
        """Test when all units already exist"""
        comparator = UnitComparator(sample_existing_codes)
        
        new_availability = pd.DataFrame({
            'UNIT CODE': ['PC1-01', 'PC1-02', 'VALL-01']
        })
        
        new_units = comparator.find_new_units(new_availability)
        
        assert len(new_units) == 0
        
    @pytest.mark.unit
    def test_case_insensitive_comparison(self, sample_existing_codes):
        """Test that comparison is case insensitive"""
        comparator = UnitComparator(sample_existing_codes)
        
        new_availability = pd.DataFrame({
            'UNIT CODE': ['pc1-01', 'PC1-01', 'Pc1-01']  # Different cases, same unit
        })
        
        new_units = comparator.find_new_units(new_availability)
        
        assert len(new_units) == 0  # All are existing
        
    @pytest.mark.unit
    def test_whitespace_handling(self, sample_existing_codes):
        """Test that whitespace is handled correctly"""
        comparator = UnitComparator(sample_existing_codes)
        
        new_availability = pd.DataFrame({
            'UNIT CODE': ['  PC1-01  ', 'PC1-02   ', '  PC1-03']
        })
        
        new_units = comparator.find_new_units(new_availability)
        
        assert len(new_units) == 0  # All exist after trimming


class TestStateTracking:
    """Test suite for availability state tracking"""
    
    @pytest.fixture
    def sample_current_inventory(self):
        """Sample current inventory"""
        return pd.DataFrame({
            'default_code': ['PC1-01', 'PC1-02', 'PC1-03', 'VALL-01', 'VALL-02'],
            'unit_area': [100, 120, 150, 200, 220],
            'project': ['Park Central', 'Park Central', 'Park Central', 'Valleys', 'Valleys']
        })
    
    @pytest.mark.unit
    def test_all_available(self, sample_current_inventory):
        """Test when all units are available"""
        new_availability = pd.DataFrame({
            'UNIT CODE': ['PC1-01', 'PC1-02', 'PC1-03', 'VALL-01', 'VALL-02']
        })
        
        comparator = UnitComparator(set())
        updated_df = comparator.generate_updated_inventory(
            sample_current_inventory,
            new_availability
        )
        
        assert (updated_df['state'] == 'available').all()
        assert len(updated_df) == 5
        
    @pytest.mark.unit
    def test_some_unavailable(self, sample_current_inventory):
        """Test when some units become unavailable"""
        new_availability = pd.DataFrame({
            'UNIT CODE': ['PC1-01', 'PC1-03', 'VALL-02']  # PC1-02 and VALL-01 missing
        })
        
        comparator = UnitComparator(set())
        updated_df = comparator.generate_updated_inventory(
            sample_current_inventory,
            new_availability
        )
        
        # Check specific states
        pc1_01_state = updated_df[updated_df['default_code'] == 'PC1-01']['state'].values[0]
        pc1_02_state = updated_df[updated_df['default_code'] == 'PC1-02']['state'].values[0]
        vall_01_state = updated_df[updated_df['default_code'] == 'VALL-01']['state'].values[0]
        
        assert pc1_01_state == 'available'
        assert pc1_02_state == 'unavailable'
        assert vall_01_state == 'unavailable'
        
    @pytest.mark.unit
    def test_all_unavailable(self, sample_current_inventory):
        """Test when all units become unavailable"""
        new_availability = pd.DataFrame({
            'UNIT CODE': []  # Empty - no units available
        })
        
        comparator = UnitComparator(set())
        updated_df = comparator.generate_updated_inventory(
            sample_current_inventory,
            new_availability
        )
        
        assert (updated_df['state'] == 'unavailable').all()
        
    @pytest.mark.unit
    def test_state_column_added(self, sample_current_inventory):
        """Test that state column is added to inventory"""
        new_availability = pd.DataFrame({
            'UNIT CODE': ['PC1-01']
        })
        
        comparator = UnitComparator(set())
        updated_df = comparator.generate_updated_inventory(
            sample_current_inventory,
            new_availability
        )
        
        assert 'state' in updated_df.columns
        
    @pytest.mark.unit
    def test_multiple_unit_code_columns(self, sample_current_inventory):
        """Test handling of multiple unit code column variations"""
        new_availability = pd.DataFrame({
            'UNIT CODE': ['PC1-01', 'PC1-02'],
            'UNIT CODES': [None, None],
            'Unit Code': ['PC1-03', None]
        })
        
        comparator = UnitComparator(set())
        updated_df = comparator.generate_updated_inventory(
            sample_current_inventory,
            new_availability
        )
        
        # PC1-01, PC1-02, PC1-03 should be available
        available_codes = updated_df[updated_df['state'] == 'available']['default_code'].tolist()
        assert 'PC1-01' in available_codes
        assert 'PC1-02' in available_codes
        assert 'PC1-03' in available_codes

