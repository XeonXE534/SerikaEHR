import pandas as pd
from rich.console import Console

console = Console()

# Transform v1

def extract_patients(bundles: list[dict]) -> pd.DataFrame:
    """Extract Patient resources from FHIR bundles"""
    patients = []
    errors: int = 0

    for bundle_idx, bundle in enumerate(bundles):
        if 'entry' not in bundle:
            console.log(f"Bundle {bundle_idx} missing 'entry' field :(", style="yellow")
            continue

        for entry in bundle['entry']:
            resource = entry.get('resource', {})

            if resource.get('resourceType') != 'Patient':
                continue

            try:
                patient_data = parse_patient(resource)
                patients.append(patient_data)

            except Exception as e:
                errors += 1
                patient_id= resource.get('id', 'unknown')
                console.log(f"Failed to parse patient {patient_id}: {str(e)[:50]} :(", style="yellow") #!CHECK
                continue

    console.log(f"Extracted {len(patients)} patients ({errors} errors)")
    return pd.DataFrame(patients)

def parse_patient(resource: dict) -> dict:
    """Parse a single Patient resource into flat structure"""
    name = resource.get('name', [{}]) [0] if resource.get('name') else {} #!CHECK
    address = resource.get('address', [{}]) [0] if resource.get('address') else {}
    telecom = resource.get('telecom', [])

    phone = None
    for contact in telecom:
        if contact.get('system') == 'phone':
            phone = contact.get('value')
            break

    return {
        'patient_id':       resource.get('id'),
        'given_name':       ' '.join(name.get('given', [])),
        'family_name':      name.get('family'),
        'full_name':        ' '.join(filter(None, [' '.join(name.get('given', [])), name.get('family')])), #!CHECK
        'gender':           resource.get('gender'),
        'birth_date':       resource.get('birthDate'),
        'phone':            phone,
        'address_line':     ' '.join(address.get('line', [])),
        'city':             address.get('city'),
        'state':            address.get('state'),
        'postal_code' :     address.get('postalCode'),
        'country':          address.get('country'),
        'marital_status':   resource.get('maritalStatus', {}).get('text')
    }
