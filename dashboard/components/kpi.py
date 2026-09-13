"""
KPI display components for the AQI Forecast & Environmental Analytics
Platform dashboard.

Self-contained HTML/CSS (not dependent on Streamlit's internal class
names) so these render identically regardless of Streamlit version --
important since this couldn't be visually verified in the development
environment (Streamlit isn't installed there).
"""

from dashboard.styles.theme import COLORS, get_category_color


def render_hero_metric(value: str, label: str, category: str = None):
    """
    The one big, unboxed number per page (design plan: "one hero per
    page"). If `category` is given (an AQI category label), the number is
    colored by it -- a live, functional use of the AQI color scale, not
    decoration.

    Parameters
    ----------
    value : str
        The large display value, e.g. "271" or "Very Unhealthy".
    label : str
        Small supporting label beneath the value, e.g. "Current AQI in Delhi".
    category : str, optional
        An AQI category label (see config.constants.AQI_CATEGORIES) to
        color the hero number by.
    """
    import streamlit as st

    color = get_category_color(category) if category else COLORS["sky"]
    st.markdown(
        f"""
        <div style="padding: 0.5rem 0 1.5rem 0;">
            <div style="font-family:'Sora',sans-serif; font-weight:700;
                        font-size:4.5rem; line-height:1; color:{color};">
                {value}
            </div>
            <div style="font-family:'Inter',sans-serif; font-size:1.05rem;
                        color:{COLORS['ink']}; opacity:0.75; margin-top:0.4rem;">
                {label}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_supporting_panel(label: str, value: str, sublabel: str = ""):
    """
    A quieter supporting metric panel (mist background) -- deliberately
    smaller and less prominent than the hero, not a duplicate of it in a
    4-up identical-card grid.
    """
    import streamlit as st

    sub_html = (
        f"<div style='font-size:0.8rem; color:{COLORS['ink']}; "
        f"opacity:0.6; margin-top:0.2rem;'>{sublabel}</div>"
        if sublabel
        else ""
    )
    st.markdown(
        f"""
        <div style="background-color:{COLORS['mist']}; border-radius:10px;
                    padding:1rem 1.2rem;">
            <div style="font-family:'Inter',sans-serif; font-size:0.85rem;
                        color:{COLORS['ink']}; opacity:0.7;">
                {label}
            </div>
            <div style="font-family:'Sora',sans-serif; font-weight:600;
                        font-size:1.6rem; color:{COLORS['ink']}; margin-top:0.2rem;">
                {value}
            </div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
