import streamlit as st
import csv
from io import StringIO
import json

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("📊 CSV Profiler")

# ---- Simple functions from Day 2 ----
def is_missing(v):
    return v is None or str(v).strip().lower() in ["", "na", "n/a", "null"]

def infer_type(values):
    for v in values:
        if not is_missing(v):
            try:
                float(v)
            except:
                return "text"
    return "number"

def profile_data(rows):
    if not rows: 
        return {"rows": 0, "cols": 0, "columns": []}
    
    cols = list(rows[0].keys())
    result = {"rows": len(rows), "cols": len(cols), "columns": []}
    
    for col in cols:
        values = [r.get(col, "") for r in rows]
        missing = sum(1 for v in values if is_missing(v))
        col_type = infer_type(values)
        
        col_info = {
            "name": col, 
            "type": col_type, 
            "missing": missing,
            "unique": len(set(v for v in values if not is_missing(v)))
        }
        result["columns"].append(col_info)
    
    return result

# ---- App ----
uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    # Read file
    text = uploaded.read().decode("utf-8")
    rows = list(csv.DictReader(StringIO(text)))
    
    st.write(f"**File:** {uploaded.name}")
    st.write(f"**Rows:** {len(rows)}")
    
    if rows:
        st.write(f"**Columns:** {', '.join(rows[0].keys())}")
    
    # Show first 3 rows
    st.write("**Preview:**")
    for i, row in enumerate(rows[:3]):
        st.write(f"{i+1}. {row}")
    
    # Generate profile
    if st.button("Analyze"):
        profile = profile_data(rows)
        st.session_state.profile = profile
        st.success("Analysis complete!")
    
    # Show results
    if "profile" in st.session_state:
        p = st.session_state.profile
        
        st.write("---")
        st.write("## 📈 Results")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows", p["rows"])
        with col2:
            st.metric("Columns", p["cols"])
        
        # Column table
        st.write("### Columns")
        for col in p["columns"]:
            st.write(f"**{col['name']}** ({col['type']}) - "
                    f"Missing: {col['missing']}, Unique: {col['unique']}")
        
        # Download button
        json_data = json.dumps(p, indent=2)
        st.download_button("📥 Download JSON", json_data, "profile.json")
        
else:
    st.info("👈 Upload a CSV file to analyze")
    st.code("""name,age,city
Aisha,23,Riyadh
Fahad,,Jeddah
Noor,29,""")