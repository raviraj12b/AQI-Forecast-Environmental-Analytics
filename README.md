# AQI Forecast & Environmental Analytics Platform

> Forecasting future Air Quality Index (AQI) values from historical
> environmental data, with an interactive analytics dashboard.

**Status:** 🚧 Milestone 1 (Project Initialization) complete — see
[`CHANGELOG.md`](CHANGELOG.md) and `PROJECT_STATUS.md` for progress.

---

## Business Problem

Most public AQI tools report only current or historical pollution levels,
which forces reactive rather than proactive decisions. This platform adds a
predictive layer — forecasting future AQI so that health advisories and
planning decisions can happen *before* pollution reaches unsafe levels.

## Objectives

- Forecast future AQI values (next day / week / month).
- Analyze historical pollution trends and seasonal patterns.
- Evaluate individual pollutant behavior (PM2.5, PM10, NO₂, SO₂, CO, O₃).
- Present everything through an interactive, beginner-friendly dashboard.

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Data / ML | pandas, NumPy, scikit-learn |
| Visualization | Plotly, Matplotlib |
| Dashboard | Streamlit |
| Testing | pytest |
| Model persistence | joblib |

## Architecture

Layered, modular design — presentation, application/services,
machine learning, and data layers are kept independent so that, for example,
the dashboard never trains a model directly and preprocessing never imports
from the dashboard.

```
User → Streamlit Dashboard → Services → ML (forecasting/models) → Feature
Engineering → Preprocessing → Data
```

See `docs/architecture/` (to be populated) and Master Development Handbook
Part 5 for the full architecture rules.

## Project Structure

```
AQI_Forecast_Platform/
├── data/              # raw / processed / interim / external / samples / metadata
├── notebooks/         # exploratory & experimentation notebooks
├── src/                # business logic: preprocessing, feature_engineering,
│                        # models, forecasting, evaluation, visualization,
│                        # services, utils, pipelines
├── dashboard/          # Streamlit app (pages, components, styles, assets)
├── models/             # trained/checkpoints/metadata/experiments/archive
├── outputs/             # forecasts, reports, charts, exports, logs, performance
├── config/              # paths.py, constants.py, settings.py
├── tests/                # unit / integration / functional / regression
├── docs/                 # architecture, guides, diagrams, screenshots, releases
├── assets/               # logos, icons, images
├── scripts/               # automation utilities
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

Every directory contains its own `README.md` explaining its specific
responsibility in more detail.

## Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd AQI_Forecast_Platform

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place your AQI dataset in data/raw/
#    (required columns: Date, AQI, PM2.5, PM10, NO2, SO2, CO, O3 — see
#    config/constants.py: REQUIRED_DATASET_COLUMNS)
```

## Usage

```bash
# Run the notebooks (once added in Milestone 2+)
jupyter notebook notebooks/

# Launch the dashboard (once added in Milestone 5)
streamlit run dashboard/app.py

# Run the test suite
pytest
```

## Machine Learning Pipeline

```
Dataset → Validation → Cleaning → EDA → Feature Engineering → Scaling →
Time-Series Split → Model Training → Hyperparameter Tuning → Evaluation →
Model Comparison → Forecast Generation → Model Serialization →
Dashboard Integration
```

Mandatory models: Linear Regression (baseline), Random Forest. Optional:
XGBoost, LightGBM, Gradient Boosting. Chronological (non-random) splitting is
used throughout to prevent data leakage in this time-series problem.

## Dashboard Overview

Planned pages: Home · Dataset Overview · Exploratory Data Analysis ·
Pollutant Analysis · Forecast · Model Performance · Health Recommendations ·
Reports & Export · About. *(Implemented in Milestone 5.)*

## Screenshots

_To be added once the dashboard is implemented (Milestone 5)._

## Evaluation Metrics

_To be added once models are trained (Milestone 4). Target: R² > 0.80 per
PRD success metric SM-001._

## Future Improvements

Multi-city forecasting, real-time AQI API integration, LSTM/GRU deep-learning
models, interactive maps, cloud deployment. See PRD Section 17 / Part 8.7 for
the complete roadmap.

## License

Distributed under the MIT License — see [`LICENSE`](LICENSE).

## Author

_Your name here._

---

*Built following the project's PRD (`01_Product_Requirements_Document.txt`)
and Master Development Handbook (`02_Master_Development_Prompt.txt`).*
