"""
Pytest configuration and shared fixtures
"""
import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_unit_data():
    """Sample unit data for testing"""
    return {
        'UNIT CODE': 'PC1-A3-01-SA-24',
        'UNIT TYPE': 'APARTMENT-Three Bedrooms',
        'FLOOR': 'SECOND',
        'GROSS BUA': 120,
        'TOTAL PRICE': 1000000,
        'NUMBER OF BEDROOMS': 3
    }


@pytest.fixture
def sample_valleys_data():
    """Sample Valleys unit data"""
    return {
        'UNIT CODE': 'VAL-V3-206-SV-G',
        'UNIT TYPE': 'Standalone Villa G',
        'FLOOR': '',
        'GROSS BUA': 300,
        'Final Price': 5000000
    }


@pytest.fixture
def sample_slw_data():
    """Sample SLW unit data"""
    return {
        'Unit Code': 'SLW-8011-B2-11',
        'UNIT TYPE': 'APARTMENT',
        'FLOOR': 'SECOND',
        'GROSS BUA': 120,
        'TOTAL PRICE - 7 Years': 1500000
    }

