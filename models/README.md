# models/

Repository for trained, production-ready ML artifacts (Handbook Appendix A.7).
This is distinct from `src/models/`, which contains the *code* that trains
and loads models — this folder holds the serialized *output* of that code.

| Folder | Purpose |
|---|---|
| `trained/` | Approved, production-ready serialized models (`.joblib`). |
| `checkpoints/` | Intermediate training checkpoints. |
| `metadata/` | Model metadata: algorithm, dataset version, features, metrics, hyperparameters. |
| `experiments/` | Experimental models not selected for production. |
| `archive/` | Deprecated/superseded model versions, kept for reproducibility. |

Naming convention: `<algorithm>_v<version>.joblib` (e.g. `random_forest_v1.joblib`) — never `model.pkl` or `latest.joblib`.
