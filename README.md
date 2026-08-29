# Sales Data Analysis

A portfolio-ready sales analytics project built with **Python, Pandas, NumPy, Matplotlib, and Seaborn**.

## Project Overview

This project analyzes 1,500 synthetic retail transactions to answer practical business questions:

- How much revenue was generated?
- Which products and categories perform best?
- How does revenue change over time?
- Which sales channels and regions contribute most?
- What are the core sales KPIs?

## Tech Stack

- Python 3
- Pandas — data loading, cleaning, aggregation
- NumPy — numerical operations
- Matplotlib — visualization
- Seaborn — statistical/business charts
- Pytest — basic automated tests

## Project Structure

```text
sales-data-analysis/
├── data/
│   └── sales_data.csv
├── notebooks/
├── outputs/
│   ├── monthly_revenue.png
│   ├── sales_by_category.png
│   └── top_products.png
├── src/
│   └── analysis.py
├── tests/
│   └── test_analysis.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Getting Started

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
```

Activate it, then:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
python src/analysis.py
```

Run tests:

```bash
pytest
```

## Dataset

The dataset contains 1,500 synthetic retail transactions with:

- transaction ID
- date
- customer ID
- product
- category
- region
- channel
- quantity
- unit price
- discount
- revenue

The data is synthetic and intended for portfolio/learning purposes.

## Outputs

The analysis generates:

1. Monthly revenue trend
2. Top products by revenue
3. Revenue by category

## Notes

This repository is designed as a portfolio project. The dataset is intentionally synthetic so that no private customer information is included.
