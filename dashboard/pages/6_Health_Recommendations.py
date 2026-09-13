"""Health Recommendations page (UI-HEALTH-001)."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_PROJECT_ROOT, _PROJECT_ROOT / "dashboard"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import streamlit as st

from components.aqi_badge import render_aqi_badge
from components.sidebar import render_sidebar_branding
from styles.theme import inject_custom_css
from src.services.data_service import load_cleaned_dataset
from src.services.health_service import disclaimer, get_health_recommendation, get_recommendation_for_aqi
from config.constants import AQI_CATEGORIES

st.set_page_config(page_title="Health Recommendations — Delhi AQI", page_icon="🩺", layout="wide")
inject_custom_css()
render_sidebar_branding()

st.title("Health Recommendations")
st.caption(disclaimer)

df = load_cleaned_dataset().sort_values("Date")
latest = df.iloc[-1]
current_rec = get_recommendation_for_aqi(latest["AQI"])

st.markdown("### Today's guidance")
if current_rec:
    col1, col2 = st.columns([1, 3])
    with col1:
        render_aqi_badge(current_rec["category"])
        st.caption(f"AQI {latest['AQI']:.0f} · range {current_rec['aqi_range']}")
    with col2:
        st.write(current_rec["description"])
        st.write(f"**Health risk:** {current_rec['health_risk']}")
        st.write(f"**Outdoor activity:** {current_rec['outdoor_recommendation']}")
        st.write(f"**Safety advice:** {current_rec['safety_advice']}")

st.write("")
st.markdown("### Check guidance for any AQI value")
user_aqi = st.slider("AQI value", min_value=0, max_value=500, value=int(latest["AQI"]))
rec = get_recommendation_for_aqi(user_aqi)
if rec:
    render_aqi_badge(rec["category"])
    st.write(rec["description"])
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Health risk:** {rec['health_risk']}")
        st.write(f"**Outdoor activity:** {rec['outdoor_recommendation']}")
    with col2:
        st.write(f"**Safety advice:** {rec['safety_advice']}")

st.write("")
st.markdown("### All AQI categories")
for cat in AQI_CATEGORIES:
    guidance = get_health_recommendation(cat["label"])
    with st.expander(f"{cat['label']} ({cat['min']}–{cat['max']})"):
        render_aqi_badge(cat["label"], size="small")
        st.write(guidance["description"])
        st.write(f"**Health risk:** {guidance['health_risk']}")
        st.write(f"**Outdoor activity:** {guidance['outdoor_recommendation']}")
        st.write(f"**Safety advice:** {guidance['safety_advice']}")
