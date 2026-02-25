# E-Commerce Sales Dashboard

An interactive Streamlit dashboard for e-commerce sales analysis, built on a
modular Python backend.

## Project Structure

```
02.wed-jupyter/
├── ecommerce_data/             # Source CSV files
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── products_dataset.csv
│   ├── customers_dataset.csv
│   ├── order_reviews_dataset.csv
│   └── order_payments_dataset.csv
├── data_loader.py              # Data ingestion, preprocessing, and joins
├── business_metrics.py         # Pure metric functions (year/month parameterized)
├── app.py                      # Streamlit dashboard
├── EDA_Refactored.ipynb        # Structured exploratory analysis notebook
├── requirements.txt            # Python dependencies
└── README.md
```

## Architecture

| Module | Responsibility |
|---|---|
| `data_loader.py` | Reads CSVs, normalizes dates, joins all tables into a flat sales DataFrame |
| `business_metrics.py` | Stateless metric functions; all accept `year` and optional `month` parameters |
| `app.py` | Streamlit UI; calls only `business_metrics` functions, contains no cleaning logic |
| `EDA_Refactored.ipynb` | Analysis notebook; imports from both modules |

## Setup

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Run the dashboard**

From the `02.wed-jupyter/` directory:

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

**3. Run the notebook**

```bash
jupyter notebook EDA_Refactored.ipynb
```

## Dashboard Features

- **Year selector** in the header; all charts and KPIs update instantly.
- **KPI cards**: Total Revenue, Avg Monthly Growth Rate, Average Order Value,
  Total Orders — each with a year-over-year delta indicator.
- **Revenue trend chart**: current year (solid line) vs prior year (dashed line).
- **Top 10 categories chart**: horizontal bar chart with blue gradient coloring.
- **Geographic map**: US state-level revenue choropleth (blue scale).
- **Delivery experience chart**: avg review score by delivery time bucket.
- **Summary cards**: avg delivery time and avg review score with prior-year delta.

## Configuration

To analyze a different data directory, pass `data_dir` to `load_sales_data`:

```python
from data_loader import load_sales_data
sales = load_sales_data(data_dir="/path/to/your/data")
```

All metric functions accept `year` and optional `month` parameters, making
the framework portable to any time period present in the data.
