import json
from pathlib import Path
from rich.console import Console

console = Console()

# Extract v1

def load_data_fhir(file_path: Path) -> dict:
    """Load single FHIR bundle JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        #console.log(f"Successfully loaded FHIR data from {file_path} :)", style="green")
        return data

    except json.JSONDecodeError as e:
        console.log(f"Invalid JSON in file {file_path}: {e} :(", style="red")
        raise

    except Exception as e:
        console.log(f"Error loading FHIR data from {file_path}: {e} :(", style="red")
        raise

def extract_all_bundles(data_dir: str = "../../data/raw/data_raw") -> list[dict]:
    """Load all FHIR bundles from directory"""
    bundles = []
    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(f"Data directory {data_dir} does not exist :(")

    json_files = sorted(data_path.glob("*.json"))
    console.log(f"Found {len(json_files)} FHIR bundles :]", style="blue")

    for file in json_files:
        try:
            bundle = load_data_fhir(file)
            bundles.append(bundle)

        except Exception as e:
            console.log(f"Skipping file {file.name} due to error: {e} :/", style="yellow")
            continue

    console.log(f"Successfully extracted {len(bundles)} FHIR bundles :)", style="green")
    return bundles