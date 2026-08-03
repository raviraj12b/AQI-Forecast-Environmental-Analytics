"""Unit tests for src.preprocessing.data_validator (FR-DATA-002)."""

from pathlib import Path

import pandas as pd
import pytest

from config.constants import REQUIRED_DATASET_COLUMNS
from src.preprocessing.data_loader import load_dataset
from src.preprocessing.data_validator import ValidationReport, validate_dataset
from src.utils.exceptions import DatasetValidationError

FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent / "test_data" / "synthetic_aqi_fixture.csv"
)


def test_validate_dataset_passes_on_valid_fixture():
    df = load_dataset(FIXTURE_PATH)
    report = validate_dataset(df, REQUIRED_DATASET_COLUMNS)
    assert isinstance(report, ValidationReport)
    assert report.is_valid is True
    assert report.missing_required_columns == []
    assert report.duplicate_column_names == []


def test_validate_dataset_detects_injected_missing_values():
    df = load_dataset(FIXTURE_PATH)
    report = validate_dataset(df, REQUIRED_DATASET_COLUMNS)
    # The fixture intentionally contains 3 missing PM2.5 values.
    assert report.missing_value_counts["PM2.5"] == 3


def test_validate_dataset_detects_injected_duplicate_row():
    df = load_dataset(FIXTURE_PATH)
    report = validate_dataset(df, REQUIRED_DATASET_COLUMNS)
    # The fixture intentionally contains exactly 1 duplicated row.
    assert report.duplicate_row_count == 1


def test_validate_dataset_rejects_missing_required_column():
    df = load_dataset(FIXTURE_PATH)
    df_missing_col = df.drop(columns=["AQI"])
    with pytest.raises(DatasetValidationError):
        validate_dataset(df_missing_col, REQUIRED_DATASET_COLUMNS)


def test_validate_dataset_rejects_empty_dataframe():
    empty_df = pd.DataFrame(columns=REQUIRED_DATASET_COLUMNS)
    with pytest.raises(DatasetValidationError):
        validate_dataset(empty_df, REQUIRED_DATASET_COLUMNS)


def test_validate_dataset_rejects_duplicate_column_names():
    df = load_dataset(FIXTURE_PATH)
    df_dupe_cols = df.copy()
    df_dupe_cols.columns = list(df.columns[:-1]) + [df.columns[0]]  # duplicate "City"
    with pytest.raises(DatasetValidationError):
        validate_dataset(df_dupe_cols, REQUIRED_DATASET_COLUMNS)


def test_validation_report_summary_is_readable_string():
    df = load_dataset(FIXTURE_PATH)
    report = validate_dataset(df, REQUIRED_DATASET_COLUMNS)
    assert isinstance(report.summary(), str)
    assert "VALID" in report.summary()
