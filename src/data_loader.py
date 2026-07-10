"""Load and preprocess EDOM CSV data: parsing, period assignment, validation."""

import pandas as pd

from src.utils import (
    DATA_PATH,
    DATA_ENCODING,
    DATA_SEPARATOR,
    TIMESTAMP_COL,
    DOSEN_COL,
    PERIODE_RANGES,
    TIMESTAMP_FORMAT,
    get_kriteria_columns,
)


def load_raw_data(path=DATA_PATH, encoding=DATA_ENCODING, sep=DATA_SEPARATOR) -> pd.DataFrame:
    """Read the raw EDOM CSV file with the correct encoding."""
    df = pd.read_csv(path, encoding=encoding, sep=sep)
    return df


def parse_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the Timestamp column to proper datetime objects."""
    df = df.copy()
    df[TIMESTAMP_COL] = pd.to_datetime(
        df[TIMESTAMP_COL], format=TIMESTAMP_FORMAT, errors="coerce"
    )
    return df


def assign_periode(df: pd.DataFrame) -> pd.DataFrame:
    """Assign each row to 'Pra UTS' or 'Pra UAS' based on the Timestamp range."""
    df = df.copy()
    df["Periode"] = None

    for periode, (start_str, end_str) in PERIODE_RANGES.items():
        start = pd.to_datetime(start_str, format=TIMESTAMP_FORMAT)
        end = pd.to_datetime(end_str, format=TIMESTAMP_FORMAT)
        mask = (df[TIMESTAMP_COL] >= start) & (df[TIMESTAMP_COL] <= end)
        df.loc[mask, "Periode"] = periode

    return df


def validate_periode_assignment(df: pd.DataFrame) -> dict:
    """Return a summary dict validating that every row has a valid Periode."""
    total_rows = len(df)
    unassigned = df["Periode"].isna().sum()
    per_periode_counts = df["Periode"].value_counts(dropna=False).to_dict()

    return {
        "total_rows": total_rows,
        "unassigned_rows": int(unassigned),
        "per_periode_counts": per_periode_counts,
        "is_fully_assigned": unassigned == 0,
    }


def load_and_prepare_data(path=DATA_PATH, encoding=DATA_ENCODING) -> pd.DataFrame:
    """Full pipeline: load raw CSV, parse timestamps, assign periode."""
    df = load_raw_data(path=path, encoding=encoding)
    df = parse_timestamps(df)
    df = assign_periode(df)
    for col in get_kriteria_columns(df.columns):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def get_dosen_list(df: pd.DataFrame) -> list:
    """Return a sorted list of unique lecturer names."""
    return sorted(df[DOSEN_COL].dropna().unique().tolist())


def filter_by_dosen(df: pd.DataFrame, nama_dosen: str) -> pd.DataFrame:
    """Filter the dataframe to rows belonging to a single lecturer."""
    return df[df[DOSEN_COL] == nama_dosen].copy()


def get_kriteria_list(df: pd.DataFrame) -> list:
    """Return the 20 kriteria column names."""
    return get_kriteria_columns(df.columns)
