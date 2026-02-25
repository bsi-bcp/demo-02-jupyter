"""
E-Commerce Sales Dashboard

A Streamlit application that visualizes sales performance metrics using
business_metrics.py for all computations and Plotly for all charts.
No raw Pandas cleaning logic is present in this file.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_loader import load_sales_data
from business_metrics import (
    get_aov,
    get_avg_delivery_time,
    get_avg_monthly_growth,
    get_avg_review_score,
    get_delivery_experience,
    get_monthly_revenue,
    get_revenue_by_category,
    get_revenue_by_state,
    get_total_orders,
    get_total_revenue,
)
from translations import TRANSLATIONS

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Sales Dashboard | 电商销售仪表盘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Data loading (cached)
# ---------------------------------------------------------------------------


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and cache the full sales DataFrame."""
    return load_sales_data()


sales = load_data()
available_years = sorted(
    sales["year"].dropna().unique().astype(int), reverse=True
)
_DEFAULT_YEAR = 2023
_default_year_index = (
    available_years.index(_DEFAULT_YEAR)
    if _DEFAULT_YEAR in available_years
    else 0
)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def pct_delta(current: float, previous: float):
    """Return percentage change, or None if previous is zero."""
    if previous == 0:
        return None
    return round(100 * (current - previous) / previous, 2)


def fmt_currency(value: float) -> str:
    """Format a numeric value as a compact currency string."""
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:.2f}"


def score_label(score: float, t: dict) -> str:
    """Convert a numeric review score to a localized descriptive text label."""
    if score >= 4.5:
        return t["score_excellent"]
    if score >= 4.0:
        return t["score_good"]
    if score >= 3.0:
        return t["score_average"]
    return t["score_below"]


# ---------------------------------------------------------------------------
# Header  (language toggle first so all subsequent text is correctly localized)
# ---------------------------------------------------------------------------

h_title, h_year, h_lang = st.columns([3, 1, 1])

with h_lang:
    lang_choice = st.radio(
        "",
        options=["English", "中文"],
        horizontal=True,
        label_visibility="collapsed",
    )

lang = "zh" if lang_choice == "中文" else "en"
t = TRANSLATIONS[lang]

with h_title:
    st.title(t["title"])

with h_year:
    selected_year = st.selectbox(t["select_year"], available_years, index=_default_year_index)

comparison_year = selected_year - 1

# ---------------------------------------------------------------------------
# Compute KPIs
# ---------------------------------------------------------------------------

rev_curr = get_total_revenue(sales, selected_year)
rev_prev = get_total_revenue(sales, comparison_year)
rev_delta = pct_delta(rev_curr, rev_prev)

growth_curr = get_avg_monthly_growth(sales, selected_year) * 100
growth_prev = get_avg_monthly_growth(sales, comparison_year) * 100
growth_delta = round(growth_curr - growth_prev, 2)

aov_curr = get_aov(sales, selected_year)
aov_prev = get_aov(sales, comparison_year)
aov_delta = pct_delta(aov_curr, aov_prev)

orders_curr = get_total_orders(sales, selected_year)
orders_prev = get_total_orders(sales, comparison_year)
orders_delta = pct_delta(orders_curr, orders_prev)

# ---------------------------------------------------------------------------
# KPI Row
# ---------------------------------------------------------------------------

st.markdown("---")
k1, k2, k3, k4 = st.columns(4)

with k1:
    delta_str = (
        f"{rev_delta:+.2f}% {t['vs']} {comparison_year}"
        if rev_delta is not None
        else t["na"]
    )
    st.metric(
        label=t["total_revenue"],
        value=fmt_currency(rev_curr),
        delta=delta_str,
        delta_color="normal",
    )

with k2:
    st.metric(
        label=t["avg_monthly_growth"],
        value=f"{growth_curr:.2f}%",
        delta=f"{growth_delta:+.2f}{t['pp_unit']} {t['vs']} {comparison_year}",
        delta_color="normal",
    )

with k3:
    delta_str = (
        f"{aov_delta:+.2f}% {t['vs']} {comparison_year}"
        if aov_delta is not None
        else t["na"]
    )
    st.metric(
        label=t["avg_order_value"],
        value=fmt_currency(aov_curr),
        delta=delta_str,
        delta_color="normal",
    )

with k4:
    delta_str = (
        f"{orders_delta:+.2f}% {t['vs']} {comparison_year}"
        if orders_delta is not None
        else t["na"]
    )
    st.metric(
        label=t["total_orders"],
        value=f"{orders_curr:,}",
        delta=delta_str,
        delta_color="normal",
    )

# ---------------------------------------------------------------------------
# Charts Row 1: Revenue trend and Top 10 categories
# ---------------------------------------------------------------------------

st.markdown("---")
chart_row1_left, chart_row1_right = st.columns(2)

# Revenue trend
with chart_row1_left:
    st.subheader(
        t["revenue_trend_title"].format(year=selected_year, comp=comparison_year)
    )

    all_months = pd.DataFrame({"month": range(1, 13)})
    monthly_curr = all_months.merge(
        get_monthly_revenue(sales, selected_year), on="month", how="left"
    ).fillna(0)
    monthly_prev = all_months.merge(
        get_monthly_revenue(sales, comparison_year), on="month", how="left"
    ).fillna(0)

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=t["months"],
        y=monthly_curr["revenue"],
        mode="lines+markers",
        name=str(selected_year),
        line=dict(color="#1f77b4", width=2),
    ))
    fig_trend.add_trace(go.Scatter(
        x=t["months"],
        y=monthly_prev["revenue"],
        mode="lines+markers",
        name=str(comparison_year),
        line=dict(color="#aec7e8", width=2, dash="dash"),
    ))
    fig_trend.update_layout(
        yaxis_tickformat="$,.0f",
        xaxis_title=t["month_axis"],
        yaxis_title=t["revenue_axis"],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=10, b=40),
        height=350,
        hovermode="x unified",
        xaxis=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            spikecolor="#888888",
            spikethickness=1,
            spikedash="dash",
        ),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# Top 10 categories
with chart_row1_right:
    st.subheader(t["top_categories_title"].format(year=selected_year))

    categories = get_revenue_by_category(sales, selected_year, top_n=10)
    categories_asc = categories.sort_values("revenue", ascending=True)

    n = len(categories_asc)
    color_scale = px.colors.sequential.Blues[2:]
    color_idx = [int(i * (len(color_scale) - 1) / max(n - 1, 1)) for i in range(n)]
    bar_colors = [color_scale[i] for i in color_idx]

    fig_cat = go.Figure(go.Bar(
        x=categories_asc["revenue"],
        y=categories_asc["product_category_name"],
        orientation="h",
        marker_color=bar_colors,
    ))
    fig_cat.update_layout(
        xaxis_tickformat="$,.0f",
        xaxis_title=t["revenue_axis"],
        margin=dict(t=10, b=40, l=160),
        height=350,
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ---------------------------------------------------------------------------
# Charts Row 2: Geographic distribution and Delivery experience
# ---------------------------------------------------------------------------

chart_row2_left, chart_row2_right = st.columns(2)

# Geographic distribution
with chart_row2_left:
    st.subheader(t["revenue_by_state_title"].format(year=selected_year))

    state_revenue = get_revenue_by_state(sales, selected_year)

    fig_map = px.choropleth(
        state_revenue,
        locations="customer_state",
        color="revenue",
        locationmode="USA-states",
        scope="usa",
        color_continuous_scale="Blues",
        labels={"revenue": t["revenue_axis"], "customer_state": t["state_label"]},
    )
    fig_map.update_layout(
        coloraxis_colorbar=dict(tickformat="$,.0f"),
        margin=dict(t=10, b=10, l=0, r=0),
        height=350,
    )
    st.plotly_chart(fig_map, use_container_width=True)

# Delivery experience
with chart_row2_right:
    st.subheader(t["delivery_exp_title"].format(year=selected_year))

    experience = get_delivery_experience(sales, selected_year)
    experience = experience.copy()
    experience["delivery_time"] = experience["delivery_time"].map(
        t["delivery_buckets"]
    )

    fig_exp = go.Figure(go.Bar(
        x=experience["delivery_time"],
        y=experience["avg_review_score"].round(2),
        marker_color=["#1f77b4", "#4e9fd4", "#aec7e8"],
        text=experience["avg_review_score"].round(2),
        textposition="outside",
    ))
    fig_exp.update_layout(
        xaxis_title=t["delivery_time_axis"],
        yaxis=dict(range=[0, 5], title=t["avg_review_score_axis"]),
        margin=dict(t=10, b=40),
        height=350,
    )
    st.plotly_chart(fig_exp, use_container_width=True)

# ---------------------------------------------------------------------------
# Bottom Row: Delivery time and Review score cards
# ---------------------------------------------------------------------------

st.markdown("---")
b1, b2, b3 = st.columns([1, 1, 2])

avg_delivery_curr = get_avg_delivery_time(sales, selected_year)
avg_delivery_prev = get_avg_delivery_time(sales, comparison_year)
delivery_delta = round(avg_delivery_curr - avg_delivery_prev, 2)

avg_score_curr = get_avg_review_score(sales, selected_year)
avg_score_prev = get_avg_review_score(sales, comparison_year)
score_delta = round(avg_score_curr - avg_score_prev, 2)

with b1:
    st.metric(
        label=t["avg_delivery_time"],
        value=f"{avg_delivery_curr:.1f} {t['days_unit']}",
        delta=f"{delivery_delta:+.2f} {t['days_unit']} {t['vs']} {comparison_year}",
        delta_color="inverse",
    )

with b2:
    st.metric(
        label=t["avg_review_score_label"],
        value=f"{avg_score_curr:.2f} / 5.0  [{score_label(avg_score_curr, t)}]",
        delta=f"{score_delta:+.2f} {t['vs']} {comparison_year}",
        delta_color="normal",
    )
