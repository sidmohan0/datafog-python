import pytest
from datafog import DataFog

def test_scan():
    datafog = DataFog()

    # Test case: When the csv file has columns present in predefined_header_values
    contains_pii, pii_fields = datafog.scan("files/test.csv")
    assert contains_pii == True
    assert set(pii_fields) == {"name", "age", "email_address"}

    # Test case: When the csv file does not have any column present in predefined_header_values
    # Assuming another csv file "test_no_pii.csv" with columns not in predefined_header_values
    contains_pii, pii_fields = datafog.scan("files/test_no_pii.csv")
    assert contains_pii == False
    assert pii_fields == []
