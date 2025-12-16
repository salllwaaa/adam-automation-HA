"""
Test runner script for Hassan Allam Inventory Automation
Run all tests and generate coverage report
"""
import sys
import pytest


def main():
    """Run the test suite"""
    print("=" * 80)
    print("HASSAN ALLAM INVENTORY AUTOMATION - TEST SUITE")
    print("=" * 80)
    print()
    
    # Run pytest with coverage
    args = [
        'tests/',
        '-v',
        '--tb=short',
        '--cov=.',
        '--cov-report=term-missing',
        '--cov-report=html',
        '-m', 'not integration or integration',  # Run all tests
    ]
    
    result = pytest.main(args)
    
    print()
    print("=" * 80)
    if result == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 80)
    print()
    print("Coverage report generated in: htmlcov/index.html")
    print()
    
    return result


if __name__ == '__main__':
    sys.exit(main())

