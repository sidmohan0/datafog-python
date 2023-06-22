import pytest
from datafog import DataFog
from datafog.models import ValueMapping, Base
import pandas as pd
import os
import hashlib

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


# def test_swap():
#     # Define data
#     data = {
#         'account_number': ['1234567890', '0987654321', '1112223334'],
#         'age': [25, 30, 40],
#         'name': ['John Doe', 'Jane Doe', 'Jim Smith'],
#     }

#     # Create DataFrame
#     df = pd.DataFrame(data)

#     # Write DataFrame to CSV
#     input_path = 'files/test_contains_pii.csv'
#     df.to_csv(input_path, index=False)

#     # Create a DataFog instance
#     datafog = DataFog()

#     # Define the output path
#     output_path = 'files/'

#     # Call the swap method
#     datafog.swap(input_path, output_path)

#     # Check that the output file exists
#     output_file = os.path.join(output_path, 'synthetic_output.csv')
#     assert os.path.exists(output_file)

#     # Load the output file
#     df_output = pd.read_csv(output_file)

#     # Check that the output file has the same shape as the input file
#     assert df.shape == df_output.shape

#     # Check that the output file has the same column names as the input file
#     assert list(df.columns) == list(df_output.columns)

#     # Check that the output file does not contain any PII
#     contains_pii, _ = datafog.scan(output_file)
#     assert not contains_pii

def test_redact():
    # Create a DataFog instance
    datafog = DataFog()

    # Test redact method
    assert datafog.redact("sensitive data") == "[REDACTED]"


# def test_hash():
#     # Create a DataFog instance
#     datafog = DataFog()

#     # Test hash method
#     assert datafog.hash("sensitive data") == hashlib.sha256("sensitive data".encode('utf-8')).hexdigest()

def test_hash_known_value():
    # Create a DataFog instance
    datafog = DataFog()

    # SHA-256 hash of the empty string
    known_hash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

    # Test hash method with empty string
    assert datafog.hash('') == known_hash


def test_save():
    datafog = DataFog(db_path='sqlite:///:memory:')
    session = datafog.Session()
    datafog.save(record_id=1, field_name='test', original_value='original', new_value='synthetic')
    # Query the database manually
    result = session.query(ValueMapping).first()
    assert result is not None
    assert result.record_id == 1
    assert result.field_name == 'test'
    assert result.original_value == 'original'
    assert result.new_value == 'synthetic'
    session.close()
