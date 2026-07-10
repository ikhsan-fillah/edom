"""Utility constants and helpers for the EDOM Dashboard project."""

import re
from pathlib import Path

DATA_PATH = Path("data/EDOM GENAP 25 26(Sheet1).csv")
DATA_ENCODING = "latin1"
DATA_SEPARATOR = ";"
OUTPUT_DIR = Path("output/charts")

TIMESTAMP_COL = "Timestamp"
DOSEN_COL = "Nama dosen yang anda nilai :"

PERIODE_RANGES = {
    "Pra UTS": ("08/01/2026 05.29", "27/04/2026 13.56"),
    "Pra UAS": ("08/06/2026 08.14", "26/06/2026 14.46"),
}

TIMESTAMP_FORMAT = "%d/%m/%Y %H.%M"

SCORE_MIN = 1
SCORE_MAX = 8


def safe_filename(value: str, max_length: int = 80) -> str:
    """Return a Windows-safe file or folder name."""
    safe_value = re.sub(r'[<>:"/\\|?*]+', "_", value.strip())
    safe_value = re.sub(r"\s+", "_", safe_value)
    safe_value = safe_value.strip("._")
    return safe_value[:max_length] or "untitled"


def get_output_dir(nama_dosen: str) -> Path:
    """Return (and create) the output directory for a given lecturer."""
    safe_name = safe_filename(nama_dosen)
    out_dir = OUTPUT_DIR / safe_name
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def get_kriteria_columns(df_columns) -> list:
    """Return the 20 numeric kriteria columns."""
    prefixes = tuple(f"{number}." for number in range(1, 21))
    return [col for col in df_columns if col.strip().startswith(prefixes)]
