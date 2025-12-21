"""
Rendering functions for reports
"""
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    return "-".join(text.strip().casefold().split())

def build_markdown_report(profile: Dict[str, Any]) -> str:
    """Build a Markdown report."""
    lines = []
    
    # Header
    lines.append("# CSV Profiling Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    
    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Rows:** {profile['n_rows']:,}")
    lines.append(f"- **Columns:** {profile['n_cols']}")
    lines.append("")
    
    # Column table
    lines.append("## Columns")
    lines.append("")
    lines.append("| Column | Type | Missing | Unique |")
    lines.append("|--------|------|--------:|-------:|")
    
    for col_info in profile['columns']:
        name = col_info['name']
        col_type = col_info['type']
        missing = col_info['missing']
        unique = col_info['unique']
        lines.append(f"| {name} | {col_type} | {missing} | {unique} |")
    
    lines.append("")
    
    # Detailed statistics
    lines.append("## Detailed Statistics")
    lines.append("")
    
    for col_info in profile['columns']:
        lines.append(f"### {col_info['name']}")
        lines.append("")
        lines.append(f"- **Type:** {col_info['type']}")
        lines.append(f"- **Missing values:** {col_info['missing']}")
        lines.append(f"- **Unique values:** {col_info['unique']}")
        
        if col_info['type'] == 'number':
            if col_info.get('min') is not None:
                lines.append(f"- **Min:** {col_info['min']}")
            if col_info.get('max') is not None:
                lines.append(f"- **Max:** {col_info['max']}")
            if col_info.get('mean') is not None:
                lines.append(f"- **Mean:** {col_info['mean']:.2f}")
        else:
            lines.append(f"- **Top values:**")
            for item in col_info.get('top', []):
                lines.append(f"  - {item['value']}: {item['count']}")
        
        lines.append("")
    
    return "\n".join(lines)

def write_json(report: Dict[str, Any], path: str) -> None:
    """Write report as JSON file."""
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

def write_markdown(report: Dict[str, Any], path: str) -> None:
    """Write report as Markdown file."""
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    markdown = build_markdown_report(report)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(markdown)