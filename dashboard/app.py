"""
Home page — AQI Forecast & Environmental Analytics Platform dashboard
(FR-DASH-001, UI-HOME-001).

Streamlit entry point: run with `streamlit run dashboard/app.py`.

Per Handbook Section 5.6, this file contains presentation logic only --
data loading, forecasting, and health lookups all go through
`src/services/`, never reimplemented here.
"""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
for _p in (_PROJECT_ROOT, _PROJECT_ROOT / "dashboard"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import streamlit as st

from components.aqi_badge import render_aqi_badge
from components.kpi import render_hero_metric, render_supporting_panel
from components.sidebar import render_sidebar_branding
from styles.theme import inject_custom_css
from src.services.data_service import load_cleaned_dataset, load_production_model
from src.services.forecast_service import generate_future_forecast
from src.services.health_service import get_recommendation_for_aqi

st.set_page_config(page_title="Delhi AQI Forecast", page_icon="🌤️", layout="wide")
inject_custom_css()
render_sidebar_branding()


@st.cache_data
def _get_data():
    return load_cleaned_dataset()


@st.cache_resource
def _get_model():
    return load_production_model()


df = _get_data()
model, metadata = _get_model()
df_sorted = df.sort_values("Date")
latest = df_sorted.iloc[-1]

current_aqi = latest["AQI"]
recommendation = get_recommendation_for_aqi(current_aqi)
current_category = recommendation["category"] if recommendation else None

st.title("Delhi Air Quality")
st.caption(
    "Historical analytics and forecasting built on CPCB AQI data, "
    f"2018–2024. Latest recorded day: {latest['Date'].strftime('%d %B %Y')}."
)

render_hero_metric(
    value=f"{current_aqi:.0f}",
    label=f"Current AQI — {latest['Date'].strftime('%d %b %Y')}",
    category=current_category,
)
if current_category:
    render_aqi_badge(current_category)

st.write("")
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_supporting_panel("7-Day Average", f"{df_sorted.tail(7)['AQI'].mean():.0f}")
with col2:
    render_supporting_panel("All-Time High", f"{df['AQI'].max():.0f}")
with col3:
    render_supporting_panel("All-Time Low", f"{df['AQI'].min():.0f}")
with col4:
    try:
        tomorrow = generate_future_forecast(
            model, df, metadata["feature_names"], horizon_days=1
        ).iloc[0]
        render_supporting_panel(
            "Tomorrow's Forecast",
            f"{tomorrow['Predicted_AQI']:.0f}",
            tomorrow["Predicted_AQI_Category"],
        )
    except ValueError:
        render_supporting_panel("Tomorrow's Forecast", "—", "unavailable")

st.write("")
st.markdown("### Recent trend")
st.caption("Last 90 days of recorded AQI.")
recent = df_sorted.tail(90).set_index("Date")["AQI"]
st.line_chart(recent, height=300)

st.write("")
st.markdown("### About this platform")
st.write(
    "This dashboard forecasts Delhi's Air Quality Index using historical "
    "CPCB data and a Linear Regression model selected after comparing it "
    "against Random Forest and Gradient Boosting on held-out test data "
    "(see the Model Performance page). Use the sidebar to explore the "
    "dataset, historical trends, pollutant behavior, forecasts, and "
    "health guidance."
)
