"""Unit tests for src.services.report_service (FR-REPORT-001/002)."""

import pandas as pd
import pytest

from src.services.report_service import export_dataframe_to_csv, export_summary_to_pdf


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Date": pd.date_range("2025-01-01", periods=3),
        "Predicted_AQI": [250.0, 260.0, 245.0],
    })


def test_export_dataframe_to_csv_creates_file(sample_df, tmp_path):
    out_path = export_dataframe_to_csv(sample_df, tmp_path / "test_export.csv")
    assert out_path.exists()


def test_export_dataframe_to_csv_roundtrips_data(sample_df, tmp_path):
    out_path = export_dataframe_to_csv(sample_df, tmp_path / "test_export.csv")
    reloaded = pd.read_csv(out_path)
    assert len(reloaded) == len(sample_df)
    assert list(reloaded.columns) == list(sample_df.columns)


def test_export_dataframe_to_csv_creates_parent_directories(sample_df, tmp_path):
    nested_path = tmp_path / "a" / "b" / "c" / "export.csv"
    out_path = export_dataframe_to_csv(sample_df, nested_path)
    assert out_path.exists()


def test_export_summary_to_pdf_creates_file(sample_df, tmp_path):
    out_path = export_summary_to_pdf(
        title="Test Report",
        summary_lines=["Line 1", "Line 2"],
        table_df=sample_df,
        path=tmp_path / "test_report.pdf",
    )
    assert out_path.exists()
    assert out_path.stat().st_size > 0


def test_export_summary_to_pdf_produces_valid_pdf_header(sample_df, tmp_path):
    out_path = export_summary_to_pdf(
        title="Test Report", summary_lines=["Line 1"], table_df=sample_df,
        path=tmp_path / "test_report.pdf",
    )
    with open(out_path, "rb") as f:
        header = f.read(5)
    assert header == b"%PDF-"
