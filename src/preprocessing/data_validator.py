"""
Dataset validation for the AQI Forecast & Environmental Analytics Platform.

Verifies dataset integrity before any downstream cleaning, feature
engineering, or model training occurs, per FR-DATA-002 and Handbook Section
6.3 (Data Validation Standards). Validation failures raise
`DatasetValidationError` so that invalid datasets cannot silently continue
through the pipeline (FR-DATA-002 acceptance criteria: "Invalid datasets
cannot continue").
"""

from dataclasses import dataclass
from typing import Sequence

import pandas as pd

from src.utils.exceptions import DatasetValidationError
from src.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ValidationReport:
    """Structured result of validating a dataset (ML-EDA-001 profiling fields)."""

    is_valid: bool
    row_count: int
    column_count: int
    missing_required_columns: list
    duplicate_column_names: list
    dtypes: dict
    missing_value_counts: dict
    missing_value_percentages: dict
    duplicate_row_count: int

    def summary(self) -> str:
        """Human-readable summary, e.g. for logging or the Dataset Overview page."""
        status = "VALID" if self.is_valid else "INVALID"
        lines = [
            f"Validation status: {status}",
            f"Shape: {self.row_count} rows x {self.column_count} columns",
            f"Duplicate rows: {self.duplicate_row_count}",
        ]
        if self.missing_required_columns:
            lines.append(f"Missing required columns: {self.missing_required_columns}")
        if self.duplicate_column_names:
            lines.append(f"Duplicate column names: {self.duplicate_column_names}")
        nonzero_missing = {
            col: pct for col, pct in self.missing_value_percentages.items() if pct > 0
        }
        if nonzero_missing:
            lines.append(f"Columns with missing values (%): {nonzero_missing}")
        return "\n".join(lines)


def validate_dataset(
    df: pd.DataFrame, required_columns: Sequence[str]
) -> ValidationReport:
    """
    Validate a loaded dataset against required-column and integrity rules.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to validate (typically the output of `load_dataset`).
    required_columns : Sequence[str]
        Column names that must be present for the dataset to be usable
        (see `config.constants.REQUIRED_DATASET_COLUMNS`).

    Returns
    -------
    ValidationReport
        Full validation report, including non-blocking diagnostics such as
        missing-value counts and duplicate-row counts. Missing values and
        duplicate *rows* are informational here (FR-DATA-003/004 handle
        them) — only structural problems block the pipeline.

    Raises
    ------
    DatasetValidationError
        If the dataset is empty, has duplicate column names, or is missing
        any required column.
    """
    if df.empty:
        raise DatasetValidationError("Dataset is empty (zero rows).")

    column_list = list(df.columns)
    duplicate_column_names = list(
        dict.fromkeys(col for col in column_list if column_list.count(col) > 1)
    )

    missing_required_columns = [
        col for col in required_columns if col not in df.columns
    ]

    is_valid = not duplicate_column_names and not missing_required_columns

    missing_counts = df.isna().sum()
    missing_percentages = (missing_counts / len(df) * 100).round(2)

    report = ValidationReport(
        is_valid=is_valid,
        row_count=len(df),
        column_count=df.shape[1],
        missing_required_columns=missing_required_columns,
        duplicate_column_names=duplicate_column_names,
        dtypes={col: str(dtype) for col, dtype in df.dtypes.items()},
        missing_value_counts=missing_counts.to_dict(),
        missing_value_percentages=missing_percentages.to_dict(),
        duplicate_row_count=int(df.duplicated().sum()),
    )

    if not is_valid:
        logger.error("Dataset validation failed:\n%s", report.summary())
        raise DatasetValidationError("Dataset failed validation.\n" + report.summary())

    logger.info("Dataset validation passed.\n%s", report.summary())
    return report
