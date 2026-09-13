"""Dataset Overview page (UI-DATA-001)."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_PROJECT_ROOT, _PROJECT_ROOT / "dashboard"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import pandas as pd
import streamlit as st

from components.sidebar import render_sidebar_branding
from styles.theme import COLORS, inject_custom_css
from src.preprocessing.data_validator import validate_dataset
from src.services.data_service import load_cleaned_dataset
from config.constants import REQUIRED_DATASET_COLUMNS

st.set_page_config(page_title="Dataset Overview — Delhi AQI", page_icon="📋", layout="wide")
inject_custom_css()
render_sidebar_branding()

st.title("Dataset Overview")
st.caption(
    "The cleaned dataset behind every page in this dashboard. "
    "See the About page for full provenance and licensing."
)

df = load_cleaned_dataset()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Rows", f"{len(df):,}")
with col2:
    st.metric("Columns", df.shape[1])
with col3:
    st.metric("Date range (days)", f"{(df['Date'].max() - df['Date'].min()).days:,}")
with col4:
    st.metric("Cities", df["City"].nunique())

st.write("")
st.markdown("### Data quality (FR-DATA-002)")
report = validate_dataset(df, REQUIRED_DATASET_COLUMNS)
status_color = COLORS["leaf"] if report.is_valid else COLORS["haze"]
st.markdown(
    f"<span style='color:{status_color}; font-weight:600;'>"
    f"{'✓ VALID' if report.is_valid else '✗ INVALID'}</span> — "
    f"{report.duplicate_row_count} duplicate rows, "
    f"{sum(1 for v in report.missing_value_percentages.values() if v > 0)} "
    f"columns with any missing values.",
    unsafe_allow_html=True,
)

st.write("")
st.markdown("### Column types")
dtype_df = pd.DataFrame({
    "Column": df.columns,
    "Type": [str(t) for t in df.dtypes],
    "Missing %": [report.missing_value_percentages.get(c, 0.0) for c in df.columns],
})
st.dataframe(dtype_df, use_container_width=True, hide_index=True)

st.write("")
st.markdown("### Statistical summary")
st.caption(
    "Note: PM2.5–O3 are estimated from AQI in the source data, not independent "
    "measurements — see the Pollutant Analysis page for details."
)
st.dataframe(df.describe().round(1), use_container_width=True)

st.write("")
st.markdown("### Preview")
tab1, tab2 = st.tabs(["First 10 records", "Last 10 records"])
with tab1:
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
with tab2:
    st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
