# CSV Profiler

## 📊 About
**CSV Profiler** is a simple Python project that creates summary reports for CSV files. It helps users quickly understand the structure and quality of their datasets by generating clear, readable summaries.

The tool analyzes CSV files and provides information such as basic statistics, missing values, and column data types. CSV Profiler can be used through a command-line interface (CLI) or through an optional Streamlit web application for interactive exploration.

This project is suitable for beginners learning data analysis, Python CLI tools, and GitHub workflows.

## ✨ Features
- Generate **JSON** and **Markdown** summary reports from any CSV file
- Display basic statistics:
  - Total number of rows and columns
  - Missing values per column
  - Data types of each column
  - Unique value counts
- Simple command-line interface (CLI) for quick profiling
- Optional **Streamlit web app** for interactive CSV exploration
- Lightweight and easy to install

## 🚀 Installation

### Prerequisites
- **Python 3.10** or higher
- **UV package manager** (recommended) or pip

### Install from Source
```bash
# Clone the repository
git clone https://github.com/ReAlangari/csv-profiler.git
cd csv-profiler

# Install with UV
uv sync

# Or install with pip
pip install -e .
