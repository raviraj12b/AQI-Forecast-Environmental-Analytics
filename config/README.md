# config/

Centralized configuration, kept separate from business logic
(Handbook Appendix A.9 / Section 5.8).

| File | Purpose |
|---|---|
| `paths.py` | All project file/directory paths, defined once via `pathlib`. Import these instead of hardcoding paths (NFR-SEC-002). |
| `constants.py` | Global constants: random seed, split ratios, required columns, AQI category breakpoints, evaluation metric names. |
| `settings.py` | Application-level settings (project name/version, logging format, dashboard defaults). |

No secrets, API keys, or credentials belong in this folder — see
`.gitignore` and NFR-SEC-003.
