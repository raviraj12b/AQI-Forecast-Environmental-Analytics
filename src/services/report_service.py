"""
Report export service for the AQI Forecast & Environmental Analytics
Platform (FR-REPORT-001/002).

CSV export has no external dependency risk. PDF export uses `reportlab`,
confirmed available in this environment; if a deployment environment lacks
it, `export_summary_to_pdf` raises a clear `ImportError`-derived message
rather than silently failing or crashing with an unrelated traceback.
"""

from pathlib import Path
from typing import Union

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def export_dataframe_to_csv(df: pd.DataFrame, path: Union[str, Path]) -> Path:
    """
    Export any DataFrame to CSV (FR-REPORT-001). Used for forecast results,
    dataset summaries, and model comparison tables alike -- one small,
    reusable function rather than a bespoke exporter per report type.
    """
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    logger.info("export_dataframe_to_csv: wrote %d rows to '%s'.", len(df), out_path)
    return out_path


def export_summary_to_pdf(
    title: str,
    summary_lines: list,
    table_df: pd.DataFrame,
    path: Union[str, Path],
) -> Path:
    """
    Generate a simple one-page PDF report (FR-REPORT-001): title, summary
    bullet lines, and a data table. Deliberately simple (no embedded
    charts) -- sufficient for a forecast/model-performance summary without
    taking on heavier PDF-layout dependencies than `reportlab` alone.

    Parameters
    ----------
    title : str
    summary_lines : list of str
        Rendered as bullet points beneath the title.
    table_df : pd.DataFrame
        Rendered as a simple table beneath the summary.
    path : str or Path

    Returns
    -------
    Path

    Raises
    ------
    ImportError
        If `reportlab` is not installed, with a clear message rather than
        a bare traceback from a missing import deep in the call stack.
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError as exc:
        raise ImportError(
            "PDF export requires the 'reportlab' package "
            "(pip install reportlab). CSV export via "
            "export_dataframe_to_csv() does not have this dependency."
        ) from exc

    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(out_path), pagesize=A4)
    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

    for line in summary_lines:
        story.append(Paragraph(f"\u2022 {line}", styles["Normal"]))
    story.append(Spacer(1, 16))

    table_data = [list(table_df.columns)] + table_df.astype(str).values.tolist()
    table = Table(table_data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4C72B0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F0F0")]),
            ]
        )
    )
    story.append(table)

    doc.build(story)
    logger.info("export_summary_to_pdf: wrote '%s'.", out_path)
    return out_path
