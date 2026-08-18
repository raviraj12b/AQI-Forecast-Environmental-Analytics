"""
Dataset loading for the AQI Forecast & Environmental Analytics Platform.

Responsible only for reading a CSV file into a pandas DataFrame and parsing
its date column. Validation and cleaning are deliberately out of scope here
-- see `data_validator.py` -- per Handbook Section 5.5 (Module Responsibility
Rule) and FR-DATA-001.
"""

from pathlib import Path
from typing import Union

import pandas as pd

from src.utils.exceptions import DatasetLoadError
from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_dataset(
    path: Union[str, Path],
    date_column: str = "Date",
    dayfirst: bool = False,
    date_format: Union[str, None] = None,
) -> pd.DataFrame:
    """
    Load an AQI dataset from a CSV file.

    Parameters
    ----------
    path : str or Path
        Location of the CSV file to load.
    date_column : str, default "Date"
        Name of the column to parse as a datetime, if present in the file.
    dayfirst : bool, default False
        Passed to `pandas.to_datetime`. Ambiguous date strings like
        "02/01/18" parse very differently depending on this flag
        (2 Jan vs 1 Feb) -- verified against the real Delhi AQI dataset,
        where the default `False` silently mis-parsed 792/2191 rows (36%)
        because its dates are DD/MM/YY. Set `dayfirst=True` for that source.
    date_format : str, optional
        An explicit strftime format (e.g. "%d/%m/%y"). When given, this
        takes precedence over `dayfirst` and avoids pandas' per-row
        format-inference entirely -- the most robust option once you know
        your source's exact date format.

    Returns
    -------
    pd.DataFrame
        The loaded dataset, with `date_column` parsed as datetime when present.

    Raises
    ------
    DatasetLoadError
        If the file does not exist, is empty, or cannot be parsed as CSV.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise DatasetLoadError(f"Dataset not found at '{file_path}'.")

    if file_path.stat().st_size == 0:
        raise DatasetLoadError(f"Dataset at '{file_path}' is an empty file.")

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as exc:
        raise DatasetLoadError(
            f"Dataset at '{file_path}' has no parseable data."
        ) from exc
    except pd.errors.ParserError as exc:
        raise DatasetLoadError(
            f"Dataset at '{file_path}' is not valid CSV: {exc}"
        ) from exc

    if df.empty:
        raise DatasetLoadError(f"Dataset at '{file_path}' loaded with zero rows.")

    if date_column in df.columns:
        if date_format is not None:
            df[date_column] = pd.to_datetime(
                df[date_column], format=date_format, errors="coerce"
            )
        else:
            df[date_column] = pd.to_datetime(
                df[date_column], dayfirst=dayfirst, errors="coerce"
            )
        n_unparsed = int(df[date_column].isna().sum())
        if n_unparsed:
            logger.warning(
                "%d row(s) in '%s' had a %s value that could not be parsed "
                "as a date.",
                n_unparsed,
                file_path.name,
                date_column,
            )

    logger.info(
        "Loaded dataset '%s': %d rows, %d columns.", file_path.name, *df.shape
    )
    return df
