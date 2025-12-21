"""
Profiling functions
"""
from typing import List, Dict, Any
from .io import is_missing, try_float

def check_empty(value) -> str:
    """D1 Exercise 2: Check if value is empty/falsy"""
    if not bool(value):
        return 'empty'
    return 'not empty'

def count_missing(rows: List[Dict[str, str]]) -> Dict[str, int]:
    """D1 Exercise 5: Count missing values per column"""
    if not rows:
        return {}
    
    columns = list(rows[0].keys())
    missing = {col: 0 for col in columns}
    
    for row in rows:
        for col in columns:
            if row.get(col, "").strip() == "":
                missing[col] += 1
    
    return missing

def basic_profile(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    """D1 Exercise 6: Basic CSV profiler"""
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": [], "missing": {}}
    
    columns = list(rows[0].keys())
    
    return {
        "n_rows": len(rows),
        "n_cols": len(columns),
        "columns": columns,
        "missing": count_missing(rows)
    }

def infer_type(values: List[str]) -> str:
    """Infer column type (number/text)."""
    usable = [v for v in values if not is_missing(v)]
    
    if not usable:
        return "text"
    
    for v in usable:
        if try_float(v) is None:
            return "text"
    
    return "number"

def numeric_stats(values: List[str]) -> Dict[str, Any]:
    """Compute statistics for numeric columns."""
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    
    nums = []
    for v in usable:
        n = try_float(v)
        if n is not None:
            nums.append(n)
    
    count = len(nums)
    unique = len(set(nums))
    
    result = {
        "count": count,
        "missing": missing,
        "unique": unique,
    }
    
    if nums:
        result["min"] = min(nums)
        result["max"] = max(nums)
        result["mean"] = sum(nums) / count
    else:
        result["min"] = None
        result["max"] = None
        result["mean"] = None
    
    return result

def text_stats(values: List[str], top_k: int = 3) -> Dict[str, Any]:
    """Compute statistics for text columns."""
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    
    counts = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1
    
    # Get top values
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    top = [{"value": v, "count": c} for v, c in sorted_items[:top_k]]
    
    return {
        "count": len(usable),
        "missing": missing,
        "unique": len(counts),
        "top": top,
    }

def get_column_values(rows: List[Dict[str, str]], column: str) -> List[str]:
    """Extract all values for a column."""
    return [row.get(column, "") for row in rows]

def profile_column(name: str, values: List[str]) -> Dict[str, Any]:
    """Profile a single column."""
    col_type = infer_type(values)
    
    if col_type == "number":
        stats = numeric_stats(values)
    else:
        stats = text_stats(values)
    
    return {
        "name": name,
        "type": col_type,
        **stats
    }

def profile_rows(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Profile CSV rows.
    """
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": []}
    
    columns = list(rows[0].keys())
    
    column_profiles = []
    for col in columns:
        values = get_column_values(rows, col)
        profile = profile_column(col, values)
        column_profiles.append(profile)
    
    return {
        "n_rows": len(rows),
        "n_cols": len(columns),
        "columns": column_profiles,
    }