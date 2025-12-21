# CSV Profiler

A simple Python tool for profiling CSV files with CLI and web interface.

## Features
- Generate JSON and Markdown summary reports
- Analyze CSV structure and data quality
- Web interface using Streamlit
- Command-line interface using Typer

## Installation

### Using uv (Recommended)
```bash
# Run directly from GitHub
uvx git+https://github.com/justRuba/CSV-profiler web
uvx git+https://github.com/justRuba/CSV-profiler profile data.csv --format both