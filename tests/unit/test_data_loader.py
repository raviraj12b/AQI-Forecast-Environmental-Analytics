"""Unit tests for src.preprocessing.data_loader (FR-DATA-001)."""

from pathlib import Path

import pandas as pd
import pytest

from src.preprocessing.data_loader import load_dataset
from src.utils.exceptions import DatasetLoadError

FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent / "test_data" / "synthetic_aqi_fixture.csv"
)


def test_load_dataset_returns_dataframe():
    df = load_dataset(FIXTURE_PATH)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_dataset_has_expected_shape():
    df = load_dataset(FIXTURE_PATH)
    assert df.shape == (61, 9)


def test_load_dataset_parses_date_column():
    df = load_dataset(FIXTURE_PATH)
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])


def test_load_dataset_missing_file_raises():
    with pytest.raises(DatasetLoadError):
        load_dataset("data/raw/does_not_exist.csv")


def test_load_dataset_empty_file_raises(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    with pytest.raises(DatasetLoadError):
        load_dataset(empty_file)


def test_load_dataset_header_only_file_raises(tmp_path):
    header_only = tmp_path / "header_only.csv"
    header_only.write_text("City,Date,AQI,PM2.5,PM10,NO2,SO2,CO,O3\n")
    with pytest.raises(DatasetLoadError):
        load_dataset(header_only)
