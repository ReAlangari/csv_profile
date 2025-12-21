## Usage

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