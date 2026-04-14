import subprocess
from pathlib import Path

from rich.console import Console

console = Console(legacy_windows=False)


def init(project_root: Path) -> None:
    """Initialize a git repo and make the initial scaffold commit."""
    if not _git_available():
        console.print(
            "[yellow]Warning:[/yellow] git not found. "
            "Run [bold]git init[/bold] manually inside the project."
        )
        return

    try:
        subprocess.run(["git", "init"], cwd=project_root, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=project_root, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "chore: initial scaffold via create-ai-project"],
            cwd=project_root,
            check=True,
            capture_output=True,
        )
        console.print("[green]OK[/green] Git repository initialized.")
    except subprocess.CalledProcessError as e:
        console.print(f"[yellow]git warning:[/yellow] {e}")


def _git_available() -> bool:
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
