"""Exploratory Data Analysis page (UI-EDA-001)."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_PROJECT_ROOT, _PROJECT_ROOT / "dashboard"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from components.sidebar import render_sidebar_branding
from styles.theme import COLORS, inject_custom_css
from src.services.data_service import load_cleaned_dataset
from config.constants import REQUIRED_POLLUTANT_COLUMNS

st.set_page_config(page_title="EDA — Delhi AQI", page_icon="📊", layout="wide")
inject_custom_css()
render_sidebar_branding()

st.title("Exploratory Data Analysis")
st.caption("Interactive version of the analysis in notebooks/03_exploratory_data_analysis.ipynb.")

df = load_cleaned_dataset().sort_values("Date")
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

plt.rcParams["figure.facecolor"] = COLORS["bg"]
plt.rcParams["axes.facecolor"] = COLORS["bg"]

tab1, tab2, tab3, tab4 = st.tabs(
    ["Distribution & Trend", "Correlation", "Seasonality", "Outliers"]
)

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**AQI Distribution**")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(df["AQI"], bins=40, color=COLORS["sky"], edgecolor="white")
        ax.axvline(df["AQI"].mean(), color=COLORS["haze"], linestyle="--", label="Mean")
        ax.set_xlabel("AQI")
        ax.set_ylabel("Days")
        ax.legend()
        st.pyplot(fig)
        st.caption(f"Right-skewed (skew={df['AQI'].skew():.2f}) — most days cluster in Moderate–Unhealthy.")

    with col2:
        st.markdown("**Historical Trend**")
        st.line_chart(df.set_index("Date")["AQI"], height=320)
        st.caption("Strong annual seasonal cycle — winter peaks, monsoon troughs.")

with tab2:
    st.markdown("**Correlation Heatmap**")
    corr_cols = ["AQI"] + list(REQUIRED_POLLUTANT_COLUMNS)
    corr = df[corr_cols].corr()
    fig, ax = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, square=True, ax=ax)
    st.pyplot(fig)
    st.warning(
        "Every correlation here is 1.00 — pollutant columns are exact linear "
        "transforms of AQI in this dataset (confirmed: PM2.5 = 0.55 × AQI, always). "
        "They are shown for context only and are never used as model input "
        "features. See Pollutant Analysis and the About page for details."
    )

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Average AQI by Month**")
        month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        monthly_avg = df.groupby("Month")["AQI"].mean().reindex(range(1, 13))
        monthly_avg.index = month_names
        st.bar_chart(monthly_avg, height=320)
    with col2:
        st.markdown("**AQI Distribution by Year**")
        fig, ax = plt.subplots(figsize=(6, 4))
        df.boxplot(column="AQI", by="Year", ax=ax)
        plt.suptitle("")
        ax.set_xlabel("Year")
        ax.set_ylabel("AQI")
        st.pyplot(fig)
    st.caption(
        "Winter months (Nov–Jan) are consistently worst; no strong multi-year "
        "improving/worsening trend visible."
    )

with tab4:
    st.markdown("**PM2.5 vs. AQI — visual proof of the collinearity finding**")
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(df["AQI"], df["PM2.5"], s=6, alpha=0.5, color=COLORS["sky"])
    ax.set_xlabel("AQI")
    ax.set_ylabel("PM2.5")
    st.pyplot(fig)
    st.caption("A perfectly straight line, not a cloud of points — PM2.5 is a deterministic function of AQI here.")
