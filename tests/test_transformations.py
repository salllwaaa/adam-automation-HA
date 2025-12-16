"""
Unit tests for data transformations (floor, finishing, name)
"""
import pytest
from utils.column_mapper import convert_floor, determine_finishing, generate_unit_name


class TestFloorConversion:
    """Test suite for floor text normalization"""
    
    @pytest.mark.unit
    def test_word_to_number_conversion(self):
        """Test conversion from words to ordinal numbers"""
        assert convert_floor('FIRST') == '1st'
        assert convert_floor('SECOND') == '2nd'
        assert convert_floor('THIRD') == '3rd'
        assert convert_floor('FOURTH') == '4th'
        assert convert_floor('FIFTH') == '5th'
        
    @pytest.mark.unit
    def test_ground_floor(self):
        """Test ground floor variations"""
        assert convert_floor('GROUND') == 'Ground'
        assert convert_floor('Ground') == 'Ground'
        
    @pytest.mark.unit
    def test_already_formatted(self):
        """Test already formatted floors are preserved"""
        assert convert_floor('1st') == '1st'
        assert convert_floor('2nd') == '2nd'
        assert convert_floor('3rd') == '3rd'
        assert convert_floor('10th') == '10th'
        
    @pytest.mark.unit
    def test_case_insensitivity(self):
        """Test mixed case handling"""
        assert convert_floor('Second') == '2nd'
        assert convert_floor('second') == '2nd'
        assert convert_floor('SECOND') == '2nd'
        
    @pytest.mark.unit
    def test_empty_values(self):
        """Test empty value handling"""
        assert convert_floor('') == ''
        assert convert_floor(None) == ''


class TestFinishingDetermination:
    """Test suite for finishing determination"""
    
    @pytest.mark.unit
    def test_park_central_finishing(self):
        """Test Park Central is always Fully Finished"""
        assert determine_finishing('Park Central - Mostakbal City', 'PC1-123') == 'Fully Finished'
        assert determine_finishing('Park Central', 'PC2-456') == 'Fully Finished'
        
    @pytest.mark.unit
    def test_valleys_finishing(self):
        """Test The Valleys is always Fully Finished"""
        assert determine_finishing('VAL: The Valleys', 'VALL-123') == 'Fully Finished'
        assert determine_finishing('The Valleys', 'VAL-456') == 'Fully Finished'
        
    @pytest.mark.unit
    def test_slw_villas_phase1(self):
        """Test SLW villas phase 1 (100-900)"""
        assert determine_finishing('SLW: SwanLake West', 'SLW-0100') == 'Core and shell and near delivery'
        assert determine_finishing('SLW: SwanLake West', 'SLW-0500') == 'Core and shell and near delivery'
        assert determine_finishing('SLW: SwanLake West', 'SLW-0900') == 'Core and shell and near delivery'
        
    @pytest.mark.unit
    def test_slw_monos(self):
        """Test SLW Monos (1000s)"""
        assert determine_finishing('SLW: SwanLake West', 'SLW-1000') == 'Serviced Apartments'
        assert determine_finishing('SLW: SwanLake West', 'SLW-1500') == 'Serviced Apartments'
        assert determine_finishing('SLW: SwanLake West', 'SLW-1999') == 'Serviced Apartments'
        
    @pytest.mark.unit
    def test_slw_twain(self):
        """Test SLW Twain (2000s)"""
        assert determine_finishing('SLW: SwanLake West', 'SLW-2000') == 'Fully Finished'
        assert determine_finishing('SLW: SwanLake West', 'SLW-2500') == 'Fully Finished'
        assert determine_finishing('SLW: SwanLake West', 'SLW-2999') == 'Fully Finished'
        
    @pytest.mark.unit
    def test_slw_villas_phase2(self):
        """Test SLW villas phase 2 (3000-7000)"""
        assert determine_finishing('SLW: SwanLake West', 'SLW-3000') == 'Core and shell, 4 years delivery'
        assert determine_finishing('SLW: SwanLake West', 'SLW-5000') == 'Core and shell, 4 years delivery'
        assert determine_finishing('SLW: SwanLake West', 'SLW-7000') == 'Core and shell, 4 years delivery'
        
    @pytest.mark.unit
    def test_slw_shimmers(self):
        """Test SLW Shimmers lagoon (8000+)"""
        assert determine_finishing('SLW: SwanLake West', 'SLW-8000') == 'Fully Finished'
        assert determine_finishing('SLW: SwanLake West', 'SLW-8500') == 'Fully Finished'
        assert determine_finishing('SLW: SwanLake West', 'SLW-9999') == 'Fully Finished'


class TestNameGeneration:
    """Test suite for unit name generation"""
    
    @pytest.mark.unit
    def test_name_format(self):
        """Test correct name format generation"""
        name = generate_unit_name('Apartment', 'PC1-A3-01', 3)
        assert name == '3B Apartment in Park Central - Mostakbal City by Hassan Allam'
        
        name = generate_unit_name('Villa', 'VALL-V3-206', 5)
        assert name == '5B Villa in VAL: The Valleys by Hassan Allam'
        
        name = generate_unit_name('Penthouse', 'SLW-8011', 4)
        assert name == '4B Penthouse in SLW: SwanLake West by Hassan Allam'
        
    @pytest.mark.unit
    def test_name_with_zero_bedrooms(self):
        """Test name generation with 0 bedrooms (studio)"""
        name = generate_unit_name('Apartment', 'PC1-123', 0)
        assert name == '0B Apartment in Park Central - Mostakbal City by Hassan Allam'
        
    @pytest.mark.unit
    def test_name_capitalization(self):
        """Test unit type capitalization"""
        name = generate_unit_name('apartment', 'PC1-123', 2)
        assert 'Apartment' in name
        
        name = generate_unit_name('PENTHOUSE', 'PC1-123', 3)
        assert 'Penthouse' in name
        
    @pytest.mark.unit
    def test_name_includes_all_parts(self):
        """Test name includes bedroom count, type, project, and developer"""
        name = generate_unit_name('Duplex', 'VALL-123', 4)
        assert '4B' in name
        assert 'Duplex' in name
        assert 'VAL: The Valleys' in name
        assert 'Hassan Allam' in name

