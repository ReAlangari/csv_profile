import streamlit as st
import csv
from io import StringIO
import json

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")

# ===== Copy profiling functions from Day 2 =====

MISSING_VALUES = {"", "na", "n/a", "null", "none", "nan"}

def is_missing(value):
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

def infer_type(values):
    """Infer column type (number/text)."""
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

def numeric_stats(values):
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

def text_stats(values, top_k=3):
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

def profile_csv(rows):
    """Profile CSV rows."""
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": []}
    
    columns = list(rows[0].keys())
    col_profiles = []
    
    for col in columns:
        values = [row.get(col, "") for row in rows]
        col_type = infer_type(values)
        
        if col_type == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)
        
        col_profiles.append({
            "name": col,
            "type": col_type,
            **stats
        })
    
    return {
        "n_rows": len(rows),
        "n_cols": len(columns),
        "columns": col_profiles
    }

def generate_markdown_report(profile):
    """Generate Markdown report."""
    lines = []
    lines.append("# CSV Profiling Report")
    lines.append("")
    lines.append(f"- **Rows:** {profile['n_rows']:,}")
    lines.append(f"- **Columns:** {profile['n_cols']}")
    lines.append("")
    lines.append("## Column Summary")
    lines.append("")
    lines.append("| Column | Type | Missing | Unique |")
    lines.append("|--------|------|--------:|-------:|")
    
    for col in profile['columns']:
        n_rows = profile['n_rows']
        missing_pct = (col['missing'] / n_rows * 100) if n_rows else 0
        lines.append(f"| {col['name']} | {col['type']} | {col['missing']} ({missing_pct:.1f}%) | {col['unique']} |")
    
    return "\n".join(lines)

# ===== Streamlit App =====

# Upload
uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    # Parse CSV
    text = uploaded.getvalue().decode("utf-8")
    rows = list(csv.DictReader(StringIO(text)))
    
    # Show data preview
    st.subheader("Data Preview")
    st.write(f"Rows: {len(rows)}")
    if rows:
        st.write(f"Columns: {list(rows[0].keys())}")
    
    # Show first 5 rows as table
    if len(rows) > 0:
        st.write("First 5 rows:")
        # Create a simple table
        headers = list(rows[0].keys())
        table_data = []
        for i, row in enumerate(rows[:5]):
            table_data.append([row.get(h, "") for h in headers])
        
        # Display as markdown table
        header_row = "| " + " | ".join(headers) + " |"
        separator = "| " + " | ".join(["---"] * len(headers)) + " |"
        data_rows = []
        for data in table_data:
            data_rows.append("| " + " | ".join(str(cell) for cell in data) + " |")
        
        st.markdown("\n".join([header_row, separator] + data_rows))
    
    # Profile on button click
    if st.button("Generate Profile"):
        profile = profile_csv(rows)
        st.session_state["profile"] = profile
        st.success("Profile generated!")
    
    # Display if available
    if "profile" in st.session_state:
        profile = st.session_state["profile"]
        
        # Show metrics
        st.subheader("Profile Results")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows", profile['n_rows'])
        with col2:
            st.metric("Columns", profile['n_cols'])
        
        # Show column details
        st.subheader("Column Analysis")
        
        for col in profile['columns']:
            with st.expander(f"{col['name']} ({col['type']})"):
                st.write(f"**Missing values:** {col['missing']}")
                st.write(f"**Unique values:** {col['unique']}")
                
                if col['type'] == 'number':
                    if col.get('min') is not None:
                        st.write(f"**Min:** {col['min']}")
                        st.write(f"**Max:** {col['max']}")
                        st.write(f"**Mean:** {col['mean']:.2f}")
                else:
                    if col.get('top'):
                        st.write("**Top values:**")
                        for item in col['top']:
                            st.write(f"- {item['value']}: {item['count']}")
        
        # Export section
        st.subheader("Export Reports")
        
        # JSON export
        json_report = json.dumps(profile, indent=2)
        st.download_button(
            "Download JSON",
            json_report,
            "profile.json",
            "application/json"
        )
        
        # Markdown export
        md_report = generate_markdown_report(profile)
        st.download_button(
            "Download Markdown",
            md_report,
            "profile.md",
            "text/markdown"
        )
        
        # Show JSON
        with st.expander("View JSON"):
            st.json(profile)

else:
    st.info("Please upload a CSV file to begin.")
    
    # Example
    st.write("Example CSV format:")
    st.code("""name,age,city,salary
Aisha,23,Riyadh,12000
Fahad,,Jeddah,9000
Noor,29,,15000
Salem,31,Dammam,15000""")