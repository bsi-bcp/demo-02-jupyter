"""
Business metrics module for e-commerce analytics.

All public functions accept a sales DataFrame (output of
data_loader.load_sales_data) plus year and optional month parameters,
and return scalar values or DataFrames for downstream use.
No raw data loading or Pandas cleaning logic lives here.
"""

from typing import Optional

import pandas as pd


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _filter(
    sales: pd.DataFrame, year: int, month: Optional[int] = None
) -> pd.DataFrame:
    """Return rows matching the requested year and optional month."""
    mask = sales["year"] == year
    if month is not None:
        mask &= sales["month"] == month
    return sales[mask]


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def categorize_delivery_speed(days: float) -> str:
    """
    Map a delivery duration to a human-readable bucket label.

    Parameters
    ----------
    days : float
        Delivery duration in calendar days.

    Returns
    -------
    str
        One of '1-3 days', '4-7 days', or '8+ days'.
    """
    if days <= 3:
        return "1-3 days"
    if days <= 7:
        return "4-7 days"
    return "8+ days"


# ---------------------------------------------------------------------------
# Revenue metrics
# ---------------------------------------------------------------------------


def get_total_revenue(
    sales: pd.DataFrame, year: int, month: Optional[int] = None
) -> float:
    """
    Calculate total revenue for the given period.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame from data_loader.
    year : int
        Calendar year to filter on.
    month : int, optional
        Calendar month (1-12) for finer granularity.

    Returns
    -------
    float
        Sum of item prices for delivered orders.
    """
    return float(_filter(sales, year, month)["price"].sum())


def get_monthly_revenue(sales: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Aggregate revenue by month for the given year.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame.
    year : int
        Calendar year to filter on.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['month', 'revenue'].
    """
    result = (
        _filter(sales, year)
        .groupby("month")["price"]
        .sum()
        .reset_index()
        .rename(columns={"price": "revenue"})
    )
    return result


def get_monthly_growth_rate(sales: pd.DataFrame, year: int) -> pd.Series:
    """
    Compute month-over-month revenue growth rates within the given year.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame.
    year : int
        Calendar year to filter on.

    Returns
    -------
    pd.Series
        Indexed by month; the first month will be NaN.
    """
    monthly = _filter(sales, year).groupby("month")["price"].sum()
    return monthly.pct_change()


def get_avg_monthly_growth(sales: pd.DataFrame, year: int) -> float:
    """
    Return the mean of the month-over-month growth rates for the given year.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame.
    year : int
        Calendar year to filter on.

    Returns
    -------
    float
        Average monthly growth rate as a decimal (e.g. 0.05 represents 5%).
    """
    growth = get_monthly_growth_rate(sales, year)
    mean_val = growth.mean()
    return float(mean_val) if not pd.isna(mean_val) else 0.0


# ---------------------------------------------------------------------------
# Order metrics
# ---------------------------------------------------------------------------


def get_total_orders(
    sales: pd.DataFrame, year: int, month: Optional[int] = None
) -> int:
    """
    Count distinct delivered orders for the given period.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame.
    year : int
        Calendar year to filter on.
    month : int, optional
        Calendar month (1-12).

    Returns
    -------
    int
        Number of unique order IDs.
    """
    return int(_filter(sales, year, month)["order_id"].nunique())


def get_aov(
    sales: pd.DataFrame, year: int, month: Optional[int] = None
) -> float:
    """
    Compute the average order value (total revenue divided by order count).

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame.
    year : int
        Calendar year to filter on.
    month : int, optional
        Calendar month (1-12).

    Returns
    -------
    float
        Average order value in currency units.
    """
    subset = _filter(sales, year, month)
    per_order = subset.groupby("order_id")["price"].sum()
    mean_val = per_order.mean()
    return float(mean_val) if not pd.isna(mean_val) else 0.0


# ---------------------------------------------------------------------------
# Category and geography
# ---------------------------------------------------------------------------


def get_revenue_by_category(
    sales: pd.DataFrame,
    year: int,
    month: Optional[int] = None,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Rank product categories by total revenue in descending order.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame.
    year : int
        Calendar year to filter on.
    month : int, optional
        Calendar month (1-12).
    top_n : int
        Maximum number of categories to return.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['product_category_name', 'revenue'].
    """
    result = (
        _filter(sales, year, month)
        .groupby("product_category_name")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
        .rename(columns={"price": "revenue"})
    )
    return result


def get_revenue_by_state(
    sales: pd.DataFrame, year: int, month: Optional[int] = None
) -> pd.DataFrame:
    """
    Aggregate revenue by US state abbreviation.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame.
    year : int
        Calendar year to filter on.
    month : int, optional
        Calendar month (1-12).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['customer_state', 'revenue'].
    """
    result = (
        _filter(sales, year, month)
        .groupby("customer_state")["price"]
        .sum()
        .reset_index()
        .rename(columns={"price": "revenue"})
    )
    return result


# ---------------------------------------------------------------------------
# Delivery and experience metrics
# ---------------------------------------------------------------------------


def get_delivery_experience(
    sales: pd.DataFrame, year: int, month: Optional[int] = None
) -> pd.DataFrame:
    """
    Compute average review score per delivery time bucket.

    Delivery time buckets: '1-3 days', '4-7 days', '8+ days'.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame (must contain delivery_days and review_score).
    year : int
        Calendar year to filter on.
    month : int, optional
        Calendar month (1-12).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['delivery_time', 'avg_review_score'],
        sorted by delivery time bucket order.
    """
    subset = (
        _filter(sales, year, month)[["order_id", "delivery_days", "review_score"]]
        .drop_duplicates("order_id")
        .dropna(subset=["delivery_days", "review_score"])
        .copy()
    )
    subset["delivery_time"] = subset["delivery_days"].apply(categorize_delivery_speed)

    result = (
        subset.groupby("delivery_time")["review_score"]
        .mean()
        .reset_index()
        .rename(columns={"review_score": "avg_review_score"})
    )

    bucket_order = {"1-3 days": 0, "4-7 days": 1, "8+ days": 2}
    result["_sort"] = result["delivery_time"].map(bucket_order)
    result = (
        result.sort_values("_sort")
        .drop(columns="_sort")
        .reset_index(drop=True)
    )
    return result


def get_avg_delivery_time(
    sales: pd.DataFrame, year: int, month: Optional[int] = None
) -> float:
    """
    Return mean delivery duration in calendar days.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame.
    year : int
        Calendar year to filter on.
    month : int, optional
        Calendar month (1-12).

    Returns
    -------
    float
        Average delivery time in days.
    """
    subset = (
        _filter(sales, year, month)[["order_id", "delivery_days"]]
        .drop_duplicates("order_id")
        .dropna()
    )
    mean_val = subset["delivery_days"].mean()
    return float(mean_val) if not pd.isna(mean_val) else 0.0


def get_avg_review_score(
    sales: pd.DataFrame, year: int, month: Optional[int] = None
) -> float:
    """
    Return mean customer review score on a 1-5 scale.

    Parameters
    ----------
    sales : pd.DataFrame
        Flat sales DataFrame.
    year : int
        Calendar year to filter on.
    month : int, optional
        Calendar month (1-12).

    Returns
    -------
    float
        Average review score.
    """
    subset = (
        _filter(sales, year, month)[["order_id", "review_score"]]
        .drop_duplicates("order_id")
        .dropna()
    )
    mean_val = subset["review_score"].mean()
    return float(mean_val) if not pd.isna(mean_val) else 0.0
