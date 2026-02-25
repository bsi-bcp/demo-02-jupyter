# E-Commerce Sales Dashboard | 电商销售仪表盘

[English](#english) | [中文简体](#中文简体)

---

## English

An interactive Streamlit dashboard for e-commerce sales analysis, built on a
modular Python backend.

### Project Structure

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
├── translations.py             # English and Simplified Chinese UI strings
├── app.py                      # Streamlit dashboard
├── EDA_Refactored.ipynb        # Structured exploratory analysis notebook
├── requirements.txt            # Python dependencies
└── README.md
```

### Architecture

| Module | Responsibility |
|---|---|
| `data_loader.py` | Reads CSVs, normalizes dates, joins all tables into a flat sales DataFrame |
| `business_metrics.py` | Stateless metric functions; all accept `year` and optional `month` parameters |
| `translations.py` | All UI strings in English and Simplified Chinese |
| `app.py` | Streamlit UI; calls only `business_metrics` functions, contains no cleaning logic |
| `EDA_Refactored.ipynb` | Analysis notebook; imports from both modules |

### Setup

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

### Dashboard Features

- **Language toggle** (English / Chinese) in the header; all labels switch instantly.
- **Year selector** in the header; all charts and KPIs update instantly.
- **KPI cards**: Total Revenue, Avg Monthly Growth Rate, Average Order Value,
  Total Orders — each with a year-over-year delta indicator.
- **Revenue trend chart**: current year (solid line) vs prior year (dashed line).
- **Top 10 categories chart**: horizontal bar chart with blue gradient coloring.
- **Geographic map**: US state-level revenue choropleth (blue scale).
- **Delivery experience chart**: avg review score by delivery time bucket.
- **Summary cards**: avg delivery time and avg review score with prior-year delta.

### Configuration

To analyze a different data directory, pass `data_dir` to `load_sales_data`:

```python
from data_loader import load_sales_data
sales = load_sales_data(data_dir="/path/to/your/data")
```

All metric functions accept `year` and optional `month` parameters, making
the framework portable to any time period present in the data.

---

## 中文简体

基于模块化 Python 后端构建的电商销售数据交互式 Streamlit 仪表盘，支持中英双语切换。

### 项目结构

```
02.wed-jupyter/
├── ecommerce_data/             # 原始 CSV 数据文件
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── products_dataset.csv
│   ├── customers_dataset.csv
│   ├── order_reviews_dataset.csv
│   └── order_payments_dataset.csv
├── data_loader.py              # 数据读取、预处理与多表关联
├── business_metrics.py         # 业务指标纯函数（支持 year/month 参数）
├── translations.py             # 中英双语 UI 文本
├── app.py                      # Streamlit 仪表盘主程序
├── EDA_Refactored.ipynb        # 结构化探索性分析笔记本
├── requirements.txt            # Python 依赖清单
└── README.md
```

### 架构说明

| 模块 | 职责 |
|---|---|
| `data_loader.py` | 读取 CSV、标准化日期、多表关联，输出扁平化销售 DataFrame |
| `business_metrics.py` | 无状态指标函数，全部支持 `year` 和可选 `month` 参数 |
| `translations.py` | 中英双语 UI 字符串词典 |
| `app.py` | Streamlit 前端，仅调用 `business_metrics`，不含任何数据清洗逻辑 |
| `EDA_Refactored.ipynb` | 分析笔记本，从两个模块导入 |

### 快速开始

**1. 安装依赖**

```bash
pip install -r requirements.txt
```

**2. 启动仪表盘**

在 `02.wed-jupyter/` 目录下执行：

```bash
streamlit run app.py
```

浏览器访问 `http://localhost:8501`。

**3. 运行笔记本**

```bash
jupyter notebook EDA_Refactored.ipynb
```

### 仪表盘功能

- **语言切换**（English / 中文）：页面顶部切换，所有标签即时更新。
- **年份选择器**：默认 2023 年，切换后全局图表与指标联动刷新。
- **KPI 卡片**：总收入、月均增长率、平均订单价值、总订单量，每项附带同比涨跌幅。
- **收入趋势图**：当前年实线 vs 对比年虚线。
- **品类排行图**：前十品类横向柱状图，蓝色渐变配色。
- **地理分布图**：美国州级收入 Choropleth 地图（蓝色调）。
- **送货体验图**：不同送货时效区间的平均评分对比。
- **底部指标卡**：平均送货天数、平均评分（含等级文案与同比变化）。

### 配置说明

如需切换数据目录，向 `load_sales_data` 传入 `data_dir` 参数：

```python
from data_loader import load_sales_data
sales = load_sales_data(data_dir="/your/data/path")
```

所有指标函数均支持 `year` 和可选 `month` 参数，可直接适配数据中的任意时间段。
