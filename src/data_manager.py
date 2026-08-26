"""Validation and file replacement helpers for EDOM source data."""

from datetime import datetime
from pathlib import Path
import shutil

import pandas as pd

from src.utils import (
    DATA_ENCODING,
    DATA_PATH,
    DATA_SEPARATOR,
    DOSEN_COL,
    TIMESTAMP_COL,
    get_kriteria_columns,
)


def validate_edom_file(file_path: Path) -> tuple[bool, str]:
    """Validate CSV structure before replacing active EDOM data."""
    try:
        df = pd.read_csv(
            file_path,
            encoding=DATA_ENCODING,
            sep=DATA_SEPARATOR,
        )
    except Exception as error:
        return False, f"File tidak dapat dibaca: {error}"

    required_columns = [TIMESTAMP_COL, DOSEN_COL]
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        return (
            False,
            "Kolom wajib tidak ditemukan: "
            + ", ".join(missing_columns),
        )

    kriteria_columns = get_kriteria_columns(df.columns)

    if len(kriteria_columns) != 20:
        return (
            False,
            "Jumlah kolom kriteria tidak valid. "
            f"Ditemukan {len(kriteria_columns)}, seharusnya 20.",
        )

    if df.empty:
        return False, "File tidak memiliki data responden."

    return (
        True,
        f"Valid. File berisi {len(df)} respons dan "
        f"{len(kriteria_columns)} kolom kriteria.",
    )


def replace_edom_data(uploaded_bytes: bytes) -> Path:
    """Back up old data and replace it with uploaded CSV data."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DATA_PATH.exists():
        backup_dir = DATA_PATH.parent / "backup"
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"edom_backup_{timestamp}.csv"

        shutil.copy2(DATA_PATH, backup_path)

    DATA_PATH.write_bytes(uploaded_bytes)

    return DATA_PATH
