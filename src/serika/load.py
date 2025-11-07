from sqlalchemy import create_engine, text
import pandas as pd
from rich.console import Console
from pathlib import Path

console = Console()

# Load v1

def create_db(db_path: str = "data/processed/serika.db"):
    """Create database and tables"""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}", echo=False)

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                given_name TEXT,
                family_name TEXT,
                full_name TEXT,
                gender TEXT,
                birth_date DATE,
                phone TEXT,
                address_line TEXT,
                city TEXT,
                state TEXT,
                postal_code TEXT,
                country TEXT,
                marital_status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

    console.log(f"Database created at {db_path} :)", style="green")
    return engine

def load_patients(df: pd.DataFrame, engine) -> int:
    """Load patients DataFrame into database"""
    if df.empty:
        console.log("No patient data to load :(", style="yellow")
        return 0

    try:
        df.to_sql("patients", engine, if_exists="append", index=False)
        console.log(f"Successfully loaded {len(df)} patients into database :)", style="green")
        return len(df)

    except Exception as e:
        console.log(f"Error loading patients into database: {e} :(", style="red")
        raise