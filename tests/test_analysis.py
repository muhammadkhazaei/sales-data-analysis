import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from analysis import load_data, clean_data, build_kpis

def test_load_and_clean():
    df = clean_data(load_data())
    assert not df.empty
    assert df["transaction_id"].is_unique
    assert (df["quantity"] > 0).all()
    assert (df["unit_price"] > 0).all()

def test_kpis():
    df = clean_data(load_data())
    kpis = build_kpis(df)
    assert kpis["transactions"] == df["transaction_id"].nunique()
    assert kpis["units_sold"] == int(df["quantity"].sum())
    assert kpis["total_revenue"] > 0
    assert kpis["average_order_value"] > 0
