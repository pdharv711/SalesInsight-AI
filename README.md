# 🏪 AI-Powered Sales Data Analytics and Business Insights

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)](https://jupyter.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-green?logo=scikit-learn)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 1. Project Title

**AI-Powered Sales Data Analytics and Business Insights**

---

## 2. Project Overview

An end-to-end data analytics and machine learning project that analyses retail sales data, discovers actionable business insights, and uses AI/ML to predict sales revenue. Built as part of the **IBM SkillsBuild Data Analytics with AI Internship 2026** (BharatCares / AICTE).

---

## 3. Problem Statement

Retail businesses generate large volumes of transactional data but rarely extract actionable insights efficiently. This project addresses the challenge of transforming raw sales data into measurable business intelligence using data analytics and AI techniques.

---

## 4. Objectives

- Clean, validate, and explore a large sales dataset
- Answer 14+ critical business questions with data evidence
- Create 13+ professional, insight-driven visualisations
- Build and compare three ML regression models for sales prediction
- Generate AI-assisted business insights using a local rule-based engine
- Provide actionable business recommendations

---

## 5. Features

- ✅ Comprehensive data cleaning and preprocessing
- ✅ Exploratory Data Analysis (EDA) with 13+ professional charts
- ✅ Product, category, region, and segment performance analysis
- ✅ Monthly and yearly sales trend analysis
- ✅ Discount impact analysis
- ✅ Machine learning: Linear Regression, Random Forest, Gradient Boosting
- ✅ Model evaluation with MAE, RMSE, R² metrics
- ✅ Feature importance analysis
- ✅ AI-based rule-driven business insights (no external API required)
- ✅ Actionable business recommendations

---

## 6. Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Core programming language |
| Jupyter Notebook | Latest | Interactive development environment |
| Pandas | Latest | Data manipulation and analysis |
| NumPy | Latest | Numerical computing |
| Matplotlib | Latest | Charting and visualisation |
| Seaborn | Latest | Statistical visualisation |
| Scikit-learn | Latest | ML models and evaluation |
| python-docx | Latest | Report generation |

---

## 7. Dataset Description

| Field | Details |
|-------|---------|
| **Name** | Synthetic Superstore Sales Dataset |
| **Type** | Synthetically generated (Python) |
| **Records** | 10,000 rows |
| **Columns** | 18 features |
| **Time Period** | January 2021 – December 2023 |

**Dataset Note:** The dataset used in this project is synthetically generated using Python for educational and internship demonstration purposes. It is modelled after the structure of publicly available Superstore-style retail datasets.

---

## 8. Dataset Source / Dataset Link

> **Reference Dataset (Structure):**  
> Kaggle Superstore Sales Dataset  
> 🔗 https://www.kaggle.com/datasets/himanshuuike/superstore-sales-dataset

The synthetic dataset file is included in the repository at `data/sales_data.csv`.

---

## 9. Project Structure

```
AI-Sales-Analytics/
│
├── data/
│   ├── sales_data.csv          ← Synthetic sales dataset (10,000 records)
│   └── generate_dataset.py     ← Dataset generation script
│
├── notebooks/
│   └── DharvPatel_AI_Sales_Analytics.ipynb  ← Main Jupyter Notebook
│
├── src/
│   ├── analysis.py             ← Reusable analysis helper functions
│   └── build_notebook.py       ← Notebook generation script
│
├── report/
│   └── DharvPatel_AI_Sales_Analytics_ProjectReport.docx  ← Project Report
│
├── requirements.txt            ← Python dependencies
├── README.md                   ← This file
├── PRESENTATION_AND_VIVA.md   ← Viva preparation guide
└── .gitignore                  ← Git exclusions
```

---

## 10. Methodology

```
Raw Data → Data Cleaning → Feature Engineering → EDA → Visualisation
    → ML Model Training → Model Evaluation → Business Insights → Recommendations
```

### Step-by-Step:
1. **Data Collection:** Load synthetic sales dataset (CSV)
2. **Inspection:** Shape, dtypes, missing values, duplicates
3. **Cleaning:** Handle missing values, remove duplicates, fix data types, detect invalid values
4. **Feature Engineering:** Add Year, Month, Quarter, Profit_Margin, Discount_Amount
5. **EDA:** KPI computation, category/region/segment/monthly analysis
6. **Visualisation:** 13+ charts (trends, bar charts, scatter plots, heatmaps)
7. **ML Training:** Linear Regression, Random Forest, Gradient Boosting
8. **Evaluation:** MAE, MSE, RMSE, R² metrics + Actual vs Predicted plot
9. **Insights:** Rule-based Python insight engine (no API)
10. **Recommendations:** Actionable business strategy based on findings

---

## 11. Data Cleaning

- Missing value detection and handling (median for numerical, mode for categorical)
- Duplicate row detection and removal
- Data type verification (datetime, float, integer, string)
- Date validity checks (Ship_Date ≥ Order_Date)
- Invalid value detection (negative sales, out-of-range discounts)
- Outlier analysis using the IQR method (flagged but retained for realistic analysis)

---

## 12. Exploratory Data Analysis

KPIs computed:
- Total Revenue, Total Profit, Total Orders
- Average Order Value, Average Profit, Average Discount
- Overall Profit Margin

Analyses performed:
- Product, category, sub-category, region, segment, monthly, quarterly performance
- Discount impact on profit
- Seasonal patterns

---

## 13. Machine Learning Approach

**Task:** Sales (Revenue) Regression — Predict net sales per order

**Features:** Month, Quarter, Year, Category (encoded), Region (encoded), Segment (encoded), Quantity, Discount, Unit_Price

**Models:**

| Model | Type | Reason Selected |
|-------|------|----------------|
| Linear Regression | Baseline | Interpretable, fast |
| Random Forest Regressor | Ensemble | Handles non-linearity, robust |
| Gradient Boosting Regressor | Ensemble | High accuracy, complex patterns |

**Evaluation Metrics:** MAE, MSE, RMSE, R²

---

## 14. AI-Based Insights

A **local, rule-based Python insight engine** automatically inspects computed metrics and generates natural-language business insights. No external LLM, API key, or internet connection is required. This approach ensures the project is:
- Fully reproducible offline
- Transparent and explainable
- 100% verifiable (insights tied to actual computed values)

---

## 15. Key Findings

1. Clear Q4 seasonal demand spikes (November–December)
2. Technology category drives the highest revenue
3. Office Supplies delivers the best profit margins
4. Discounts above 20% significantly erode profitability
5. A small number of products generate a disproportionate share of revenue
6. Random Forest and Gradient Boosting models show the best prediction performance

---

## 16. Business Recommendations

1. 🔴 Implement a 20% maximum discount policy to protect margins
2. 🔴 Pre-stock Technology products before Q4 to capture peak demand
3. 🟡 Launch targeted marketing in the lowest-performing region
4. 🟡 Develop loyalty programmes for the top customer segment
5. 🟢 Use the ML model for quarterly sales forecasting

---

## 17. Installation Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Sales-Analytics.git
cd AI-Sales-Analytics
```

### Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 18. How to Run

### Option A: Run the Jupyter Notebook (Recommended)

```bash
jupyter notebook notebooks/DharvPatel_AI_Sales_Analytics.ipynb
```

Then click **"Run All"** in the Jupyter interface (Kernel → Restart & Run All).

### Option B: Run with JupyterLab

```bash
jupyter lab notebooks/DharvPatel_AI_Sales_Analytics.ipynb
```

### Option C: Execute Notebook from Command Line

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/DharvPatel_AI_Sales_Analytics.ipynb
```

---

## 19. How to Regenerate the Dataset

If you want to regenerate the synthetic dataset:

```bash
python data/generate_dataset.py
```

This creates a fresh `data/sales_data.csv` with 10,000 records.

---

## 20. Example Results

After running the notebook, you will see outputs such as:

```
KEY PERFORMANCE INDICATORS (KPIs)
Total Revenue         : $X,XXX,XXX.XX
Total Profit          : $XXX,XXX.XX
Total Orders          : 10,000
Total Quantity Sold   : XX,XXX
Average Order Value   : $XXX.XX
Overall Profit Margin : XX.XX%
```

**ML Model Performance (sample):**

| Model | MAE | RMSE | R² |
|-------|-----|------|----|
| Linear Regression | ~$XXX | ~$XXX | ~0.XX |
| Random Forest | ~$XXX | ~$XXX | ~0.XX |
| Gradient Boosting | ~$XXX | ~$XXX | ~0.XX |

*(Actual values are computed when the notebook is executed)*

---

## 21. Limitations

- Dataset is synthetic and may not capture all real-world complexities
- No external economic factors included in ML features
- Static batch analysis — not real-time
- Simple label encoding used for categorical variables

---

## 22. Future Scope

- Real-time Streamlit dashboard
- Time-series forecasting (ARIMA, Prophet)
- Customer segmentation (K-Means clustering)
- Advanced feature engineering and hyperparameter tuning
- REST API deployment for the prediction model

---

## 23. Conclusion

This project demonstrates a complete data analytics and AI pipeline applied to retail sales data. From cleaning raw data to generating ML-backed predictions and actionable business insights, the workflow reflects real-world data science practice.

---

## 24. Author

**Dharv Patel**  
IBM SkillsBuild Data Analytics with AI Internship 2026  
Organisation: BharatCares / AICTE / IBM SkillsBuild

---

## 25. References

1. Kaggle Superstore Sales Dataset: https://www.kaggle.com/datasets/himanshuuike/superstore-sales-dataset
2. Scikit-learn Documentation: https://scikit-learn.org/stable/
3. Pandas Documentation: https://pandas.pydata.org/docs/
4. Seaborn Documentation: https://seaborn.pydata.org/
5. Matplotlib Documentation: https://matplotlib.org/stable/
6. IBM SkillsBuild: https://skillsbuild.org/

---

*This project is created for educational and internship demonstration purposes as part of the AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026 | BharatCares.*
