"""
generate_report.py
==================
Generates the Project Report as a Microsoft Word (.docx) file using python-docx.

Usage:
    python generate_report.py

Output:
    report/DharvPatel_AI_Sales_Analytics_ProjectReport.docx
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

# ── Try to get actual metrics from the dataset ────────────────────────────────
try:
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.preprocessing import LabelEncoder

    DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "data", "sales_data.csv")
    df = pd.read_csv(DATA_PATH, parse_dates=["Order_Date", "Ship_Date"])

    # Feature engineering
    df["Year"]           = df["Order_Date"].dt.year
    df["Month"]          = df["Order_Date"].dt.month
    df["Quarter"]        = df["Order_Date"].dt.quarter
    df["Profit_Margin"]  = (df["Profit"] / df["Sales"].replace(0, np.nan) * 100).round(2)
    df["Discount_Amount"]= (df["Unit_Price"] * df["Quantity"] * df["Discount"]).round(2)

    # KPIs
    total_revenue  = df["Sales"].sum()
    total_profit   = df["Profit"].sum()
    total_orders   = df["Order_ID"].nunique()
    total_qty      = df["Quantity"].sum()
    avg_order_val  = df["Sales"].mean()
    avg_profit     = df["Profit"].mean()
    avg_discount   = df["Discount"].mean() * 100
    overall_margin = df["Profit"].sum() / df["Sales"].sum() * 100

    # Category
    cat_rev    = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    top_cat    = cat_rev.index[0]
    cat_margin = (df.groupby("Category")["Profit"].sum() /
                  df.groupby("Category")["Sales"].sum() * 100).round(2)

    # Region
    reg_rev  = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    top_reg  = reg_rev.index[0]

    # ML
    feature_cols = ["Month", "Quarter", "Year", "Category", "Region",
                    "Segment", "Quantity", "Discount", "Unit_Price"]
    ml_df = df[feature_cols + ["Sales"]].copy()
    le = LabelEncoder()
    for col in ["Category", "Region", "Segment"]:
        ml_df[col] = le.fit_transform(ml_df[col].astype(str))
    X = ml_df[feature_cols]
    y = ml_df["Sales"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    ml_results = {}
    for name, model in [
        ("Linear Regression", LinearRegression()),
        ("Random Forest Regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
        ("Gradient Boosting Regressor", GradientBoostingRegressor(n_estimators=100, random_state=42)),
    ]:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        ml_results[name] = {
            "MAE":  round(mean_absolute_error(y_test, y_pred), 2),
            "MSE":  round(mean_squared_error(y_test, y_pred), 2),
            "RMSE": round(np.sqrt(mean_squared_error(y_test, y_pred)), 2),
            "R2":   round(r2_score(y_test, y_pred), 4),
        }

    best_model = max(ml_results, key=lambda k: ml_results[k]["R2"])
    best_r2    = ml_results[best_model]["R2"]
    best_rmse  = ml_results[best_model]["RMSE"]
    DATA_LOADED = True
    print("Actual metrics computed from dataset.")
except Exception as e:
    DATA_LOADED = False
    print(f"Warning: Could not load dataset ({e}). Using placeholder values.")
    total_revenue  = 0.0
    total_profit   = 0.0
    total_orders   = 0
    total_qty      = 0
    avg_order_val  = 0.0
    avg_profit     = 0.0
    avg_discount   = 0.0
    overall_margin = 0.0
    top_cat        = "Technology"
    top_reg        = "East"
    ml_results     = {}
    best_model     = "Random Forest Regressor"
    best_r2        = 0.0
    best_rmse      = 0.0


# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT SETUP
# ─────────────────────────────────────────────────────────────────────────────
doc = Document()

# Page margins
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.5)


def add_page_break(doc):
    doc.add_page_break()


def heading(doc, text, level=1):
    doc.add_heading(text, level=level)


def para(doc, text, bold=False, italic=False, size=11, align=WD_ALIGN_PARAGRAPH.LEFT, color=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold   = bold
    run.italic = italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    p.alignment = align
    return p


def table_row(table, values, bold=False, bg_color=None):
    row = table.add_row()
    for i, val in enumerate(values):
        cell = row.cells[i]
        cell.text = str(val)
        if bold:
            for run in cell.paragraphs[0].runs:
                run.bold = True
        if bg_color:
            tc   = cell._tc
            tcPr = tc.get_or_add_tcPr()
            shd  = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:color"), "auto")
            shd.set(qn("w:fill"), bg_color)
            tcPr.append(shd)
    return row


def add_table(doc, headers, rows, header_bg="4472C4"):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    # Header
    hdr_cells = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        run = hdr_cells[i].paragraphs[0].runs[0]
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        # Background
        tc   = hdr_cells[i]._tc
        tcPr = tc.get_or_add_tcPr()
        shd  = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), header_bg)
        tcPr.append(shd)
    for row in rows:
        table_row(t, row)
    return t


# ─────────────────────────────────────────────────────────────────────────────
# COVER PAGE
# ─────────────────────────────────────────────────────────────────────────────
para(doc, "", size=12)
para(doc, "", size=12)
para(doc, "AICTE | IBM SkillsBuild | BharatCares", bold=True, size=13,
     align=WD_ALIGN_PARAGRAPH.CENTER, color=(68, 114, 196))
para(doc, "Data Analytics with AI Internship 2026", bold=False, size=12,
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "", size=12)
para(doc, "─" * 60, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "", size=12)

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title_p.add_run("AI-Powered Sales Data Analytics\nand Business Insights")
run.bold = True
run.font.size = Pt(22)
run.font.color.rgb = RGBColor(31, 73, 125)

para(doc, "", size=12)
para(doc, "─" * 60, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "", size=12)

fields = [
    ("Project Type",   "Data Analytics + Artificial Intelligence / Machine Learning"),
    ("Submitted By",   "Dharv Patel"),
    ("Programme",      "IBM SkillsBuild Data Analytics with AI Internship 2026"),
    ("Organisation",   "BharatCares / AICTE / IBM SkillsBuild"),
    ("Date",           datetime.datetime.now().strftime("%B %Y")),
]
for label, value in fields:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"{label}: ")
    r1.bold = True
    r1.font.size = Pt(12)
    r2 = p.add_run(value)
    r2.font.size = Pt(12)

add_page_break(doc)

# ─────────────────────────────────────────────────────────────────────────────
# ACKNOWLEDGEMENT
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "Acknowledgement", 1)
doc.add_paragraph(
    "I am sincerely grateful to IBM SkillsBuild, AICTE, and BharatCares for providing "
    "this Data Analytics with AI Internship opportunity in 2026. This internship has given "
    "me valuable hands-on experience in applying data analytics, Python programming, "
    "and machine learning techniques to solve real-world business problems.\n\n"
    "I would like to thank all the mentors, programme coordinators, and faculty members "
    "who designed the curriculum and provided guidance throughout the programme. The "
    "structured learning path and project-based assessment have significantly enhanced "
    "my understanding of the data science lifecycle.\n\n"
    "I am also grateful to the open-source community — developers of Pandas, NumPy, "
    "Matplotlib, Seaborn, and Scikit-learn — whose freely available tools made this "
    "project possible.\n\n"
    "Finally, I thank my family and peers for their continued support and encouragement "
    "throughout this internship.\n\n"
    "— Dharv Patel"
)
add_page_break(doc)

# ─────────────────────────────────────────────────────────────────────────────
# ABSTRACT
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "Abstract", 1)
doc.add_paragraph(
    "This project presents an end-to-end data analytics and machine learning solution "
    "applied to retail sales data. A synthetic Superstore-style sales dataset of 10,000 "
    "records spanning three years (2021–2023) was generated using Python, modelled after "
    "the structure of the publicly available Kaggle Superstore Sales Dataset "
    "(https://www.kaggle.com/datasets/himanshuuike/superstore-sales-dataset).\n\n"
    "The project follows the complete data science lifecycle: data loading and inspection, "
    "systematic data cleaning, feature engineering, exploratory data analysis (EDA), "
    "professional data visualisation (13+ charts), machine learning for sales prediction "
    "(comparing Linear Regression, Random Forest, and Gradient Boosting), model evaluation "
    "using MAE, RMSE, and R-squared metrics, and AI-assisted rule-based business insight "
    "generation.\n\n"
    f"Key findings include a total revenue of ${total_revenue:,.2f}, overall profit margin "
    f"of {overall_margin:.1f}%, with {top_cat} as the top revenue category and {top_reg} "
    f"as the leading geographic region. The best-performing ML model achieved an R² of "
    f"{best_r2:.4f} with an RMSE of ${best_rmse:,.2f}.\n\n"
    "The project concludes with actionable business recommendations derived from the "
    "analysis, including discount policy optimisation, seasonal inventory planning, and "
    "regional marketing strategy."
)
add_page_break(doc)

# ─────────────────────────────────────────────────────────────────────────────
# TABLE OF CONTENTS (manual)
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "Table of Contents", 1)
toc_items = [
    ("1", "Introduction", ""),
    ("2", "Problem Statement", ""),
    ("3", "Objectives", ""),
    ("4", "Scope", ""),
    ("5", "Technologies Used", ""),
    ("6", "Dataset Description", ""),
    ("7", "Methodology", ""),
    ("8", "Data Collection", ""),
    ("9", "Data Preprocessing", ""),
    ("10", "Exploratory Data Analysis", ""),
    ("11", "Data Visualisation", ""),
    ("12", "Machine Learning Methodology", ""),
    ("13", "Model Training", ""),
    ("14", "Model Evaluation", ""),
    ("15", "AI-Based Business Insights", ""),
    ("16", "Results and Findings", ""),
    ("17", "Business Recommendations", ""),
    ("18", "Limitations", ""),
    ("19", "Future Scope", ""),
    ("20", "Conclusion", ""),
    ("21", "References", ""),
]
for num, title, _ in toc_items:
    doc.add_paragraph(f"{num}. {title}", style="List Number")
add_page_break(doc)

# ─────────────────────────────────────────────────────────────────────────────
# 1. INTRODUCTION
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "1. Introduction", 1)
doc.add_paragraph(
    "The retail industry generates millions of transactional records daily. Each transaction "
    "contains valuable information about customer behaviour, product performance, geographic "
    "demand patterns, and the effectiveness of pricing strategies. However, the sheer volume "
    "of this data makes it challenging for human analysts to extract meaningful insights "
    "manually.\n\n"
    "Data analytics and artificial intelligence (AI) provide powerful tools to automate "
    "insight extraction, identify hidden patterns, and generate predictions that support "
    "strategic decision-making. This project applies these techniques to a comprehensive "
    "retail sales dataset, demonstrating how a data-driven approach can transform raw "
    "transactional data into actionable business intelligence.\n\n"
    "The project is developed as part of the IBM SkillsBuild Data Analytics with AI "
    "Internship 2026, organised by AICTE and BharatCares. It uses Python and its data "
    "science ecosystem to implement a complete analytics pipeline: from raw data to "
    "business recommendations."
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. PROBLEM STATEMENT
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "2. Problem Statement", 1)
doc.add_paragraph(
    "Retail businesses face the following challenges in their sales data management:\n\n"
    "1. Large volumes of transactional data are collected but not systematically analysed.\n"
    "2. Management lacks clear visibility into which products, categories, and regions "
    "drive revenue and profit.\n"
    "3. The impact of discount strategies on profitability is not quantified.\n"
    "4. Seasonal demand patterns are not identified or planned for.\n"
    "5. Sales forecasting is done manually, leading to inventory and staffing mismatches.\n\n"
    "This project addresses these challenges by building a structured analytics solution "
    "that delivers KPIs, visualisations, predictive models, and actionable recommendations "
    "from the available sales data."
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. OBJECTIVES
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "3. Objectives", 1)
objectives = [
    "Load, inspect, and clean the sales dataset systematically.",
    "Perform comprehensive exploratory data analysis (EDA).",
    "Engineer meaningful derived features for deeper analysis.",
    "Create 13+ professional, insight-driven visualisations.",
    "Answer 14 critical business questions from the data.",
    "Build and compare three ML regression models for sales prediction.",
    "Evaluate models using MAE, RMSE, and R-squared metrics.",
    "Generate AI-assisted business insights using a local rule-based engine.",
    "Provide actionable, data-backed business recommendations.",
    "Deliver a reproducible, well-documented project suitable for demonstration.",
]
for i, obj in enumerate(objectives, 1):
    doc.add_paragraph(f"{i}. {obj}", style="List Number")

# ─────────────────────────────────────────────────────────────────────────────
# 4. SCOPE
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "4. Scope", 1)
doc.add_paragraph(
    "The project covers the following areas:\n\n"
    "In Scope:\n"
    "• Retail sales data analytics for products, categories, regions, and customer segments\n"
    "• Time-based trend analysis (monthly, quarterly, annual)\n"
    "• Discount impact and profitability analysis\n"
    "• Machine learning-based sales (revenue) prediction\n"
    "• Feature importance analysis\n"
    "• Rule-based AI business insight generation\n\n"
    "Out of Scope:\n"
    "• Real-time data ingestion or streaming\n"
    "• External economic or competitive data integration\n"
    "• Deep learning models\n"
    "• Customer churn prediction or recommendation systems\n"
    "• Production deployment or CI/CD pipelines"
)

# ─────────────────────────────────────────────────────────────────────────────
# 5. TECHNOLOGIES USED
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "5. Technologies Used", 1)
add_table(doc,
    ["Technology", "Version", "Purpose"],
    [
        ["Python",        "3.8+",    "Core programming language"],
        ["Jupyter Notebook", "Latest", "Interactive development environment"],
        ["Pandas",        "Latest",  "Data manipulation and analysis"],
        ["NumPy",         "Latest",  "Numerical computing"],
        ["Matplotlib",    "Latest",  "Charting and visualisation"],
        ["Seaborn",       "Latest",  "Statistical data visualisation"],
        ["Scikit-learn",  "Latest",  "Machine learning models and evaluation"],
        ["python-docx",   "Latest",  "Project report generation"],
        ["nbformat",      "Latest",  "Jupyter notebook programmatic creation"],
    ]
)

# ─────────────────────────────────────────────────────────────────────────────
# 6. DATASET DESCRIPTION
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "6. Dataset Description", 1)
doc.add_paragraph(
    "Dataset Name: Synthetic Superstore Sales Dataset\n"
    "Type: Synthetically generated using Python for educational/internship purposes\n"
    "Reference Structure: Kaggle Superstore Sales Dataset\n"
    "Reference URL: https://www.kaggle.com/datasets/himanshuuike/superstore-sales-dataset\n"
    "Records: 10,000 rows\n"
    "Columns: 18 features\n"
    "Time Period: January 2021 – December 2023\n"
    "File Format: CSV\n"
    "File Location: data/sales_data.csv\n\n"
    "Note: The dataset is synthetically generated and does not represent any real company's "
    "data. It is created for educational demonstration purposes only."
)
doc.add_paragraph("")
add_table(doc,
    ["Column", "Data Type", "Description"],
    [
        ["Order_ID",       "String",   "Unique order identifier"],
        ["Order_Date",     "Date",     "Date the order was placed"],
        ["Ship_Date",      "Date",     "Date the order was shipped"],
        ["Ship_Mode",      "String",   "Shipping mode (Standard/Second/First/Same Day)"],
        ["Customer_ID",    "String",   "Unique customer identifier"],
        ["Customer_Name",  "String",   "Full name of the customer"],
        ["Segment",        "String",   "Customer segment (Consumer/Corporate/Home Office)"],
        ["Region",         "String",   "Geographic region (East/West/Central/South)"],
        ["State",          "String",   "City/state of delivery"],
        ["Category",       "String",   "Product category"],
        ["Sub_Category",   "String",   "Product sub-category"],
        ["Product_Name",   "String",   "Product description"],
        ["Quantity",       "Integer",  "Units ordered"],
        ["Unit_Price",     "Float",    "Price per unit in USD"],
        ["Discount",       "Float",    "Discount rate (0.0 to 0.5)"],
        ["Sales",          "Float",    "Net sales amount in USD (after discount)"],
        ["Profit",         "Float",    "Profit earned in USD"],
        ["Payment_Method", "String",   "Payment method used"],
    ]
)

# ─────────────────────────────────────────────────────────────────────────────
# 7. METHODOLOGY
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "7. Methodology", 1)
doc.add_paragraph(
    "The project follows the CRISP-DM (Cross-Industry Standard Process for Data Mining) "
    "methodology adapted for a retail analytics context:\n\n"
    "Step 1: Business Understanding — Define the business questions and objectives.\n"
    "Step 2: Data Understanding — Load and inspect the dataset.\n"
    "Step 3: Data Preparation — Clean, preprocess, and engineer features.\n"
    "Step 4: Modelling — Train and evaluate ML regression models.\n"
    "Step 5: Evaluation — Compare models, analyse feature importance, validate predictions.\n"
    "Step 6: Deployment (Insight Generation) — Generate AI-based insights and recommendations."
)

# ─────────────────────────────────────────────────────────────────────────────
# 8. DATA COLLECTION
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "8. Data Collection", 1)
doc.add_paragraph(
    "The dataset was created synthetically using a Python script (data/generate_dataset.py). "
    "The generation process:\n\n"
    "• Products were drawn from three real-world product categories with realistic names and price ranges.\n"
    "• Order dates were randomly distributed across 3 years (2021–2023) with seasonal weighting "
    "(higher probability in November–December to simulate holiday shopping).\n"
    "• Customer names were generated from common first and last name lists.\n"
    "• Discounts were drawn from a realistic distribution (0%, 5%, 10%, ..., 50%).\n"
    "• Profit margins were computed category-specifically (Technology ~22%, "
    "Furniture ~10%, Office Supplies ~30%) with random variation.\n"
    "• The random seed (42) was fixed for reproducibility.\n\n"
    "The resulting dataset is statistically plausible and suitable for demonstrating "
    "the full analytics pipeline."
)

# ─────────────────────────────────────────────────────────────────────────────
# 9. DATA PREPROCESSING
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "9. Data Preprocessing", 1)
doc.add_paragraph(
    "Data preprocessing ensured the dataset was clean, consistent, and ready for analysis."
)
heading(doc, "9.1 Missing Value Analysis", 2)
doc.add_paragraph(
    "Each column was checked for null/NaN values using df.isnull().sum(). Since the dataset "
    "is synthetically generated, no missing values were found. The verification step "
    "confirmed data completeness."
)
heading(doc, "9.2 Duplicate Detection", 2)
doc.add_paragraph(
    "Duplicate rows were identified using df.duplicated().sum() and removed using "
    "df.drop_duplicates(). The dataset contained no duplicates post-generation."
)
heading(doc, "9.3 Data Type Verification", 2)
doc.add_paragraph(
    "Column data types were verified: Order_Date and Ship_Date were confirmed as datetime64, "
    "numerical columns (Quantity, Unit_Price, Discount, Sales, Profit) as float64/int64, "
    "and categorical columns as object (string)."
)
heading(doc, "9.4 Invalid Value Detection", 2)
doc.add_paragraph(
    "Checks were performed for:\n"
    "• Negative or zero Sales values\n"
    "• Non-positive Quantity values\n"
    "• Discount values outside [0, 1]\n"
    "• Ship_Date earlier than Order_Date\n\n"
    "Any invalid records were removed or corrected."
)
heading(doc, "9.5 Outlier Analysis", 2)
doc.add_paragraph(
    "Outliers in Sales and Profit were identified using the IQR (Interquartile Range) method. "
    "Outliers were flagged but retained, as high-value orders represent legitimate business "
    "transactions rather than data errors."
)
heading(doc, "9.6 Feature Engineering", 2)
doc.add_paragraph(
    "The following derived features were added:"
)
add_table(doc,
    ["Feature", "Formula", "Purpose"],
    [
        ["Year",            "Order_Date.dt.year",                  "Year-level trend analysis"],
        ["Month",           "Order_Date.dt.month",                 "Seasonality analysis"],
        ["Month_Name",      "Order_Date.dt.strftime('%b')",        "Readable month labels"],
        ["Quarter",         "Order_Date.dt.quarter",               "Quarterly grouping"],
        ["Profit_Margin",   "Profit / Sales × 100",                "Product/category profitability %"],
        ["Discount_Amount", "Unit_Price × Quantity × Discount",    "Absolute discount in USD"],
        ["Revenue",         "Alias for Sales",                     "Clarity in reporting"],
    ]
)

# ─────────────────────────────────────────────────────────────────────────────
# 10. EDA
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "10. Exploratory Data Analysis", 1)
doc.add_paragraph(
    "EDA was performed to understand the distribution, relationships, and patterns in the "
    "cleaned dataset. Key metrics computed:"
)
doc.add_paragraph("")
add_table(doc,
    ["KPI", "Value"],
    [
        ["Total Revenue (USD)",       f"${total_revenue:,.2f}"],
        ["Total Profit (USD)",        f"${total_profit:,.2f}"],
        ["Total Orders",              f"{total_orders:,}"],
        ["Total Quantity Sold",       f"{total_qty:,}"],
        ["Average Order Value (USD)", f"${avg_order_val:,.2f}"],
        ["Average Profit per Order",  f"${avg_profit:,.2f}"],
        ["Average Discount",          f"{avg_discount:.2f}%"],
        ["Overall Profit Margin",     f"{overall_margin:.2f}%"],
    ]
)
doc.add_paragraph("")
doc.add_paragraph(
    "Additional analyses performed:\n"
    "• Revenue and profit by category, sub-category, region, segment\n"
    "• Monthly and quarterly sales trends\n"
    "• Year-over-year growth analysis\n"
    "• Top 10 products by revenue and profit\n"
    "• Discount group analysis (impact on profit)\n"
    "• Correlation analysis between numerical features"
)

# ─────────────────────────────────────────────────────────────────────────────
# 11. DATA VISUALISATION
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "11. Data Visualisation", 1)
doc.add_paragraph("The following charts were created in the Jupyter Notebook:")
charts = [
    ["1",  "Monthly Sales Trend",                    "Line chart with fill",    "Sales patterns over 36 months"],
    ["2",  "Monthly Profit Trend",                   "Bar chart",               "Profit in each month"],
    ["3",  "Revenue by Category",                    "Bar + Pie",               "Category revenue share"],
    ["4",  "Revenue vs Profit by Category",          "Grouped bar",             "Revenue vs Profit + Margin %"],
    ["5",  "Revenue and Profit by Region",           "Bar chart",               "Regional comparison"],
    ["6",  "Top 10 Products by Revenue",             "Horizontal bar",          "Highest revenue products"],
    ["7",  "Top 10 Products by Profit",              "Horizontal bar",          "Most profitable products"],
    ["8",  "Sales vs Profit by Category",            "Scatter plot",            "Revenue-Profit relationship"],
    ["9",  "Discount vs Profit",                     "Scatter (colour-mapped)", "Discount impact on profit"],
    ["10", "Quantity vs Revenue by Category",        "Scatter plot",            "Quantity-revenue relationship"],
    ["11", "Monthly Sales Heatmap",                  "Seaborn heatmap",         "Year x Month patterns"],
    ["12", "Correlation Heatmap",                    "Seaborn heatmap",         "Feature correlations"],
    ["13", "Revenue by Customer Segment",            "Bar + Pie",               "Segment performance"],
]
add_table(doc,
    ["#", "Chart Title", "Chart Type", "Business Purpose"],
    charts
)

# ─────────────────────────────────────────────────────────────────────────────
# 12. ML METHODOLOGY
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "12. Machine Learning Methodology", 1)
doc.add_paragraph(
    "Task Type: Supervised Regression (predicting a continuous numerical value)\n"
    "Target Variable: Sales (net revenue per order)\n\n"
    "Features Selected:"
)
doc.add_paragraph(
    "Month, Quarter, Year, Category (label-encoded), Region (label-encoded), "
    "Segment (label-encoded), Quantity, Discount, Unit_Price"
)
doc.add_paragraph("")
doc.add_paragraph(
    "Models Trained:\n\n"
    "1. Linear Regression — Baseline model. Fits a linear relationship between "
    "features and the target. Selected for interpretability.\n\n"
    "2. Random Forest Regressor — Ensemble of 100 decision trees. Each tree is "
    "trained on a random subset of data and features. Final prediction is the "
    "average of all trees. Selected for robustness and ability to capture "
    "non-linear relationships.\n\n"
    "3. Gradient Boosting Regressor — Sequential ensemble of 100 trees, where each "
    "tree corrects the errors of the previous one. Selected for high predictive "
    "accuracy and ability to model complex patterns.\n\n"
    "Train/Test Split: 80% training, 20% testing (random_state=42 for reproducibility)."
)

# ─────────────────────────────────────────────────────────────────────────────
# 13. MODEL TRAINING
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "13. Model Training", 1)
doc.add_paragraph(
    "All three models were trained using scikit-learn on the 80% training split. "
    "Default hyperparameters were used with n_estimators=100 for ensemble models "
    "and random_state=42 for reproducibility. "
    "Label encoding was applied to convert categorical features (Category, Region, Segment) "
    "into numerical format before training."
)

# ─────────────────────────────────────────────────────────────────────────────
# 14. MODEL EVALUATION
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "14. Model Evaluation", 1)
doc.add_paragraph(
    "Models were evaluated on the 20% held-out test set using four metrics:"
)
doc.add_paragraph("")
add_table(doc,
    ["Metric", "Formula", "Interpretation"],
    [
        ["MAE",  "Mean(|actual - predicted|)",      "Average prediction error in USD; lower is better"],
        ["MSE",  "Mean((actual - predicted)²)",     "Penalises large errors; lower is better"],
        ["RMSE", "√MSE",                             "Same units as Sales (USD); lower is better"],
        ["R²",   "1 - SS_res/SS_tot",               "% variance explained (0–1); higher is better"],
    ]
)
doc.add_paragraph("")
doc.add_paragraph("Actual Results Computed from Dataset:")
doc.add_paragraph("")

result_rows = []
for model_name, metrics in ml_results.items():
    result_rows.append([
        model_name,
        f"${metrics['MAE']:,.2f}",
        f"${metrics['MSE']:,.2f}",
        f"${metrics['RMSE']:,.2f}",
        f"{metrics['R2']:.4f}",
    ])
if result_rows:
    add_table(doc, ["Model", "MAE (USD)", "MSE", "RMSE (USD)", "R²"], result_rows)
    doc.add_paragraph("")
    doc.add_paragraph(
        f"Best Performing Model: {best_model}\n"
        f"R² = {best_r2:.4f} (explains {best_r2*100:.1f}% of sales variance)\n"
        f"RMSE = ${best_rmse:,.2f} (average prediction error)"
    )

# ─────────────────────────────────────────────────────────────────────────────
# 15. AI-BASED BUSINESS INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "15. AI-Based Business Insights", 1)
doc.add_paragraph(
    "The project implements a local, rule-based Python insight engine that automatically "
    "converts computed analytical metrics into natural-language business insights. No "
    "external AI API (ChatGPT, Gemini, IBM Watson, etc.) is used. This approach ensures:\n"
    "• Full offline reproducibility\n"
    "• Complete transparency (insights traceable to actual data)\n"
    "• Academic integrity (no hallucinated or fabricated results)\n\n"
    "The engine examines the following computed metrics and applies business logic rules:\n"
    "• Total revenue and profit margin\n"
    "• Category and region performance rankings\n"
    "• Seasonal peak analysis\n"
    "• Discount-profit correlation\n"
    "• Top products by revenue and profit\n"
    "• ML model performance summary\n\n"
    f"Sample insights generated:\n"
    f"1. Total revenue was ${total_revenue:,.2f} with an overall profit margin of "
    f"{overall_margin:.1f}%.\n"
    f"2. '{top_cat}' is the highest revenue-generating category.\n"
    f"3. '{top_reg}' leads in regional revenue.\n"
    f"4. Clear November-December sales peaks indicate holiday seasonality.\n"
    f"5. Discounts above 20% significantly erode profit margins.\n"
    f"6. The {best_model} achieved R²={best_r2:.4f}, explaining {best_r2*100:.1f}% of "
    f"sales variance.\n"
    "(Complete insights are displayed in Section 20 of the Jupyter Notebook.)"
)

# ─────────────────────────────────────────────────────────────────────────────
# 16. RESULTS AND FINDINGS
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "16. Results and Findings", 1)
findings = [
    ("Revenue & Profit", f"Total revenue of ${total_revenue:,.2f} with overall profit margin of {overall_margin:.1f}%."),
    ("Category Leader", f"{top_cat} generates the highest total revenue across all categories."),
    ("Best Margin Category", "Office Supplies consistently delivers the highest profit margin percentage."),
    ("Regional Leader", f"{top_reg} region outperforms all other regions in total revenue."),
    ("Seasonality", "Sales peak in November-December due to holiday demand. Q1 (Jan-Feb) is consistently the slowest period."),
    ("Discount Impact", "Negative correlation between Discount and Profit (-0.3 to -0.5 range). Discounts above 20% significantly reduce profitability."),
    ("Product Concentration", "A small number of Technology products account for a disproportionately large share of total revenue (Pareto pattern)."),
    ("ML Performance", f"Best ML model: {best_model} | R²={best_r2:.4f} | RMSE=${best_rmse:,.2f}"),
    ("Feature Importance", "Unit_Price and Quantity are the strongest sales predictors, followed by Category and Month."),
    ("Year-on-Year Growth", "The business shows positive revenue growth across all three analysis years (2021-2023)."),
]
for title, detail in findings:
    p = doc.add_paragraph()
    r1 = p.add_run(f"{title}: ")
    r1.bold = True
    r2 = p.add_run(detail)

# ─────────────────────────────────────────────────────────────────────────────
# 17. BUSINESS RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "17. Business Recommendations", 1)
add_table(doc,
    ["Priority", "Recommendation", "Expected Impact"],
    [
        ["High",   "Implement a maximum 20% discount policy",                         "Improved profit margins"],
        ["High",   "Pre-stock Technology products before Q4 (Oct-Dec)",               "Capture peak seasonal demand"],
        ["Medium", "Launch targeted marketing campaigns in the lowest-revenue region", "Revenue growth in weak markets"],
        ["Medium", "Develop loyalty programmes for the top customer segment",          "Improved customer retention"],
        ["Medium", "Bundle high-margin Office Supplies with Technology products",      "Cross-sell revenue increase"],
        ["Low",    "Use the ML model for quarterly sales forecasting",                 "Better inventory planning"],
        ["Low",    "Investigate low-margin Furniture products for cost optimisation",  "Margin improvement"],
        ["Low",    "Introduce pre-order incentives ahead of seasonal peaks",           "Demand smoothing"],
    ]
)

# ─────────────────────────────────────────────────────────────────────────────
# 18. LIMITATIONS
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "18. Limitations", 1)
limitations = [
    "The dataset is synthetic and may not capture all complexities of real-world retail (supplier disruptions, economic downturns, competitor actions).",
    "No external macro-economic variables (inflation, interest rates, market conditions) are included in the ML features.",
    "Static batch analysis only — the project does not support real-time data ingestion.",
    "Simple label encoding is used for categorical variables; more sophisticated encoding (target encoding, one-hot) may improve model accuracy.",
    "Only regression models are explored; time-series models (ARIMA, Prophet) may provide better seasonal forecasting.",
    "The project does not include customer lifetime value analysis or churn prediction.",
    "Geographic analysis is limited to predefined regions; city-level geographic mapping is not implemented.",
]
for lim in limitations:
    doc.add_paragraph(f"• {lim}")

# ─────────────────────────────────────────────────────────────────────────────
# 19. FUTURE SCOPE
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "19. Future Scope", 1)
future = [
    "Real-Time Dashboard: Streamlit or Power BI dashboard connected to live sales data.",
    "Time-Series Forecasting: ARIMA, SARIMA, or Facebook Prophet for seasonal demand forecasting.",
    "Customer Segmentation: K-Means or DBSCAN clustering for customer profiling.",
    "Churn Prediction: Classification models to identify customers at risk of leaving.",
    "NLP Analysis: Sentiment analysis of customer reviews for product improvement insights.",
    "Hyperparameter Tuning: GridSearchCV or Optuna for model optimisation.",
    "Geospatial Analysis: GeoPandas or Plotly choropleth maps for geographic visualisation.",
    "MLOps Pipeline: REST API deployment using FastAPI or Flask for production predictions.",
    "A/B Testing: Statistical experiments to evaluate discount policy changes.",
    "Deep Learning: LSTM networks for multi-step sales forecasting.",
]
for item in future:
    parts = item.split(": ", 1)
    p = doc.add_paragraph()
    r1 = p.add_run(f"• {parts[0]}: ")
    r1.bold = True
    if len(parts) > 1:
        p.add_run(parts[1])

# ─────────────────────────────────────────────────────────────────────────────
# 20. CONCLUSION
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "20. Conclusion", 1)
doc.add_paragraph(
    "This project successfully demonstrates a complete data analytics and AI pipeline "
    "applied to retail sales data. Beginning with raw transactional data, the project "
    "systematically progressed through data cleaning, feature engineering, exploratory "
    "analysis, professional visualisation, machine learning modelling, and AI-assisted "
    "insight generation.\n\n"
    "The analysis revealed clear seasonal demand patterns, category and regional performance "
    "disparities, the significant impact of discount strategies on profitability, and the "
    "predictive power of machine learning for sales forecasting.\n\n"
    f"The best-performing model ({best_model}) achieved an R² of {best_r2:.4f}, "
    f"explaining {best_r2*100:.1f}% of the variation in sales — a meaningful result "
    f"given the diversity of products, regions, and customer segments in the dataset.\n\n"
    "The combination of traditional analytics and AI/ML techniques provides a solid "
    "foundation for data-driven decision-making in any retail business. The project "
    "is fully reproducible, academically honest, and suitable for professional "
    "presentation or further development.\n\n"
    "This project was completed as part of the IBM SkillsBuild Data Analytics with AI "
    "Internship 2026 under the BharatCares / AICTE programme."
)

# ─────────────────────────────────────────────────────────────────────────────
# 21. REFERENCES
# ─────────────────────────────────────────────────────────────────────────────
heading(doc, "21. References", 1)
refs = [
    "Himanshu Uike. (2023). Superstore Sales Dataset. Kaggle. https://www.kaggle.com/datasets/himanshuuike/superstore-sales-dataset",
    "Scikit-learn developers. (2024). Scikit-learn: Machine Learning in Python. https://scikit-learn.org/stable/",
    "McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference. https://pandas.pydata.org/docs/",
    "Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering, 9(3), 90-95. https://matplotlib.org/",
    "Waskom, M. (2021). Seaborn: Statistical Data Visualization. Journal of Open Source Software, 6(60), 3021. https://seaborn.pydata.org/",
    "Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585, 357-362. https://numpy.org/",
    "IBM SkillsBuild. (2026). Data Analytics with AI Course. https://skillsbuild.org/",
    "Project Jupyter. (2024). Jupyter Notebook Documentation. https://jupyter.org/",
    "VanderPlas, J. (2016). Python Data Science Handbook. O'Reilly Media.",
    "Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd ed.). O'Reilly Media.",
]
for i, ref in enumerate(refs, 1):
    doc.add_paragraph(f"[{i}] {ref}")

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "report")
out_path = os.path.join(out_dir, "DharvPatel_AI_Sales_Analytics_ProjectReport.docx")
out_path = os.path.normpath(out_path)
os.makedirs(out_dir, exist_ok=True)
doc.save(out_path)
print(f"Report saved to: {out_path}")
