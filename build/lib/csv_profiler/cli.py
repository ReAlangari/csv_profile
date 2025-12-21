#!/usr/bin/env python3
"""CLI for CSV Profiler"""

import sys
import os

# Add the project root to Python path to find the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Now import from csv_profiler package
from src.csv_profiler.io import read_csv_rows
from src.csv_profiler.profiling import basic_profile  # Note: your file is profiling.py, not profile.py
from src.csv_profiler.render import write_json, write_markdown

import typer
import json

app = typer.Typer(help="CSV Profiler CLI Tool")

@app.command()
def profile(
    file_path: str = typer.Argument(..., help="Path to CSV file"),
    output: str = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("json", "--format", "-f", help="Output format: json, markdown, or text")
):
    """Generate a profile for a CSV file"""
    
    try:
        # Read CSV rows
        rows = read_csv_rows(file_path)
        
        # Generate profile
        profile_data = basic_profile(rows)
        
        # Output based on format
        if output:
            if format == "json":
                write_json(profile_data, output)
            elif format == "markdown":
                write_markdown(profile_data, output)
            else:
                with open(output, 'w') as f:
                    f.write(str(profile_data))
            typer.echo(f"Profile saved to {output}")
        else:
            # Print to console
            if format == "json":
                typer.echo(json.dumps(profile_data, indent=2))
            elif format == "markdown":
                import io
                buffer = io.StringIO()
                write_markdown(profile_data, buffer)
                typer.echo(buffer.getvalue())
            else:
                typer.echo(profile_data)
                
    except FileNotFoundError:
        typer.echo(f"Error: File '{file_path}' not found", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)

@app.command()
def version():
    """Show version information"""
    typer.echo("CSV Profiler v1.0.0")

if __name__ == "__main__":
    app()