"""
analysis.py
===========
Reusable helper functions for the AI-Powered Sales Data Analytics project.

These functions are used inside the Jupyter Notebook and can also be called
independently for scripted analysis.

Author : Dharv Patel
Project: AI-Powered Sales Data Analytics and Business Insights
Program: IBM SkillsBuild Data Analytics with AI Internship 2026
"""

from __future__ import annotations

import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore")

# ── Styling ───────────────────────────────────────────────────────────────────
PALETTE = "viridis"
FIGURE_SIZE = (12, 5)
sns.set_theme(style="whitegrid", palette=PALETTE)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING & INSPECTION
# ═══════════════════════════════════════════════════════════════════════════════

def load_data(path: str) -> pd.DataFrame:
    """Load the CSV dataset and return a DataFrame."""
    df = pd.read_csv(path, parse_dates=["Order_Date", "Ship_Date"])
    print(f"✅ Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def inspect_data(df: pd.DataFrame) -> None:
    """Print a structured inspection of the DataFrame."""
    print("=" * 60)
    print("DATASET INSPECTION")
    print("=" * 60)
    print(f"\n📐 Shape       : {df.shape}")
    print(f"\n📋 Columns     :\n{list(df.columns)}")
    print(f"\n🔎 Data Types  :\n{df.dtypes}")
    print(f"\n📊 First 5 rows:\n{df.head()}")
    print(f"\n❓ Missing Values:\n{df.isnull().sum()}")
    print(f"\n🔁 Duplicates  : {df.duplicated().sum()}")
    print(f"\n📈 Statistics  :\n{df.describe(include='all')}")


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns for time-based and financial analysis."""
    df = df.copy()
    df["Year"]           = df["Order_Date"].dt.year
    df["Month"]          = df["Order_Date"].dt.month
    df["Month_Name"]     = df["Order_Date"].dt.strftime("%b")
    df["Quarter"]        = df["Order_Date"].dt.quarter
    df["Profit_Margin"]  = (df["Profit"] / df["Sales"].replace(0, np.nan) * 100).round(2)
    df["Discount_Amount"] = (df["Unit_Price"] * df["Quantity"] * df["Discount"]).round(2)
    df["Revenue"]        = df["Sales"]           # alias for clarity
    return df


# ═══════════════════════════════════════════════════════════════════════════════
# KPI SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

def compute_kpis(df: pd.DataFrame) -> dict:
    """Return a dict of key business KPIs."""
    kpis = {
        "Total Revenue ($)":        round(df["Sales"].sum(), 2),
        "Total Profit ($)":         round(df["Profit"].sum(), 2),
        "Total Orders":             df["Order_ID"].nunique(),
        "Total Quantity Sold":      int(df["Quantity"].sum()),
        "Average Order Value ($)":  round(df["Sales"].mean(), 2),
        "Average Profit ($)":       round(df["Profit"].mean(), 2),
        "Average Discount (%)":     round(df["Discount"].mean() * 100, 2),
        "Overall Profit Margin (%)": round(df["Profit"].sum() / df["Sales"].sum() * 100, 2),
    }
    return kpis


def print_kpis(kpis: dict) -> None:
    print("\n" + "=" * 45)
    print("         KEY PERFORMANCE INDICATORS")
    print("=" * 45)
    for k, v in kpis.items():
        print(f"  {k:<32}: {v:>12,}")
    print("=" * 45)


# ═══════════════════════════════════════════════════════════════════════════════
# VISUALISATION HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def fmt_millions(x, _):
    """Axis formatter for large numbers."""
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"${x/1_000:.0f}K"
    return f"${x:.0f}"


def plot_monthly_trend(df: pd.DataFrame, col: str = "Sales", title: str = "Monthly Sales Trend"):
    monthly = (
        df.groupby(["Year", "Month"])[col]
        .sum()
        .reset_index()
        .sort_values(["Year", "Month"])
    )
    monthly["Period"] = monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str).str.zfill(2)

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    ax.plot(monthly["Period"], monthly[col], marker="o", linewidth=2, color="#2196F3")
    ax.fill_between(range(len(monthly)), monthly[col], alpha=0.15, color="#2196F3")
    ax.set_title(title, fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Period (Year-Month)", fontsize=11)
    ax.set_ylabel(col, fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    plt.xticks(range(len(monthly)), monthly["Period"], rotation=60, fontsize=8)
    plt.tight_layout()
    return fig


def plot_bar(data: pd.Series, title: str, xlabel: str, ylabel: str,
             color: str = "#4CAF50", horizontal: bool = False):
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    if horizontal:
        data.plot(kind="barh", ax=ax, color=color, edgecolor="white")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    else:
        data.plot(kind="bar", ax=ax, color=color, edgecolor="white")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=30, ha="right")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)
    plt.tight_layout()
    return fig


def plot_scatter(df: pd.DataFrame, x: str, y: str, hue: str,
                 title: str, xlabel: str, ylabel: str):
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    for cat in df[hue].unique():
        sub = df[df[hue] == cat]
        ax.scatter(sub[x], sub[y], label=cat, alpha=0.55, s=30)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(title=hue, fontsize=9)
    plt.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# MACHINE LEARNING
# ═══════════════════════════════════════════════════════════════════════════════

def prepare_ml_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Encode categorical features and return X, y for sales prediction.
    Target: Sales
    Features: Month, Quarter, Year, Category, Region, Segment, Quantity, Discount, Unit_Price
    """
    ml_df = df[["Month", "Quarter", "Year", "Category", "Region",
                "Segment", "Quantity", "Discount", "Unit_Price", "Sales"]].copy()

    # Encode categoricals
    le = LabelEncoder()
    for col in ["Category", "Region", "Segment"]:
        ml_df[col] = le.fit_transform(ml_df[col].astype(str))

    X = ml_df.drop("Sales", axis=1)
    y = ml_df["Sales"]
    return X, y


def train_evaluate_models(X: pd.DataFrame, y: pd.Series,
                          test_size: float = 0.2,
                          random_state: int = 42) -> pd.DataFrame:
    """
    Train LinearRegression, RandomForestRegressor, and GradientBoostingRegressor.
    Return a comparison DataFrame and fitted models.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    models = {
        "Linear Regression":          LinearRegression(),
        "Random Forest Regressor":    RandomForestRegressor(n_estimators=100, random_state=random_state),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, random_state=random_state),
    }

    results = []
    fitted = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae  = mean_absolute_error(y_test, y_pred)
        mse  = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2   = r2_score(y_test, y_pred)

        results.append({"Model": name, "MAE": round(mae, 2),
                        "MSE": round(mse, 2), "RMSE": round(rmse, 2), "R²": round(r2, 4)})
        fitted[name] = (model, X_test, y_test, y_pred)

    return pd.DataFrame(results), fitted


# ═══════════════════════════════════════════════════════════════════════════════
# AI-BASED RULE INSIGHT ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def generate_insights(df: pd.DataFrame, kpis: dict) -> list[str]:
    """
    Rule-based insight engine: inspects actual computed metrics and generates
    natural-language business insights.

    This is a local, deterministic, API-free approach — no external LLM is used.
    """
    insights = []

    # ── Revenue & Profit ────────────────────────────────────────────────────
    total_rev    = kpis["Total Revenue ($)"]
    total_profit = kpis["Total Profit ($)"]
    margin       = kpis["Overall Profit Margin (%)"]

    insights.append(f"📊 The business generated total revenue of ${total_rev:,.2f} "
                    f"with an overall profit margin of {margin:.1f}%.")

    if margin < 10:
        insights.append("⚠️  Overall profit margin is below 10%. "
                        "Cost reduction and pricing strategy review are recommended.")
    elif margin < 20:
        insights.append("✅ Profit margin is moderate (10–20%). "
                        "Optimising high-discount products could improve profitability.")
    else:
        insights.append("🌟 Excellent profit margin (>20%) indicates healthy pricing and cost control.")

    # ── Top category ────────────────────────────────────────────────────────
    cat_rev = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    top_cat = cat_rev.index[0]
    insights.append(f"🏆 '{top_cat}' is the highest revenue-generating category "
                    f"(\${cat_rev.iloc[0]:,.2f}), making it the primary revenue driver.")

    cat_margin = (df.groupby("Category")["Profit"].sum() /
                  df.groupby("Category")["Sales"].sum() * 100).round(2)
    best_margin_cat = cat_margin.idxmax()
    insights.append(f"💰 '{best_margin_cat}' has the best profit margin "
                    f"({cat_margin.max():.1f}%) among all categories.")

    # ── Top region ──────────────────────────────────────────────────────────
    reg_rev = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    top_reg = reg_rev.index[0]
    insights.append(f"📍 '{top_reg}' region leads in total revenue "
                    f"(\${reg_rev.iloc[0]:,.2f}). Maintaining strong presence here is critical.")

    weak_reg = reg_rev.index[-1]
    insights.append(f"📉 '{weak_reg}' is the weakest region by revenue "
                    f"(\${reg_rev.iloc[-1]:,.2f}). Targeted marketing could boost performance.")

    # ── Seasonal pattern ────────────────────────────────────────────────────
    monthly_sales = df.groupby("Month")["Sales"].sum()
    peak_month    = monthly_sales.idxmax()
    month_names   = {1: "January", 2: "February", 3: "March", 4: "April",
                     5: "May", 6: "June", 7: "July", 8: "August",
                     9: "September", 10: "October", 11: "November", 12: "December"}
    insights.append(f"📅 Sales peak in {month_names[peak_month]} "
                    f"(\${monthly_sales[peak_month]:,.2f}). "
                    "Inventory and staffing should be planned for seasonal demand.")

    # ── Discount effect ─────────────────────────────────────────────────────
    high_disc = df[df["Discount"] >= 0.3]
    if len(high_disc) > 0:
        avg_profit_high_disc = high_disc["Profit"].mean()
        avg_profit_overall   = df["Profit"].mean()
        if avg_profit_high_disc < avg_profit_overall * 0.7:
            insights.append("🔻 Products with ≥30% discount show significantly lower profit "
                            "on average. Discount policy should be reviewed to protect margins.")
        else:
            insights.append("ℹ️  High discounts (≥30%) are offered but their profit impact is manageable.")

    # ── Top products ────────────────────────────────────────────────────────
    prod_rev = df.groupby("Product_Name")["Sales"].sum().sort_values(ascending=False)
    top_prod = prod_rev.index[0]
    insights.append(f"⭐ Top revenue product: '{top_prod}' (\${prod_rev.iloc[0]:,.2f}). "
                    "Ensure consistent availability and stock management.")

    prod_profit = df.groupby("Product_Name")["Profit"].sum().sort_values(ascending=False)
    top_profit_prod = prod_profit.index[0]
    insights.append(f"💎 Top profit product: '{top_profit_prod}' (\${prod_profit.iloc[0]:,.2f}). "
                    "This product should be prioritised in marketing campaigns.")

    # ── Segment insight ─────────────────────────────────────────────────────
    seg_rev = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
    top_seg = seg_rev.index[0]
    insights.append(f"👥 '{top_seg}' segment is the biggest revenue contributor "
                    f"(\${seg_rev.iloc[0]:,.2f}). Loyalty programmes could further increase retention.")

    # ── Ship mode ────────────────────────────────────────────────────────────
    ship_cnt = df["Ship_Mode"].value_counts()
    top_ship = ship_cnt.index[0]
    insights.append(f"🚚 '{top_ship}' is the most commonly used shipping mode "
                    f"({ship_cnt.iloc[0]:,} orders). "
                    "Negotiating better rates with this carrier could reduce operational costs.")

    return insights
