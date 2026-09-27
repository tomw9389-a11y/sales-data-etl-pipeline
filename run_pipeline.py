from pathlib import Path
from src.pipeline import extract, transform, load_to_sqlite, run_sqlite_analytics

root = Path(__file__).resolve().parent
raw = extract(root / "data/raw/sales_transactions.csv")
clean = transform(raw)
load_to_sqlite(clean, root / "data/sales.db")
clean.to_csv(root / "data/processed/clean_sales.csv", index=False)
for name, frame in run_sqlite_analytics(root / "data/sales.db", root / "sql/analytics.sql").items():
    print(f"\n{name}\n{frame.to_string(index=False)}")
