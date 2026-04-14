import subprocess
import sys
from pathlib import Path

from rich.console import Console

console = Console(legacy_windows=False)


def setup(project_root: Path) -> None:
    """Run uv sync inside the generated project to install deps and create the venv."""
    if not _uv_available():
        console.print(
            "[yellow]Warning:[/yellow] uv not found. "
            "Run [bold]uv sync[/bold] manually inside the project."
        )
        return

    console.print("[dim]Running uv sync...[/dim]")
    result = subprocess.run(
        ["uv", "sync"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        console.print(f"[yellow]uv sync warning:[/yellow]\n{result.stderr}")
    else:
        console.print("[green]OK[/green] Dependencies installed with uv.")


def _uv_available() -> bool:
    try:
        subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
