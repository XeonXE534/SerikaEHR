from rich.console import Console
import logging
from pathlib import Path

from sqlalchemy.testing.plugin.plugin_base import engines

from .extract import extract_all_bundles
from .transform import extract_patients
from .load import create_db, load_patients

console = Console()

# SerikaEHR-BACKEND v1

def setup_logging():
    """Logging"""
    log_dir = Path("src/serika/logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=log_dir / "serika.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def run():
    """Main entry point for ETL process"""
    console.print("""\n[blue]
███████╗███████╗██████╗ ██╗██╗  ██╗ █████╗       ███████╗██╗  ██╗██████╗ 
██╔════╝██╔════╝██╔══██╗██║██║ ██╔╝██╔══██╗      ██╔════╝██║  ██║██╔══██╗
███████╗█████╗  ██████╔╝██║█████╔╝ ███████║█████╗█████╗  ███████║██████╔╝
╚════██║██╔══╝  ██╔══██╗██║██╔═██╗ ██╔══██║╚════╝██╔══╝  ██╔══██║██╔══██╗
███████║███████╗██║  ██║██║██║  ██╗██║  ██║      ███████╗██║  ██║██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝      ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
[/blue]\n""")
    setup_logging()

    try:
        console.print("[blue]>>> EXTRACTING DATA...[/blue]")
        bundles = extract_all_bundles('data/raw/data_raw')
        logging.info(f"Extracted {len(bundles)} FHIR bundles :3")

        console.print("[blue]>>> TRANSFORMING DATA...[/blue]")
        patients_df = extract_patients(bundles)
        logging.info(f"Transformed data into {len(patients_df)} patient records :3")

        console.print("[blue]>>> LOADING DATA...[/blue]")
        engine = create_db()
        load_patients(patients_df, engine)
        logging.info("Loaded patient data into database :3")

        console.print("[green]ETL PROCESS COMPLETED SUCCESSFULLY! :D[/green]")
        console.print(f"[dim]Database: data/processed/serika.db[/dim]")

    except Exception as e:
        console.print(f"[red]ETL PROCESS FAILED: {e} :([/red]")
        logging.error(f"ETL process failed: {e} :(", exc_info=True)

if __name__ == "__main__":
    run()