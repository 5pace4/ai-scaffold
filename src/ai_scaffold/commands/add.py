import tomllib
from pathlib import Path

import typer
from rich.console import Console

from ai_scaffold.generator.context import (
    DEFAULT_EMBEDDING,
    DEFAULT_MODEL,
    ProjectContext,
)
from ai_scaffold.generator.engine import MANIFEST_MAP
from ai_scaffold.generator.writer import should_include

console = Console()

# Components that can be added to an existing project
ADDABLE_COMPONENTS: dict[str, str] = {
    "semantic-cache": "Semantic similarity cache to avoid redundant LLM calls",
    "reranker": "Cross-encoder reranker to improve retrieval precision",
    "cost-tracker": "Per-request token and cost tracking with breakdown reports",
    "agent-tools": "Pluggable tool definitions: web search, code search, vector search",
    "observability": "Full observability stack: tracer, feedback capture, cost tracker",
    "frontend": "Gradio/Streamlit frontend containerized separately",
    "evaluation": "Golden dataset, offline eval pipeline, and online monitor",
}

COMPONENT_MANIFEST: dict[str, list[str]] = {
    "semantic-cache": ["src.services.semantic_cache"],
    "reranker": ["src.components.reranker"],
    "cost-tracker": ["observability.cost_tracker"],
    "agent-tools": [
        "src.agents.tools.web_search",
        "src.agents.tools.code_search",
        "src.agents.tools.vector_search",
    ],
    "observability": [
        "observability.tracer",
        "observability.feedback",
        "observability.cost_tracker",
    ],
    "frontend": ["frontend.app", "frontend.requirements", "frontend.dockerfile"],
    "evaluation": [
        "evaluation.golden_dataset",
        "evaluation.offline_eval",
        "evaluation.online_monitor",
    ],
}


def run_add(component: str, project_dir: str) -> None:
    if component not in ADDABLE_COMPONENTS:
        console.print(
            f"[red]Error:[/red] Unknown component '{component}'. "
            f"Run [bold]create-ai-project list-components[/bold] to see available components."
        )
        raise typer.Exit(1)

    start = Path(project_dir).resolve()
    root = next(
        (p for p in [start, *start.parents] if (p / "pyproject.toml").exists()),
        None,
    )

    if root is None:
        console.print(
            f"[red]Error:[/red] No pyproject.toml found in '{start}' or any parent directory. "
            "Run this command from inside a create-ai-project project."
        )
        raise typer.Exit(1)

    pyproject = root / "pyproject.toml"

    # Read scaffold metadata from pyproject.toml
    with open(pyproject, "rb") as f:
        pyproject_data = tomllib.load(f)

    scaffold_meta = pyproject_data.get("tool", {}).get("ai-scaffold", {})
    if not scaffold_meta:
        console.print(
            "[yellow]Warning:[/yellow] No [tool.ai-scaffold] section found in pyproject.toml. "
            "Using defaults — some template variables may be generic."
        )

    context = ProjectContext(
        project_name=pyproject_data.get("project", {}).get("name", root.name),
        package_name=root.name,
        profile=scaffold_meta.get("profile", "rag"),
        llm_provider=scaffold_meta.get("llm_provider", "openai"),
        vector_db=scaffold_meta.get("vector_db", "chroma"),
        embedding_model=scaffold_meta.get(
            "embedding_model",
            DEFAULT_EMBEDDING.get(scaffold_meta.get("llm_provider", "openai"), "text-embedding-3-small"),
        ),
        llm_model=scaffold_meta.get(
            "llm_model",
            DEFAULT_MODEL.get(scaffold_meta.get("llm_provider", "openai"), "gpt-4o"),
        ),
    )

    from ai_scaffold.generator import engine

    keys = COMPONENT_MANIFEST[component]
    written = 0
    for key in keys:
        entry = MANIFEST_MAP[key]
        if not should_include(entry, context):
            continue
        dest = root / entry.output_path
        if dest.exists():
            console.print(f"[yellow]Skip[/yellow]  {entry.output_path} (already exists)")
            continue
        content = engine.render(key, context)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        console.print(f"[green]✓[/green]  {entry.output_path}")
        written += 1

    if written == 0:
        console.print("[yellow]Nothing new to add — all files already exist.[/yellow]")
    else:
        console.print(
            f"\n[green]Added component '[bold]{component}[/bold]' ({written} file(s)).[/green]"
        )
