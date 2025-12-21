"""
Typer CLI for CSV Profiler
"""
import typer
from pathlib import Path
import time
import subprocess  # ADD THIS
import sys         # ADD THIS

from .io import read_csv_rows
from .profiling import profile_rows
from .render import write_json, write_markdown, slugify

app = typer.Typer(help="CSV Profiler CLI Tool")

@app.command()
def profile(
    file_path: str = typer.Argument(..., help="Path to CSV file"),
    out_dir: str = typer.Option("outputs", "--out-dir", "-o", help="Output directory"),
    report_name: str = typer.Option("report", "--report-name", "-n", help="Report name"),
    format: str = typer.Option("both", "--format", "-f", 
                               help="Output format: json, markdown, or both")
):
    """
    Profile a CSV file and generate a report.
    
    Example:
    python -m csv_profiler.cli profile data/sample.csv --out-dir outputs --report-name my_report --format json
    """
    try:
        # Start timing
        start_time = time.perf_counter()
        
        # Check if file exists
        if not Path(file_path).exists():
            typer.echo(f"Error: File not found: {file_path}")
            raise typer.Exit(code=1)
        
        typer.echo(f" Profiling: {file_path}")
        
        # Read CSV
        rows = read_csv_rows(file_path)
        typer.echo(f" Read {len(rows)} rows")
        
        # Generate profile
        profile_data = profile_rows(rows)
        
        # Auto-generate report name if not provided
        if report_name == "report":
            file_stem = Path(file_path).stem
            report_name = f"profile-{slugify(file_stem)}"
        
        # Create output directory
        output_path = Path(out_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save reports based on format
        files_saved = []
        
        # Save JSON report
        if format in ("json", "both"):
            json_file = output_path / f"{report_name}.json"
            write_json(profile_data, str(json_file))
            files_saved.append(f"JSON: {json_file}")
        
        # Save Markdown report
        if format in ("markdown", "md", "both"):
            md_file = output_path / f"{report_name}.md"
            write_markdown(profile_data, str(md_file))
            files_saved.append(f"Markdown: {md_file}")
        
        # Calculate time
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000
        
        # Show summary
        for file_info in files_saved:
            typer.echo(f" ✓ {file_info}")
        
        typer.echo(f"  Profiling took: {elapsed_ms:.2f}ms")
        
        # Show quick summary
        typer.echo(f"\n Summary:")
        typer.echo(f"  Rows: {profile_data['n_rows']:,}")
        typer.echo(f"  Columns: {profile_data['n_cols']}")
        
        # Show first 3 columns
        for col in profile_data['columns'][:3]:
            missing_pct = (col['missing'] / profile_data['n_rows']) * 100
            typer.echo(f"  {col['name']}: {col['type']} ({col['missing']} missing, {missing_pct:.1f}%)")
        
        if len(profile_data['columns']) > 3:
            typer.echo(f"  ... and {len(profile_data['columns']) - 3} more columns")
            
    except Exception as e:
        typer.echo(f" Error: {e}")
        raise typer.Exit(code=1)

@app.command()
def web() -> None:
    """Launch the Streamlit web interface."""
    # Get path to app.py relative to this module
    app_path = Path(__file__).parent / "app.py"
    
    # Check if app.py exists
    if not app_path.exists():
        typer.echo(f"Error: app.py not found at {app_path}")
        raise typer.Exit(code=1)
    
    typer.echo("Starting Streamlit app...")
    typer.echo(f"Opening browser at http://localhost:8501")
    
    try:
        # Launch Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])
    except KeyboardInterrupt:
        typer.echo("\nStreamlit app stopped.")
    except Exception as e:
        typer.echo(f"Error starting Streamlit: {e}")
        raise typer.Exit(code=1)

@app.command()
def version():
    """Show version information."""
    typer.echo("CSV Profiler v1.0.0")

if __name__ == "__main__":
    app()