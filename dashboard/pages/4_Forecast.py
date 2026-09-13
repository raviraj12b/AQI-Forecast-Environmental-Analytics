"""Forecast page (UI-FORECAST-001 / FR-FORECAST-001/002)."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_PROJECT_ROOT, _PROJECT_ROOT / "dashboard"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import pandas as pd
import streamlit as st

from components.aqi_badge import render_aqi_badge
from components.kpi import render_hero_metric
from components.sidebar import render_sidebar_branding
from styles.theme import COLORS, inject_custom_css
from src.services.data_service import load_cleaned_dataset, load_production_model
from src.services.forecast_service import generate_future_forecast

st.set_page_config(page_title="Forecast — Delhi AQI", page_icon="🔮", layout="wide")
inject_custom_css()
render_sidebar_branding()

st.title("AQI Forecast")
st.caption(
    "Recursive day-by-day forecasting — each day's prediction feeds the "
    "next day's inputs, since real future data doesn't exist yet."
)

df = load_cleaned_dataset()
model, metadata = load_production_model()

horizon_choice = st.radio(
    "Forecast horizon", ["Next day", "Next week", "Custom"], horizontal=True
)
if horizon_choice == "Next day":
    horizon_days = 1
elif horizon_choice == "Next week":
    horizon_days = 7
else:
    horizon_days = st.slider("Days ahead", min_value=1, max_value=14, value=7)

try:
    forecast = generate_future_forecast(
        model, df, metadata["feature_names"], horizon_days=horizon_days
    )
except ValueError as e:
    st.error(f"Could not generate a forecast: {e}")
    st.stop()

first_day = forecast.iloc[0]
render_hero_metric(
    value=f"{first_day['Predicted_AQI']:.0f}",
    label=f"Predicted AQI — {pd.Timestamp(first_day['Date']).strftime('%d %b %Y')}",
    category=first_day["Predicted_AQI_Category"],
)
render_aqi_badge(first_day["Predicted_AQI_Category"])
st.caption(f"Confidence: {first_day['ConfidenceLabel']}")

st.write("")
st.markdown("### Forecast chart")
st.caption("Last 30 recorded days (solid) plus the forecast horizon (dashed).")

history_tail = df.sort_values("Date").tail(30)[["Date", "AQI"]].rename(columns={"AQI": "Historical"})
forecast_for_chart = forecast[["Date", "Predicted_AQI"]].rename(columns={"Predicted_AQI": "Forecast"})
chart_df = pd.merge(history_tail, forecast_for_chart, on="Date", how="outer").set_index("Date")
st.line_chart(chart_df, height=350)

st.write("")
st.markdown("### Forecast table")
display_table = forecast.copy()
display_table["Date"] = pd.to_datetime(display_table["Date"]).dt.strftime("%d %b %Y")
st.dataframe(
    display_table[["Date", "Predicted_AQI", "Predicted_AQI_Category", "ConfidenceLabel"]],
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Confidence decreases with horizon (High → Medium → Low) because each "
    "day beyond the first is partly built on the model's own earlier "
    "predictions, not independent measurements. This is a labeled "
    "heuristic, not a statistical confidence interval."
)
