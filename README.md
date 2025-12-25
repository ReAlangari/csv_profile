## Usage
CSV Profiler
About
CSV Profiler is a simple Python project that creates summary reports for CSV files.
It is designed to help users quickly understand the structure and quality of their datasets by generating clear and readable summaries.

The tool analyzes CSV files and provides information such as basic statistics, missing values, and column data types.
CSV Profiler can be used through a command-line interface (CLI) or through an optional Streamlit web application for interactive exploration.

This project is suitable for beginners learning data analysis, Python CLI tools, and GitHub workflows.

Features
Generate JSON and Markdown summary reports from any CSV file
Display basic statistics such as:
Total number of rows
Total number of columns
Missing values per column
Data types of each column
Use a simple command-line interface (CLI) for quick and easy profiling
Launch an optional Streamlit web app to explore CSV summaries interactively
Installation
Prerequisites
Before running the project, make sure you have the following installed:

Python 3.10 or higher
UV package manager
Run Without Cloning
You can run CSV Profiler directly from GitHub using uvx without cloning the repository:
### CLI Commands
```bash
# Profile a CSV file (default: both JSON and Markdown)
csv-profiler profile data/sample.csv

# Profile with custom output directory
csv-profiler profile data/sample.csv --out-dir my_reports

# Profile with specific format
csv-profiler profile data/sample.csv --format json
csv-profiler profile data/sample.csv --format markdown

# Profile with custom report name
csv-profiler profile data/sample.csv --report-name analysis_report --format both

# All options together
csv-profiler profile data/sample.csv --out-dir reports --report-name analysis --format both

# Launch web interface
csv-profiler web
