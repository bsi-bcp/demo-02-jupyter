"""
Data loading and preprocessing module for e-commerce analytics.

Handles CSV ingestion, missing value treatment, date normalization,
and multi-table join logic to produce a flat, analysis-ready DataFrame.
"""

import os
from typing import Dict, Optional

import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ecommerce_data")

_DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def load_raw_data(data_dir: str = DATA_DIR) -> Dict[str, pd.DataFrame]:
    """
    Load all six CSV datasets from the specified directory.

    Parameters
    ----------
    data_dir : str
        Path to the folder containing the CSV files.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary with keys: orders, order_items, products,
        customers, reviews, payments.
    """
    return {
        "orders": pd.read_csv(os.path.join(data_dir, "orders_dataset.csv")),
        "order_items": pd.read_csv(
            os.path.join(data_dir, "order_items_dataset.csv")
        ),
        "products": pd.read_csv(os.path.join(data_dir, "products_dataset.csv")),
        "customers": pd.read_csv(
            os.path.join(data_dir, "customers_dataset.csv")
        ),
        "reviews": pd.read_csv(
            os.path.join(data_dir, "order_reviews_dataset.csv")
        ),
        "payments": pd.read_csv(
            os.path.join(data_dir, "order_payments_dataset.csv")
        ),
    }


def preprocess_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all timestamp columns to datetime and derive year/month columns.

    Parameters
    ----------
    orders : pd.DataFrame
        Raw orders DataFrame.

    Returns
    -------
    pd.DataFrame
        Orders DataFrame with parsed dates, year, and month columns.
    """
    df = orders.copy()
    for col in _DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    df["year"] = df["order_purchase_timestamp"].dt.year
    df["month"] = df["order_purchase_timestamp"].dt.month
    return df


def build_sales_data(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    reviews: pd.DataFrame,
) -> pd.DataFrame:
    """
    Construct a denormalized sales DataFrame by joining all relevant tables.

    Only rows with order_status == 'delivered' are retained.
    Delivery time in days, product category, customer state, and review
    score are appended to each order-item row.

    Parameters
    ----------
    orders : pd.DataFrame
        Preprocessed orders (output of preprocess_orders).
    order_items : pd.DataFrame
        Raw order_items DataFrame.
    customers : pd.DataFrame
        Raw customers DataFrame.
    products : pd.DataFrame
        Raw products DataFrame.
    reviews : pd.DataFrame
        Raw reviews DataFrame.

    Returns
    -------
    pd.DataFrame
        Flat sales DataFrame ready for metric computation.
    """
    # Join order items with orders
    sales = order_items[
        ["order_id", "order_item_id", "product_id", "price", "freight_value"]
    ].merge(
        orders[
            [
                "order_id",
                "customer_id",
                "order_status",
                "order_purchase_timestamp",
                "order_delivered_customer_date",
                "year",
                "month",
            ]
        ],
        on="order_id",
    )

    # Retain only delivered orders
    sales = sales[sales["order_status"] == "delivered"].copy()

    # Delivery time in calendar days; negative values indicate data anomalies
    sales["delivery_days"] = (
        sales["order_delivered_customer_date"]
        - sales["order_purchase_timestamp"]
    ).dt.days
    sales = sales[sales["delivery_days"] >= 0]

    # Attach product category
    sales = sales.merge(
        products[["product_id", "product_category_name"]],
        on="product_id",
        how="left",
    )

    # Attach customer state
    sales = sales.merge(
        customers[["customer_id", "customer_state"]],
        on="customer_id",
        how="left",
    )

    # Attach review score (one review per order)
    sales = sales.merge(
        reviews[["order_id", "review_score"]].drop_duplicates("order_id"),
        on="order_id",
        how="left",
    )

    return sales.reset_index(drop=True)


def load_sales_data(data_dir: str = DATA_DIR) -> pd.DataFrame:
    """
    Convenience wrapper: load raw data and return the fully joined sales DataFrame.

    Parameters
    ----------
    data_dir : str
        Path to the folder containing the CSV files.

    Returns
    -------
    pd.DataFrame
        Flat, analysis-ready sales DataFrame.
    """
    raw = load_raw_data(data_dir)
    orders = preprocess_orders(raw["orders"])
    return build_sales_data(
        orders,
        raw["order_items"],
        raw["customers"],
        raw["products"],
        raw["reviews"],
    )
