"""Reports & Export page (UI-REPORT-001 / FR-REPORT-001/002)."""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_PROJECT_ROOT, _PROJECT_ROOT / "dashboard"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import pandas as pd
import streamlit as st

from components.sidebar import render_sidebar_branding
from styles.theme import inject_custom_css
from src.services.data_service import load_all_model_metadata, load_cleaned_dataset, load_production_model
from src.services.forecast_service import generate_future_forecast
from src.services.report_service import export_dataframe_to_csv, export_summary_to_pdf
from config.paths import EXPORTS_DIR, REPORTS_DIR

st.set_page_config(page_title="Reports — Delhi AQI", page_icon="📄", layout="wide")
inject_custom_css()
render_sidebar_branding()

st.title("Reports & Export")
st.caption("Generate and download reports from the current data and model.")

df = load_cleaned_dataset()
model, metadata = load_production_model()

st.markdown("### Forecast report (CSV)")
horizon = st.slider("Forecast days to include", min_value=1, max_value=14, value=7, key="report_horizon")
if st.button("Generate forecast report"):
    forecast = generate_future_forecast(model, df, metadata["feature_names"], horizon_days=horizon)
    csv_path = export_dataframe_to_csv(forecast, EXPORTS_DIR / "forecast_report.csv")
    st.success(f"Generated {len(forecast)}-day forecast report.")
    st.download_button(
        "Download forecast_report.csv",
        data=csv_path.read_text(),
        file_name="forecast_report.csv",
        mime="text/csv",
    )

st.write("")
st.markdown("### Dataset summary (CSV)")
if st.button("Generate dataset summary"):
    summary = df.describe().reset_index().rename(columns={"index": "Statistic"})
    csv_path = export_dataframe_to_csv(summary, EXPORTS_DIR / "dataset_summary.csv")
    st.success("Generated dataset summary.")
    st.download_button(
        "Download dataset_summary.csv",
        data=csv_path.read_text(),
        file_name="dataset_summary.csv",
        mime="text/csv",
    )

st.write("")
st.markdown("### Model performance report (PDF)")
if st.button("Generate model performance PDF"):
    metadata_by_model = load_all_model_metadata()
    display_names = {
        "linear_regression_v1": "Linear Regression",
        "random_forest_v1": "Random Forest (default)",
        "random_forest_tuned_v1": "Random Forest (tuned)",
        "gradient_boosting_v1": "Gradient Boosting",
    }
    rows = []
    for key, meta in metadata_by_model.items():
        m = meta["validation_metrics"]
        rows.append({
            "Model": display_names.get(key, key),
            "MAE": round(m["MAE"], 2),
            "RMSE": round(m["RMSE"], 2),
            "R2": round(m["R2"], 4),
        })
    comparison_df = pd.DataFrame(rows).sort_values("MAE").reset_index(drop=True)

    try:
        pdf_path = export_summary_to_pdf(
            title="Delhi AQI Forecast — Model Performance Report",
            summary_lines=[
                f"Production model: {comparison_df.iloc[0]['Model']}",
                f"Best validation MAE: {comparison_df.iloc[0]['MAE']}",
                "Full methodology: data/metadata/MODEL_EVALUATION_REPORT.md",
            ],
            table_df=comparison_df,
            path=REPORTS_DIR / "model_performance_report.pdf",
        )
        st.success("Generated model performance PDF report.")
        st.download_button(
            "Download model_performance_report.pdf",
            data=pdf_path.read_bytes(),
            file_name="model_performance_report.pdf",
            mime="application/pdf",
        )
    except ImportError as e:
        st.error(str(e))
