"""AQI category badge -- a colored pill used wherever a category appears."""

from dashboard.styles.theme import get_category_color


def render_aqi_badge(category: str, size: str = "normal"):
    """
    Render a colored pill badge for an AQI category. Reuses the same
    functional color scale as the hero metric and everywhere else a
    category appears -- one consistent color system throughout, not a
    per-page choice.

    Parameters
    ----------
    category : str
        An AQI category label (config.constants.AQI_CATEGORIES).
    size : str, default "normal"
        "small" for inline/sidebar use, "normal" for page content.
    """
    import streamlit as st

    color = get_category_color(category)
    padding = "0.15rem 0.7rem" if size == "small" else "0.35rem 1rem"
    font_size = "0.8rem" if size == "small" else "0.95rem"

    st.markdown(
        f"""
        <span style="background-color:{color}1A; color:{color};
                     border:1.5px solid {color}; border-radius:999px;
                     padding:{padding}; font-family:'Inter',sans-serif;
                     font-weight:600; font-size:{font_size};
                     display:inline-block;">
            {category}
        </span>
        """,
        unsafe_allow_html=True,
    )
