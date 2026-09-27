from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id", "transaction_ts", "store_id", "customer_id", "product_id",
    "product_name", "category", "quantity", "unit_price", "payment_method"
]


def extract(csv_path: Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    out = df.copy()
    out["transaction_ts"] = pd.to_datetime(out["transaction_ts"], errors="coerce")
    out["quantity"] = pd.to_numeric(out["quantity"], errors="coerce")
    out["unit_price"] = pd.to_numeric(out["unit_price"], errors="coerce")

    out = out.dropna(subset=["transaction_id", "transaction_ts", "quantity", "unit_price"])
    out = out[out["quantity"] > 0]
    out = out[out["unit_price"] >= 0]
    out = out.drop_duplicates(subset=["transaction_id"], keep="last")

    out["revenue"] = (out["quantity"] * out["unit_price"]).round(2)
    out["sale_date"] = out["transaction_ts"].dt.date.astype(str)
    out["payment_method"] = out["payment_method"].str.strip().str.lower()
    out = out.sort_values("transaction_ts").reset_index(drop=True)
    return out


def load_to_sqlite(df: pd.DataFrame, db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)


def run_sqlite_analytics(db_path: Path, sql_path: Path) -> dict[str, pd.DataFrame]:
    queries = {}
    text = sql_path.read_text(encoding="utf-8")
    sections = {}
    current = None
    buffer = []
    for line in text.splitlines():
        if line.startswith("-- QUERY:"):
            if current:
                sections[current] = "\n".join(buffer)
            current = line.split(":", 1)[1].strip()
            buffer = []
        elif current:
            buffer.append(line)
    if current:
        sections[current] = "\n".join(buffer)

    with sqlite3.connect(db_path) as conn:
        for name, query in sections.items():
            queries[name] = pd.read_sql_query(query, conn)
    return queries


def main():
    parser = argparse.ArgumentParser(description="Sales ETL + SQLite analytics pipeline")
    parser.add_argument("--input", default="data/raw/sales_transactions.csv")
    parser.add_argument("--db", default="data/sales.db")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    input_path = root / args.input
    db_path = root / args.db
    sql_path = root / "sql" / "analytics.sql"

    raw = extract(input_path)
    clean = transform(raw)
    load_to_sqlite(clean, db_path)
    clean.to_csv(root / "data" / "processed" / "clean_sales.csv", index=False)

    print(f"Extracted rows: {len(raw)}")
    print(f"Loaded rows:    {len(clean)}")
    print(f"Database:       {db_path}")
    print("\nAnalytics:")
    for name, result in run_sqlite_analytics(db_path, sql_path).items():
        print(f"\n[{name}]\n{result.to_string(index=False)}")


if __name__ == "__main__":
    main()
