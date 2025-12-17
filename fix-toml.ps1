rm pyproject.toml -ErrorAction SilentlyContinue

$content = @"
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "csv-profiler"
version = "0.1.0"
description = "A CSV profiling tool"
authors = [{name = "ReAlangari"}]
requires-python = ">=3.8"
dependencies = [
    "typer[all]>=0.9.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0"
]

[project.scripts]
csv-profiler = "src.csv_profiler.cli:app"

[tool.setuptools.packages.find]
where = ["src"]
"@

# Save with UTF-8 without BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PWD/pyproject.toml", $content, $utf8NoBom)

Write-Host "pyproject.toml created successfully" -ForegroundColor Green
