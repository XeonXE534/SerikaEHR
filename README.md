![SerikaEHR Logo](serika.png)
## v0.0.1--Alpha

**SerikaEHR** is a lightweight, modular ETL pipeline built for handling and cleaning FHIR-formatted EHR data.

---

## Features

- **Extracts** and parses large FHIR bundles (JSON)  
- **Transforms** deeply nested data into clean tabular formats (patients, encounters, claims, etc.)  
- **Loads** data into SQL databases (SQLite or Postgres) via SQLAlchemy  
- **Logs** every step of the process with rich, colorized output  
- **Configurable and modular** — easy to extend for new resource types or data sources  

---

## Setup

### Prerequisites
- Python 3.10+

### Install dependencies
```bash
uv pip install pandas sqlalchemy pyyaml rich
```

### Run the pipeline

```bash
python src/main.py
```

---

## How It Works

1. **Extract** – Reads FHIR JSON bundles from `/data/raw`
2. **Transform** – Flattens the nested resources (Patient, Encounter, Condition, Claim, etc.)
3. **Load** – Inserts the cleaned data into a SQL database (default: SQLite)
4. **Log** – Writes all operations to `/logs/etl.log` with timestamps and error reports

---

## Future Plans

* Support for HL7v2 or openEHR formats
* Parquet/Arrow support for faster storage
* Prefect/Airflow integration
* Optional REST API for querying data
* CLI flags for selective pipeline execution

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## Notes
Feel free to use, modify, and distribute as you see fit. Just don’t blame me if your EHR data goes haywire :3
Built using Python, pandas, SQLAlchemy, and Rich