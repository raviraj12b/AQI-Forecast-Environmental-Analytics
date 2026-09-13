"""Pollutant Analysis page (UI-POLL-001 / FR-EDA-006)."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_PROJECT_ROOT, _PROJECT_ROOT / "dashboard"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import matplotlib.pyplot as plt
import streamlit as st

from components.sidebar import render_sidebar_branding
from styles.theme import COLORS, inject_custom_css
from src.services.data_service import load_cleaned_dataset
from config.constants import REQUIRED_POLLUTANT_COLUMNS

st.set_page_config(page_title="Pollutant Analysis — Delhi AQI", page_icon="🧪", layout="wide")
inject_custom_css()
render_sidebar_branding()

st.title("Pollutant Analysis")
st.info(
    "**Important context:** in this dataset, PM2.5/PM10/NO2/SO2/CO/O3 were "
    "mathematically estimated from AQI by the data source, not independently "
    "measured (confirmed: e.g. PM2.5 = 0.55 × AQI, always). This page shows "
    "them for reference and context only — they carry no information beyond "
    "AQI itself, and are never used as model input features. "
    "See the About page for full source details."
)

df = load_cleaned_dataset().sort_values("Date")
df["Month"] = df["Date"].dt.month

pollutant = st.selectbox("Select a pollutant", REQUIRED_POLLUTANT_COLUMNS)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(f"Average {pollutant}", f"{df[pollutant].mean():.2f}")
with col2:
    st.metric(f"Maximum {pollutant}", f"{df[pollutant].max():.2f}")
with col3:
    st.metric(f"Minimum {pollutant}", f"{df[pollutant].min():.2f}")

st.write("")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**{pollutant} — Historical Trend**")
    st.line_chart(df.set_index("Date")[pollutant], height=320)

with col2:
    st.markdown(f"**{pollutant} — Distribution**")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df[pollutant], bins=30, color=COLORS["sky"], edgecolor="white")
    ax.set_xlabel(pollutant)
    ax.set_ylabel("Days")
    st.pyplot(fig)

st.write("")
st.markdown(f"**{pollutant} — Average by Month**")
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_avg = df.groupby("Month")[pollutant].mean().reindex(range(1, 13))
monthly_avg.index = month_names
st.bar_chart(monthly_avg, height=300)
