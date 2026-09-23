# 🏪 AI-Powered Sales Data Analytics and Business Insights

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)](https://jupyter.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-green?logo=scikit-learn)](https://scikit-learn.org/)

---

## Project Title

**AI-Powered Sales Data Analytics and Business Insights**

---

## Project Overview

An end-to-end data analytics and machine learning project that analyses retail sales data, extracts actionable business insights, and uses supervised regression models to predict per-order Sales amounts. Built as part of the **IBM SkillsBuild Data Analytics with AI Internship 2026** (BharatCares / AICTE).

---

## Problem Statement

Retail businesses accumulate large volumes of transactional data but rarely extract structured insights from it efficiently. This project addresses the challenge of turning raw sales records into measurable business intelligence by applying data analytics and machine learning techniques.

---

## Objectives

1. Load, inspect, clean, and validate the sales dataset systematically.
2. Engineer meaningful derived features for deeper analysis.
3. Answer 14+ key business questions with data evidence.
4. Create 13+ professional, insight-driven visualisations.
5. Build a **per-order Sales prediction model** using a proper scikit-learn Pipeline.
6. Compare three ML models (Linear Regression, Random Forest, Gradient Boosting).
7. Evaluate models using MAE, RMSE, and R² on a held-out test set.
8. Generate automated business insights using a local rule-based engine.
9. Provide data-backed business recommendations.

---

## Features

- Systematic data cleaning (missing values, duplicates, date validation, outlier analysis)
- Comprehensive EDA: KPIs, categories, regions, segments, monthly and quarterly trends
- 13+ professional charts (trend lines, heatmaps, scatter plots, bar charts, pie charts)
- Per-order Sales prediction using a `ColumnTransformer` + `OneHotEncoder` + Regressor pipeline
- Model comparison: Linear Regression vs Random Forest vs Gradient Boosting
- Feature importance analysis
- Automated Business Insight Engine (local, rule-based Python — no external API)
- Data-backed business recommendations

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Core programming language |
| Jupyter Notebook | Interactive analysis environment |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computing |
| Matplotlib | Charting and visualisation |
| Seaborn | Statistical data visualisation |
| Scikit-learn | ML models, preprocessing pipeline, evaluation |
| python-docx | Project report generation |

---

## Dataset

### Actual Dataset Used in This Project

> **File:** [`data/sales_data.csv`](data/sales_data.csv)  
> **Type:** Synthetic Superstore-style Sales Dataset — generated using Python for educational and internship demonstration purposes.  
> **Records:** 10,000 rows | **Columns:** 18 | **Period:** January 2021 – December 2023  
> **Reproducible:** Fixed random seed (42) in `data/generate_dataset.py`

The dataset is **not sourced from Kaggle or any real company**. It was programmatically generated to simulate realistic retail sales behaviour, including seasonal demand patterns, category-specific pricing, and discount distributions.

### Reference Dataset (Structure Inspiration Only)

> **Kaggle Superstore Sales Dataset:**  
> https://www.kaggle.com/datasets/himanshuuike/superstore-sales-dataset  
> *(Reference for dataset structure — not the data analysed in this project)*

---

## Project Structure

```
AI-Sales-Analytics/
│
├── data/
│   ├── sales_data.csv             ← Actual dataset (10,000 records, synthetic)
│   └── generate_dataset.py        ← Dataset generation script
│
├── notebooks/
│   └── DharvPatel_AI_Sales_Analytics.ipynb  ← Main notebook (27 sections)
│
├── src/
│   ├── analysis.py                ← Reusable helper functions
│   ├── build_notebook.py          ← Notebook builder script
│   └── generate_report.py         ← Word report generator
│
├── report/
│   └── DharvPatel_AI_Sales_Analytics_ProjectReport.docx
│
├── requirements.txt
├── README.md
├── PRESENTATION_AND_VIVA.md
└── .gitignore
```

---

## Methodology

```
Data Loading → Inspection → Cleaning → Feature Engineering
    → EDA & Visualisation → ML Pipeline Build → Model Training
        → Model Evaluation → Automated Insight Engine → Recommendations
```

### Data Cleaning
- Missing value detection (`isnull().sum()`) and handling (median/mode fill)
- Duplicate detection and removal (`drop_duplicates()`)
- Data type verification (datetime, float, int, string)
- Date validity check (Ship_Date ≥ Order_Date)
- Out-of-range value detection (Discount ∈ [0,1], Sales > 0)
- Outlier flagging using IQR method (retained for realistic analysis)

### EDA
- KPIs: Total Revenue, Total Profit, Total Orders, Average Order Value, Profit Margin
- Product, category, sub-category, region, segment performance
- Monthly, quarterly, yearly trends
- Discount-Profit correlation analysis

### Visualisations (13+ charts)

| # | Chart | Type |
|---|-------|------|
| 1 | Monthly Sales Trend | Line with fill |
| 2 | Monthly Profit Trend | Bar chart |
| 3 | Revenue by Category | Bar + Pie |
| 4 | Revenue vs Profit by Category | Grouped bar |
| 5 | Revenue and Profit by Region | Bar |
| 6 | Top 10 Products by Revenue | Horizontal bar |
| 7 | Top 10 Products by Profit | Horizontal bar |
| 8 | Sales vs Profit by Category | Scatter |
| 9 | Discount vs Profit | Colour-mapped scatter |
| 10 | Quantity vs Revenue | Scatter |
| 11 | Monthly Sales Heatmap | Seaborn heatmap |
| 12 | Correlation Heatmap | Seaborn heatmap |
| 13 | Revenue by Customer Segment | Bar + Pie |

---

## Machine Learning — Per-Order Sales Prediction

**Task:** Supervised Regression — predict `Sales` (net revenue per order)

> This is a **per-order Sales prediction model**, not a time-series demand forecast.  
> The model estimates the revenue of an individual order given its transaction attributes.

**Preprocessing Pipeline (`ColumnTransformer`):**
- Numerical features (passed through): `Month`, `Quarter`, `Year`, `Quantity`, `Discount`, `Unit_Price`
- Categorical features (OneHotEncoded): `Category`, `Region`, `Segment`, `Ship_Mode`, `Payment_Method`

**Target leakage prevention:** `Profit`, `Revenue`, `Profit_Margin`, and all Sales-derived columns are excluded from model inputs.

**Models:**

| Model | Type |
|-------|------|
| Linear Regression | Baseline — interpretable |
| Random Forest Regressor | Ensemble bagging — non-linear patterns |
| Gradient Boosting Regressor | Ensemble boosting — high accuracy |

**Split:** 80% training / 20% testing | `random_state=42`

---

## Model Evaluation

Evaluated on the 20% held-out test set. Actual metrics computed when notebook is executed:

| Model | MAE (USD) | RMSE (USD) | R² |
|-------|-----------|------------|----|
| Linear Regression | $373.62 | $633.99 | 0.7129 |
| Random Forest Regressor | $48.52 | $135.23 | 0.9869 |
| **Gradient Boosting Regressor** | **$67.47** | **$133.38** | **0.9873** |

**Best model: Gradient Boosting Regressor** — R² = 0.9873, RMSE = $133.38 per order.

> These values were computed by executing the notebook on the synthetic dataset.  
> Re-running the notebook with `random_state=42` will reproduce these exact metrics.

**Metric interpretation:**
- **MAE:** Average absolute prediction error per order (in USD)
- **RMSE:** Typical prediction error per order (in USD, penalises large errors)
- **R²:** Proportion of variance in Sales explained by the model (0–1)

---

## Automated Business Insight Engine

A **local, rule-based Python system** that programmatically inspects computed metrics and generates natural-language business observations. No external AI API (ChatGPT, Gemini, IBM Watson, etc.) is used.

Insights generated include:
- Top revenue and margin categories
- Regional revenue comparison and gap analysis
- Seasonal demand peak identification
- Discount impact quantification (Pearson correlation + percentile analysis)
- Top products by revenue and profit
- Highest-revenue customer segment
- ML model performance summary

All insight statements are computed from actual data — no hard-coded claims.

---

## Key Findings

*(Computed from the synthetic dataset — reproducible with `random_state=42`)*

1. **Total Revenue:** $6,818,142.45 | **Total Profit:** $1,073,903.31 | **Overall Margin:** 15.75%
2. **Technology** drives the highest revenue ($4,090,194.29). **Office Supplies** has the best profit margin (27.11%).
3. **South** leads regionally ($1,747,085.95). **East** is lowest ($1,646,419.58) — gap of $100,666.37.
4. **Sales peak in December** ($803,029.06) — clear Q4 seasonal demand spike confirmed.
5. Discount–Profit correlation = **−0.155**. Orders at ≥30% discount show 45.2% lower average profit.
6. Top revenue product: **Herman Miller Aeron Chair** ($523,828.45). Top profit product: **Dell XPS 15 Laptop** ($94,116.14).
7. **Consumer** segment leads in revenue ($2,313,498.80).
8. Best ML model: **Gradient Boosting Regressor** — R² = 0.9873, RMSE = $133.38 per order.

---

## Business Recommendations

All recommendations are derived from the analysis:

1. **Review high-discount transactions** where the computed Discount–Profit correlation indicates profitability risk at higher discount tiers.
2. **Pre-stock Technology products before the identified seasonal peak month** to capture demand.
3. **Target the lowest-revenue region** with marketing campaigns to close the measured revenue gap.
4. **Focus retention strategies on the highest-revenue customer segment.**
5. **Use the per-order prediction model** to estimate revenue for new order configurations.
6. **Investigate low-margin product sub-categories** (particularly in Furniture) for cost or pricing optimisation.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/AI-Sales-Analytics.git
cd AI-Sales-Analytics

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

---

## How to Run

### Run the Jupyter Notebook
```bash
jupyter notebook notebooks/DharvPatel_AI_Sales_Analytics.ipynb
```
Then in Jupyter: **Kernel → Restart & Run All**

### Execute notebook from command line
```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/DharvPatel_AI_Sales_Analytics.ipynb
```

### Regenerate the dataset
```bash
python data/generate_dataset.py
```

### Regenerate the Word report
```bash
python src/generate_report.py
```

---

## Limitations

- Dataset is synthetic and may not reflect all real-world complexities.
- No external economic or competitive factors are modelled.
- Per-order prediction only; dedicated time-series forecasting is identified as future scope.
- Default hyperparameters used; tuning could improve performance.

---

## Future Scope

- Time-series forecasting (ARIMA, SARIMA, Facebook Prophet) for period-level revenue prediction
- Customer segmentation using K-Means clustering
- Hyperparameter optimisation with GridSearchCV or Optuna
- Real-time Streamlit dashboard
- REST API deployment using FastAPI

---

## Conclusion

This project demonstrates a complete data analytics and ML pipeline: from raw synthetic sales data through cleaning, EDA, per-order Sales prediction, and automated insight generation to data-backed business recommendations. The project is reproducible, academically honest, and structured for professional presentation.

---

## Author

**Dharv Patel**  
IBM SkillsBuild Data Analytics with AI Internship 2026  
Organisation: BharatCares / AICTE / IBM SkillsBuild

---

## References

1. Kaggle Superstore Sales Dataset (structural reference): https://www.kaggle.com/datasets/himanshuuike/superstore-sales-dataset
2. Scikit-learn: https://scikit-learn.org/stable/
3. Pandas: https://pandas.pydata.org/docs/
4. Matplotlib: https://matplotlib.org/
5. Seaborn: https://seaborn.pydata.org/
6. IBM SkillsBuild: https://skillsbuild.org/

---

*This project is submitted for the AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026 | BharatCares.*
