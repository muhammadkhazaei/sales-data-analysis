from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sales_data.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_data(path=DATA_PATH):
    """Load and validate the sales dataset."""
    df = pd.read_csv(path, parse_dates=["date"])
    required = {
        "transaction_id","date","customer_id","product","category",
        "region","channel","quantity","unit_price","discount","revenue"
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    return df

def clean_data(df):
    """Apply basic quality checks and normalize numeric fields."""
    df = df.copy()
    df = df.drop_duplicates(subset=["transaction_id"])
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0)
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df = df.dropna(subset=["date","product","category","quantity","unit_price","revenue"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]
    return df

def build_kpis(df):
    """Return headline business KPIs."""
    return {
        "total_revenue": float(df["revenue"].sum()),
        "transactions": int(df["transaction_id"].nunique()),
        "units_sold": int(df["quantity"].sum()),
        "average_order_value": float(df["revenue"].sum() / df["transaction_id"].nunique()),
        "customers": int(df["customer_id"].nunique()),
    }

def product_performance(df):
    return (df.groupby("product", as_index=False)
              .agg(revenue=("revenue","sum"), units=("quantity","sum"), transactions=("transaction_id","nunique"))
              .sort_values("revenue", ascending=False))

def monthly_revenue(df):
    return (df.assign(month=df["date"].dt.to_period("M").astype(str))
              .groupby("month", as_index=False)["revenue"].sum())

def category_performance(df):
    return (df.groupby("category", as_index=False)
              .agg(revenue=("revenue","sum"), units=("quantity","sum"))
              .sort_values("revenue", ascending=False))

def create_charts(df):
    sns.set_theme(style="whitegrid")

    monthly = monthly_revenue(df)
    plt.figure(figsize=(10,5))
    sns.lineplot(data=monthly, x="month", y="revenue", marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR/"monthly_revenue.png", dpi=160)
    plt.close()

    products = product_performance(df).head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(data=products, x="revenue", y="product")
    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR/"top_products.png", dpi=160)
    plt.close()

    categories = category_performance(df)
    plt.figure(figsize=(9,5))
    sns.barplot(data=categories, x="category", y="revenue")
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR/"sales_by_category.png", dpi=160)
    plt.close()

def run():
    df = clean_data(load_data())
    kpis = build_kpis(df)

    print("=" * 60)
    print("SALES DATA ANALYSIS")
    print("=" * 60)
    for key, value in kpis.items():
        label = key.replace("_", " ").title()
        print(f"{label}: {value:,.2f}" if isinstance(value, float) else f"{label}: {value:,}")

    print("\nTop products:")
    print(product_performance(df).head(5).to_string(index=False))

    print("\nRevenue by category:")
    print(category_performance(df).to_string(index=False))

    create_charts(df)
    print(f"\nCharts saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    run()
