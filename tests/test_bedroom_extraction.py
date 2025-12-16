"""
Unit tests for bedroom count extraction
"""
import pytest
from utils.column_mapper import extract_bedroom_count, lookup_bedroom_by_unit_type


class TestBedroomExtraction:
    """Test suite for bedroom count extraction from various formats"""
    
    @pytest.mark.unit
    def test_text_pattern_extraction(self):
        """Test extraction from text patterns like 'Three Bedrooms'"""
        assert extract_bedroom_count('APARTMENT-Three Bedrooms', None) == 3
        assert extract_bedroom_count('PENTHOUSE-Two Bedrooms', None) == 2
        assert extract_bedroom_count('DUPLEX-Four Bedrooms', None) == 4
        assert extract_bedroom_count('Studio', None) == 0
        
    @pytest.mark.unit
    def test_slash_format_extraction(self):
        """Test extraction from slash format like '/ 3 Beds'"""
        assert extract_bedroom_count('Town House (M) / 3 Beds', None) == 3
        assert extract_bedroom_count('Villa / 5 Beds', None) == 5
        assert extract_bedroom_count('Standalone Villa G / 5 Beds', None) == 5
        
    @pytest.mark.unit
    def test_dash_format_extraction(self):
        """Test extraction from dash format like '- 3 BED'"""
        assert extract_bedroom_count('TOWNHOUSE (M) - 3 BED', None) == 3
        assert extract_bedroom_count('VILLA - 4 BED', None) == 4
        
    @pytest.mark.unit
    def test_simple_number_extraction(self):
        """Test extraction from simple number patterns"""
        assert extract_bedroom_count('3 bedrooms', None) == 3
        assert extract_bedroom_count('4 Bedrooms', None) == 4
        assert extract_bedroom_count('5 beds+living', None) == 5
        
    @pytest.mark.unit
    def test_exclude_additional_rooms(self):
        """Test that living room, maid, driver, nanny are excluded"""
        assert extract_bedroom_count('3+living room', None) == 3
        assert extract_bedroom_count('3+maid', None) == 3
        assert extract_bedroom_count('3+driver', None) == 3
        assert extract_bedroom_count('4+nanny', None) == 4
        assert extract_bedroom_count('3+living room+nanny+driver', None) == 3
        assert extract_bedroom_count('5 bedrooms+living', None) == 5
        
    @pytest.mark.unit
    def test_valleys_mapping_lookup(self):
        """Test bedroom lookup from Valleys mapping table"""
        project = 'VAL: The Valleys'
        assert extract_bedroom_count('Standalone Villa G', project) == 5
        assert extract_bedroom_count('Standalone Villa F', project) == 4
        assert extract_bedroom_count('Standalone Villa D', project) == 4
        assert extract_bedroom_count('Twin Villa A', project) == 4
        assert extract_bedroom_count('Twin Villa B', project) == 4
        assert extract_bedroom_count('Town House (M)', project) == 3
        assert extract_bedroom_count('Town House (C)', project) == 4
        assert extract_bedroom_count('Twin House', project) == 4
        
    @pytest.mark.unit
    def test_slw_mapping_lookup(self):
        """Test bedroom lookup from SLW mapping table"""
        project = 'SLW: SwanLake West'
        assert extract_bedroom_count('STANDALONE VILLA', project) == 4
        assert extract_bedroom_count('Standalone Loft Villa', project) == 3
        assert extract_bedroom_count('TWIN VILLA', project) == 3
        assert extract_bedroom_count('Twin Loft Villa', project) == 3
        assert extract_bedroom_count('TOWNHOUSE (M)', project) == 3
        
    @pytest.mark.unit
    def test_slw_twains_all_three_bedrooms(self):
        """Test that SLW Twains are always 3 bedrooms"""
        project = 'SLW: SwanLake West'
        assert extract_bedroom_count('Twin House', project) == 3
        assert extract_bedroom_count('Twain Villa', project) == 3
        assert extract_bedroom_count('TWAIN', project) == 3
        
    @pytest.mark.unit
    def test_empty_and_none_values(self):
        """Test handling of empty and None values"""
        assert extract_bedroom_count('', None) == 0
        assert extract_bedroom_count(None, None) == 0
        assert extract_bedroom_count('   ', None) == 0
        
    @pytest.mark.unit
    def test_no_bedroom_info(self):
        """Test when no bedroom information is available"""
        assert extract_bedroom_count('Generic Villa', None) == 0
        assert extract_bedroom_count('Unit', None) == 0


class TestBedroomLookup:
    """Test suite for bedroom lookup function"""
    
    @pytest.mark.unit
    def test_valleys_lookup(self):
        """Test Valleys unit type lookup"""
        assert lookup_bedroom_by_unit_type('Standalone Villa G', 'VAL: The Valleys') == 5
        assert lookup_bedroom_by_unit_type('STANDALONE VILLA G', 'VAL: The Valleys') == 5
        
    @pytest.mark.unit
    def test_slw_lookup(self):
        """Test SLW unit type lookup"""
        assert lookup_bedroom_by_unit_type('STANDALONE VILLA', 'SLW: SwanLake West') == 4
        assert lookup_bedroom_by_unit_type('standalone villa', 'SLW: SwanLake West') == 4
        
    @pytest.mark.unit
    def test_wrong_project_returns_zero(self):
        """Test that wrong project returns 0"""
        assert lookup_bedroom_by_unit_type('Standalone Villa G', 'Park Central') == 0

