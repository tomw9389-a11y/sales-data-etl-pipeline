from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pipeline import transform


def test_transform_calculates_revenue_and_date():
    df = pd.DataFrame([
        {"transaction_id": "T1", "transaction_ts": "2026-09-20 10:00:00", "store_id": "S1",
         "customer_id": "C1", "product_id": "P1", "product_name": "Mouse", "category": "Electronics",
         "quantity": 2, "unit_price": 10.0, "payment_method": " CARD "}
    ])
    out = transform(df)
    assert out.loc[0, "revenue"] == 20.0
    assert out.loc[0, "sale_date"] == "2026-09-20"
    assert out.loc[0, "payment_method"] == "card"


def test_transform_removes_invalid_and_duplicate_rows():
    rows = []
    base = {"transaction_id": "T1", "transaction_ts": "2026-09-20 10:00:00", "store_id": "S1",
            "customer_id": "C1", "product_id": "P1", "product_name": "Mouse", "category": "Electronics",
            "quantity": 1, "unit_price": 10.0, "payment_method": "card"}
    rows.append(base)
    rows.append({**base, "transaction_id": "T1", "unit_price": 20.0})
    rows.append({**base, "transaction_id": "T2", "quantity": -1})
    out = transform(pd.DataFrame(rows))
    assert len(out) == 1
    assert out.iloc[0]["revenue"] == 20.0
