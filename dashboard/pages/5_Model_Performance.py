"""Model Performance page (UI-MODEL-001)."""

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
from src.services.data_service import (
    PRODUCTION_MODEL_FILENAME,
    load_all_model_metadata,
    load_production_model,
)
from src.models.model_trainer import get_feature_importance

st.set_page_config(page_title="Model Performance — Delhi AQI", page_icon="📈", layout="wide")
inject_custom_css()
render_sidebar_branding()

st.title("Model Performance")
st.caption("All 4 candidates trained in Milestone 4; ranked by validation MAE.")

metadata_by_model = load_all_model_metadata()

rows = []
display_names = {
    "linear_regression_v1": "Linear Regression",
    "random_forest_v1": "Random Forest (default)",
    "random_forest_tuned_v1": "Random Forest (tuned)",
    "gradient_boosting_v1": "Gradient Boosting",
}
for key, meta in metadata_by_model.items():
    m = meta["validation_metrics"]
    rows.append({
        "Model": display_names.get(key, key),
        "MAE": round(m["MAE"], 2),
        "MSE": round(m["MSE"], 2),
        "RMSE": round(m["RMSE"], 2),
        "R²": round(m["R2"], 4),
    })
comparison_df = pd.DataFrame(rows).sort_values("MAE").reset_index(drop=True)

st.markdown("### Model comparison (validation set)")
st.dataframe(comparison_df, use_container_width=True, hide_index=True)
st.bar_chart(comparison_df.set_index("Model")["MAE"], height=300)

winner = comparison_df.iloc[0]
st.success(
    f"**Production model: {winner['Model']}** "
    f"(MAE={winner['MAE']}, R²={winner['R²']}) — see "
    f"`data/metadata/MODEL_EVALUATION_REPORT.md` for the full test-set "
    f"evaluation and why the simplest model won."
)

st.write("")
st.markdown("### Feature importance (production model)")
model, prod_metadata = load_production_model()
importances = get_feature_importance(model, prod_metadata["feature_names"])
top_10 = dict(list(importances.items())[:10])
importance_df = pd.Series(top_10, name="Importance").sort_values(ascending=False)
st.bar_chart(importance_df, height=350)
st.caption(
    "Short-horizon lag features (Lag_1, Lag_3) and short rolling windows "
    "dominate — the model has learned that AQI changes gradually day to day."
)

st.write("")
with st.expander("Production model details"):
    st.write(f"**File:** `models/trained/{PRODUCTION_MODEL_FILENAME}`")
    st.write(f"**Algorithm:** {prod_metadata['algorithm']}")
    st.write(f"**Training rows:** {prod_metadata['training_rows']:,}")
    st.write(f"**Random seed:** {prod_metadata['random_seed']}")
    st.write(f"**Features used:** {len(prod_metadata['feature_names'])}")
    st.code(", ".join(prod_metadata["feature_names"]), language=None)
