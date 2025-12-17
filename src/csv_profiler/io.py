"""
IO functions for CSV reading
"""
import csv
from pathlib import Path
from typing import List, Dict

MISSING_VALUES = {"", "na", "n/a", "null", "none", "nan"}

def is_missing(value) -> bool:
    """Check if value is missing."""
    if value is None:
        return True
    if isinstance(value, str):
        cleaned = value.strip().casefold()
        return cleaned in MISSING_VALUES or cleaned == ""
    return False

def try_float(value):
    """Safely convert to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def read_csv_rows(file_path: str) -> List[Dict[str, str]]:
    """Read a CSV file into list of dictionaries."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)