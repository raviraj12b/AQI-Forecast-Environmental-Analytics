"""
"Clear Sky" visual theme for the AQI Forecast & Environmental Analytics
Platform dashboard.

Design principle: the AQI health-category colors are the dashboard's
actual functional color system, not decoration -- the same six colors
that mean "Good" or "Hazardous" in the data are reused everywhere a
category appears (badges, hero numbers, chart series).

Two layers, deliberately separated by risk:
1. `.streamlit/config.toml` -- the documented, stable Streamlit theming
   API. Guarantees bright/light base colors regardless of Streamlit
   version, independent of anything below.
2. `CUSTOM_CSS` here -- fonts and a handful of enhancements, injected via
   `st.markdown(..., unsafe_allow_html=True)`. This could not be executed
   and visually verified in the development environment (Streamlit isn't
   installed there -- see project CHANGELOG), so it deliberately targets
   only long-stable `data-testid` selectors and otherwise relies on
   self-contained custom HTML components (`dashboard/components/`) rather
   than fighting Streamlit's internal styling.
"""

# Base palette -- 6 named tokens (design plan)
COLORS = {
    "bg": "#FAFCFF",
    "ink": "#17263B",
    "sky": "#2D7DD2",
    "mist": "#EAF1F8",
    "leaf": "#3FA34D",
    "haze": "#E85D4C",
}

# The AQI category scale, reused functionally throughout the dashboard.
# Keys match config.constants.AQI_CATEGORIES labels exactly.
AQI_CATEGORY_COLORS = {
    "Good": "#3FA34D",
    "Moderate": "#F2C14E",
    "Unhealthy for Sensitive Groups": "#F2994A",
    "Unhealthy": "#E85D4C",
    "Very Unhealthy": "#A855C9",
    "Hazardous": "#7A2E3A",
}


def get_category_color(category: str) -> str:
    """Return the theme color for an AQI category, defaulting to ink if unrecognized."""
    return AQI_CATEGORY_COLORS.get(category, COLORS["ink"])


CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

h1, h2, h3, [data-testid="stSidebarNav"] a {{
    font-family: 'Sora', sans-serif !important;
    font-weight: 600;
    color: {COLORS["ink"]};
}}

/* Sidebar: mist background, matches the design plan's panel color */
[data-testid="stSidebar"] {{
    background-color: {COLORS["mist"]};
}}

/* st.metric widgets: quieter than Streamlit's default, Inter for the numeral */
[data-testid="stMetric"] {{
    background-color: {COLORS["mist"]};
    border-radius: 10px;
    padding: 1rem;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Inter', sans-serif;
    color: {COLORS["ink"]};
}}
[data-testid="stMetricLabel"] {{
    font-family: 'Inter', sans-serif;
    color: {COLORS["ink"]};
    opacity: 0.7;
}}

/* Primary buttons: sky accent */
button[kind="primary"] {{
    background-color: {COLORS["sky"]};
    border-color: {COLORS["sky"]};
}}
</style>
"""


def inject_custom_css():
    """
    Call once near the top of every page: `inject_custom_css()`.
    Deferred import of streamlit so this module (and its color constants)
    remain importable and testable without Streamlit installed.
    """
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
