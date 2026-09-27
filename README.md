# Sales Data ETL & Analytics Pipeline

An end-to-end portfolio data engineering project that extracts transactional sales data from CSV, validates and transforms it with pandas, loads the clean dataset into SQLite, and runs SQL analytics for business reporting.

## Pipeline

```text
Raw CSV
  |
  v
Extract (pandas)
  |
  v
Validate + Clean + Transform
  |
  v
Processed CSV + SQLite
  |
  v
SQL analytics
  |
  +--> Daily revenue
  +--> Category performance
  +--> Top products
  +--> Store performance
```

## Data quality handling

- Required-column validation
- Timestamp parsing
- Numeric type coercion
- Positive quantity validation
- Non-negative price validation
- Duplicate transaction handling
- Revenue calculation
- Standardised payment methods

## Project structure

```text
sales_etl_analytics/
├── data/raw/sales_transactions.csv
├── data/processed/
├── sql/analytics.sql
├── src/pipeline.py
├── tests/test_pipeline.py
├── run_pipeline.py
└── requirements.txt
```

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python run_pipeline.py
pytest -q
```

## Extension ideas

Add PostgreSQL, Docker, scheduled orchestration with Airflow/Prefect, incremental loading, data-quality checks, and a Power BI/Metabase dashboard.

## Attribution

Inspired by the App Ideas repository's sales database project specification.
