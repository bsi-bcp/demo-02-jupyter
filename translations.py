"""
UI string translations for the e-commerce sales dashboard.

Supports: English ('en'), Simplified Chinese ('zh').
"""

from typing import Dict, Any

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "en": {
        # Page and header
        "title": "E-Commerce Sales Dashboard",
        "select_year": "Select Year",
        # KPI labels
        "total_revenue": "Total Revenue",
        "avg_monthly_growth": "Avg Monthly Growth Rate",
        "avg_order_value": "Average Order Value",
        "total_orders": "Total Orders",
        # Delta text fragments
        "vs": "vs",
        "days_unit": "days",
        "pp_unit": "pp",
        "na": "N/A",
        # Chart subheaders (use .format(year=..., comp=...) to fill placeholders)
        "revenue_trend_title": "Revenue Trend: {year} vs {comp}",
        "top_categories_title": "Top 10 Categories by Revenue ({year})",
        "revenue_by_state_title": "Revenue by State ({year})",
        "delivery_exp_title": "Delivery Time vs Avg Review Score ({year})",
        # Axis and legend labels
        "month_axis": "Month",
        "revenue_axis": "Revenue",
        "delivery_time_axis": "Delivery Time",
        "avg_review_score_axis": "Avg Review Score",
        "state_label": "State",
        # Month abbreviations (index 0 = January)
        "months": [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ],
        # Bottom-row card labels
        "avg_delivery_time": "Avg Delivery Time",
        "avg_review_score_label": "Avg Review Score",
        # Review score tier labels
        "score_excellent": "Excellent",
        "score_good": "Good",
        "score_average": "Average",
        "score_below": "Below Average",
        # Delivery bucket label translation (business_metrics always returns English keys)
        "delivery_buckets": {
            "1-3 days": "1-3 days",
            "4-7 days": "4-7 days",
            "8+ days":  "8+ days",
        },
    },
    "zh": {
        # Page and header
        "title": "电商销售仪表盘",
        "select_year": "选择年份",
        # KPI labels
        "total_revenue": "总收入",
        "avg_monthly_growth": "月均增长率",
        "avg_order_value": "平均订单价值",
        "total_orders": "总订单量",
        # Delta text fragments
        "vs": "对比",
        "days_unit": "天",
        "pp_unit": "个百分点",
        "na": "暂无数据",
        # Chart subheaders
        "revenue_trend_title": "收入趋势：{year} 对比 {comp}",
        "top_categories_title": "收入前十品类（{year}）",
        "revenue_by_state_title": "各州收入分布（{year}）",
        "delivery_exp_title": "送货时效与平均评分（{year}）",
        # Axis and legend labels
        "month_axis": "月份",
        "revenue_axis": "收入",
        "delivery_time_axis": "送货时效",
        "avg_review_score_axis": "平均评分",
        "state_label": "州",
        # Month abbreviations
        "months": [
            "1月", "2月", "3月", "4月", "5月", "6月",
            "7月", "8月", "9月", "10月", "11月", "12月",
        ],
        # Bottom-row card labels
        "avg_delivery_time": "平均送货时间",
        "avg_review_score_label": "平均评价得分",
        # Review score tier labels
        "score_excellent": "优秀",
        "score_good": "良好",
        "score_average": "一般",
        "score_below": "较差",
        # Delivery bucket label translation
        "delivery_buckets": {
            "1-3 days": "1-3天",
            "4-7 days": "4-7天",
            "8+ days":  "8天以上",
        },
    },
}
