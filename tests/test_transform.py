import pytest
from src.serika.transform import parse_patient

def test_parse_patient_complete():
    resource = {
        'resourceType': 'Patient',
        'id': 'test-123',
        'name': [{'given': ['John'], 'family': 'Doe'}],
        'gender': 'male',
        'birthDate': '1990-01-01',
    }

    result = parse_patient(resource)
    assert result['patient_id'] == 'test-123'
    assert result['given_name'] == 'John'
    assert result['family_name'] == 'Doe'

# Add more tests...