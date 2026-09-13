"""About page (UI-ABOUT-001)."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_PROJECT_ROOT, _PROJECT_ROOT / "dashboard"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import streamlit as st

from components.sidebar import render_sidebar_branding
from styles.theme import inject_custom_css
from src.services.data_service import load_production_model
from config.settings import PROJECT_NAME, PROJECT_VERSION

st.set_page_config(page_title="About — Delhi AQI", page_icon="ℹ️", layout="wide")
inject_custom_css()
render_sidebar_branding()

st.title("About This Platform")

st.markdown(f"### {PROJECT_NAME}")
st.write(
    "Forecasts Delhi's Air Quality Index from historical CPCB data, and "
    "presents pollution trends, model performance, and health guidance "
    "through this dashboard. Built following a Product Requirements "
    "Document and Master Development Handbook, with every milestone "
    "tested against real data rather than assumed to work."
)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Technology stack")
    st.write(
        "Python · pandas · scikit-learn · Streamlit · Matplotlib/Seaborn "
        "· joblib · reportlab"
    )

    st.markdown("#### Machine learning")
    _, metadata = load_production_model()
    st.write(f"Production model: **{metadata['algorithm']}**")
    st.write(
        "Selected after comparing Linear Regression, Random Forest "
        "(default and tuned), and Gradient Boosting on held-out test "
        "data — see the Model Performance page."
    )

with col2:
    st.markdown("#### Dataset")
    st.write(
        "Delhi AQI, 2018–2024 (CPCB, via `cp099/India-Air-Quality-Dataset`, "
        "CC BY 4.0). Pollutant columns are estimated from AQI by the "
        "source, not independently measured — see the Pollutant Analysis "
        "page and `data/metadata/DATASET_SOURCE.md`."
    )

    st.markdown("#### Known limitations")
    st.write(
        "All of 2022 is missing from the source data (handled explicitly "
        "in feature engineering, not interpolated). Forecasts beyond the "
        "first day compound uncertainty, since they build partly on the "
        "model's own earlier predictions."
    )

st.write("")
st.markdown("#### Project documentation")
st.write(
    "Full methodology, data quality reports, and evaluation results live "
    "in `data/metadata/` and `notebooks/` in the project repository."
)

st.write("")
st.caption(f"Version {PROJECT_VERSION}")
