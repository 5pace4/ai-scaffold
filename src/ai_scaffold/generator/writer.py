from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_scaffold.generator import engine
from ai_scaffold.generator.context import ProjectContext
from ai_scaffold.generator.engine import MANIFEST_MAP, ManifestEntry
from ai_scaffold.profiles.base import PROFILE_REGISTRY

console = Console()


def should_include(entry: ManifestEntry, context: ProjectContext) -> bool:
    """Return False if any required flag is disabled on the context."""
    for flag in entry.requires:
        if not getattr(context, flag, True):
            return False
    return True


def write_project(context: ProjectContext) -> Path:
    # Import profile modules to trigger registration
    import ai_scaffold.profiles.minimal  # noqa: F401
    import ai_scaffold.profiles.rag  # noqa: F401
    import ai_scaffold.profiles.agent  # noqa: F401
    import ai_scaffold.profiles.full  # noqa: F401

    # Populate extra_deps from the context's resolved deps (used by pyproject_toml.j2)
    context = context.model_copy(update={"extra_deps": context.resolved_deps()})

    profile = PROFILE_REGISTRY[context.profile]
    root = Path.cwd() / context.project_name

    if root.exists():
        overwrite = typer.confirm(
            f"Directory '{root.name}' already exists. Overwrite?", default=False
        )
        if not overwrite:
            raise typer.Abort()

    included = [
        key for key in profile.manifest if should_include(MANIFEST_MAP[key], context)
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(
            f"[cyan]Scaffolding [bold]{context.project_name}[/bold]...",
            total=len(included),
        )

        for key in included:
            entry = MANIFEST_MAP[key]
            content = engine.render(key, context)
            dest = root / entry.output_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
            progress.advance(task)

    # Ensure __init__.py in every Python package directory
    for py_dir in _find_python_dirs(root):
        init = py_dir / "__init__.py"
        if not init.exists():
            init.write_text("")

    # Create empty data dirs (raw / processed / index_config)
    for subdir in ["raw", "processed", "index_config"]:
        d = root / "data" / subdir
        d.mkdir(parents=True, exist_ok=True)
        (d / ".gitkeep").write_text("")

    # Create eval_results dir if evaluation was scaffolded
    if "evaluation.offline_eval" in included:
        results_dir = root / "evaluation" / "eval_results"
        results_dir.mkdir(parents=True, exist_ok=True)
        (results_dir / ".gitkeep").write_text("")

    # Create frontend/static if frontend included
    if context.include_frontend and "frontend.app" in included:
        (root / "frontend" / "static").mkdir(parents=True, exist_ok=True)

    return root


def _find_python_dirs(root: Path) -> list[Path]:
    """Return directories that contain .py files (excluding hidden/venv dirs)."""
    skip = {"__pycache__", ".venv", "venv", "node_modules", ".git"}
    result: list[Path] = []
    for d in root.rglob("*"):
        if d.is_dir() and d.name not in skip and not d.name.startswith("."):
            if any(f.suffix == ".py" for f in d.iterdir() if f.is_file()):
                result.append(d)
    return result
