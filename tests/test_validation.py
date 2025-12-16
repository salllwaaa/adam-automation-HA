"""
Unit tests for data validation
"""
import pytest
import pandas as pd
from utils.validators import (
    validate_required_columns,
    validate_unit_code,
    log_data_quality_issues
)


class TestColumnValidation:
    """Test suite for column validation"""
    
    @pytest.mark.unit
    def test_all_columns_present(self):
        """Test validation passes when all columns present"""
        df = pd.DataFrame({
            'default_code': ['PC1-01'],
            'unit_area': [100],
            'state': ['available']
        })
        
        required = ['default_code', 'unit_area', 'state']
        is_valid, missing = validate_required_columns(df, required)
        
        assert is_valid == True
        assert missing == []
        
    @pytest.mark.unit
    def test_missing_columns_detected(self):
        """Test validation fails when columns missing"""
        df = pd.DataFrame({
            'default_code': ['PC1-01'],
            'unit_area': [100]
        })
        
        required = ['default_code', 'unit_area', 'state', 'project']
        is_valid, missing = validate_required_columns(df, required)
        
        assert is_valid == False
        assert 'state' in missing
        assert 'project' in missing
        assert len(missing) == 2
        
    @pytest.mark.unit
    def test_empty_dataframe(self):
        """Test validation with empty dataframe"""
        df = pd.DataFrame()
        required = ['default_code']
        is_valid, missing = validate_required_columns(df, required)
        
        assert is_valid == False
        assert 'default_code' in missing


class TestUnitCodeValidation:
    """Test suite for unit code validation"""
    
    @pytest.mark.unit
    def test_valid_unit_codes(self):
        """Test validation of valid unit codes"""
        assert validate_unit_code('PC1-A3-01-SA-24') == True
        assert validate_unit_code('VALL-V3-206') == True
        assert validate_unit_code('SLW-8011-B2-11') == True
        assert validate_unit_code('123') == True
        
    @pytest.mark.unit
    def test_invalid_unit_codes(self):
        """Test validation rejects invalid unit codes"""
        assert validate_unit_code('') == False
        assert validate_unit_code(None) == False
        assert validate_unit_code('   ') == False
        
    @pytest.mark.unit
    def test_pandas_na(self):
        """Test validation handles pandas NA values"""
        import numpy as np
        assert validate_unit_code(np.nan) == False
        assert validate_unit_code(float('nan')) == False
        
    @pytest.mark.unit
    def test_whitespace_trimming(self):
        """Test that whitespace is handled correctly"""
        # Valid after trimming
        assert validate_unit_code('  PC1-01  ') == True
        # Only whitespace - invalid
        assert validate_unit_code('     ') == False


class TestDataQualityLogging:
    """Test suite for data quality issue logging"""
    
    @pytest.mark.unit
    def test_missing_unit_codes_logged(self, caplog):
        """Test logging of missing unit codes"""
        df = pd.DataFrame({
            'UNIT CODE': ['PC1-01', None, 'PC1-03', None],
            'TOTAL PRICE': [100, 200, 300, 400]
        })
        
        log_data_quality_issues(df, 'Test Sheet')
        
        # Check if warning was logged
        assert any('missing UNIT CODE' in record.message for record in caplog.records)
        
    @pytest.mark.unit
    def test_missing_prices_logged(self, caplog):
        """Test logging of missing prices"""
        df = pd.DataFrame({
            'UNIT CODE': ['PC1-01', 'PC1-02', 'PC1-03'],
            'TOTAL PRICE': [100, None, None]
        })
        
        log_data_quality_issues(df, 'Test Sheet')
        
        assert any('missing TOTAL PRICE' in record.message for record in caplog.records)
        
    @pytest.mark.unit
    def test_duplicate_codes_logged(self, caplog):
        """Test logging of duplicate unit codes"""
        df = pd.DataFrame({
            'UNIT CODE': ['PC1-01', 'PC1-02', 'PC1-01', 'PC1-03'],
            'TOTAL PRICE': [100, 200, 300, 400]
        })
        
        log_data_quality_issues(df, 'Test Sheet')
        
        assert any('duplicate' in record.message.lower() for record in caplog.records)

