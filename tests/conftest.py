"""
Shared pytest fixtures and test configuration for the AQI Forecast &
Environmental Analytics Platform test suite (Handbook Appendix A.10).
"""

import sys
from pathlib import Path

# Make the project root importable so tests can `import config`,
# `import src...`, etc. without requiring the package to be installed.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
