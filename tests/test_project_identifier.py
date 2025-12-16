"""
Unit tests for project identification
"""
import pytest
from utils.project_identifier import identify_project


class TestProjectIdentification:
    """Test suite for project identification from unit codes"""
    
    @pytest.mark.unit
    def test_park_central_identification(self):
        """Test Park Central project detection"""
        assert identify_project('PC1-A3-01-SA-24') == 'Park Central - Mostakbal City'
        assert identify_project('PC2-B5-12') == 'Park Central - Mostakbal City'
        assert identify_project('pc1-test') == 'Park Central - Mostakbal City'
        
    @pytest.mark.unit
    def test_valleys_identification(self):
        """Test The Valleys project detection"""
        assert identify_project('VALL-V3-206-SV-G') == 'VAL: The Valleys'
        assert identify_project('VAL-123') == 'VAL: The Valleys'
        assert identify_project('vall-test') == 'VAL: The Valleys'
        
    @pytest.mark.unit
    def test_slw_identification(self):
        """Test SLW project detection"""
        assert identify_project('SLW-8011-B2-11') == 'SLW: SwanLake West'
        assert identify_project('SLW-0500') == 'SLW: SwanLake West'
        assert identify_project('slw-test') == 'SLW: SwanLake West'
        
    @pytest.mark.unit
    def test_unknown_project(self):
        """Test unknown project handling"""
        assert identify_project('UNKNOWN-123') == 'Unknown'
        assert identify_project('XYZ-456') == 'Unknown'
        assert identify_project('') == 'Unknown'
        
    @pytest.mark.unit
    def test_none_and_empty_values(self):
        """Test handling of None and empty values"""
        assert identify_project(None) == 'Unknown'
        assert identify_project('') == 'Unknown'
        assert identify_project('   ') == 'Unknown'

