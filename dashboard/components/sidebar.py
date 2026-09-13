"""
Shared sidebar branding, called from every page (Streamlit multipage apps
execute each page independently, so sidebar content isn't automatically
shared -- this small function is called once per page rather than
duplicating its contents).
"""

from dashboard.styles.theme import COLORS


def render_sidebar_branding():
    import streamlit as st

    from src.services.data_service import load_cleaned_dataset
    from src.services.health_service import get_recommendation_for_aqi

    st.sidebar.markdown(
        f"""
        <div style="font-family:'Sora',sans-serif; font-weight:700;
                    font-size:1.3rem; color:{COLORS['ink']}; margin-bottom:0.1rem;">
            🌤️ Delhi AQI
        </div>
        <div style="font-family:'Inter',sans-serif; font-size:0.8rem;
                    color:{COLORS['ink']}; opacity:0.65; margin-bottom:1rem;">
            Forecast & Environmental Analytics
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        df = load_cleaned_dataset()
        latest = df.sort_values("Date").iloc[-1]
        rec = get_recommendation_for_aqi(latest["AQI"])
        if rec:
            from dashboard.components.aqi_badge import render_aqi_badge

            with st.sidebar:
                st.caption(f"Latest reading · {latest['Date'].strftime('%d %b %Y')}")
                render_aqi_badge(rec["category"], size="small")
    except Exception:
        pass  # Sidebar branding is a nice-to-have; a data issue shouldn't block the page.

    st.sidebar.markdown("---")
