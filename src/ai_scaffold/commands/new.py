from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from ai_scaffold.generator.context import LLM_PROVIDERS, VECTOR_DBS, ProjectContext
from ai_scaffold.generator.writer import write_project
from ai_scaffold.profiles.base import PROFILE_REGISTRY

console = Console(legacy_windows=False)

VALID_PROFILES = ["minimal", "rag", "agent", "full"]


def run_new(
    project_name: str,
    profile: str,
    llm: str | None,
    vector_db: str | None,
    include_docker: bool,
    include_frontend: bool,
    include_git: bool,
    yes: bool,
    author_name: str,
    author_email: str,
    description: str,
) -> None:
    # ── Validate profile ──────────────────────────────────────────────────────
    if profile not in VALID_PROFILES:
        console.print(
            f"[red]Error:[/red] Unknown profile '{profile}'. "
            f"Valid: {', '.join(VALID_PROFILES)}"
        )
        raise typer.Exit(1)

    # ── Validate project name ─────────────────────────────────────────────────
    safe_name = project_name.replace("-", "_").replace(" ", "_")
    if not safe_name.isidentifier():
        console.print(
            f"[red]Error:[/red] '{project_name}' is not a valid project name. "
            "Use letters, digits, hyphens, or underscores."
        )
        raise typer.Exit(1)

    # ── Validate LLM / vector-db if supplied via flags ────────────────────────
    if llm is not None and llm not in LLM_PROVIDERS:
        console.print(
            f"[red]Error:[/red] Unknown LLM provider '{llm}'. "
            f"Valid: {', '.join(LLM_PROVIDERS)}"
        )
        raise typer.Exit(1)

    if vector_db is not None and vector_db not in VECTOR_DBS:
        console.print(
            f"[red]Error:[/red] Unknown vector DB '{vector_db}'. "
            f"Valid: {', '.join(VECTOR_DBS)}"
        )
        raise typer.Exit(1)

    # ── Build ProjectContext ───────────────────────────────────────────────────
    needs_wizard = not yes

    if needs_wizard:
        from ai_scaffold.prompts.interactive import run_wizard

        try:
            context = run_wizard(
                project_name=project_name,
                profile=profile,
                llm_provider=llm,
                vector_db=vector_db,
                include_docker=include_docker,
                include_frontend=include_frontend,
                include_git=include_git,
                author_name=author_name,
                author_email=author_email,
                description=description,
            )
        except KeyboardInterrupt:
            console.print("\n[yellow]Aborted.[/yellow]")
            raise typer.Exit(0)
    else:
        from ai_scaffold.prompts.interactive import build_context_with_defaults

        context = build_context_with_defaults(
            project_name=project_name,
            profile=profile,
            llm_provider=llm,
            vector_db=vector_db,
            include_docker=include_docker,
            include_frontend=include_frontend,
            include_git=include_git,
            author_name=author_name,
            author_email=author_email,
            description=description,
        )

    # ── Generate files ────────────────────────────────────────────────────────
    try:
        project_root = write_project(context)
    except typer.Abort:
        raise typer.Exit(0)

    # ── Git init ──────────────────────────────────────────────────────────────
    if include_git:
        from ai_scaffold.integrations.git import init as git_init

        git_init(project_root)

    # ── Success banner ────────────────────────────────────────────────────────
    _print_success(context, project_root)


def _print_success(context: ProjectContext, project_root: Path) -> None:
    lines = [
        f"  [bold]cd {context.project_name}[/bold]",
        "  [bold]cp .env.example .env[/bold]  and fill in your API keys",
        "  [bold]uv sync[/bold]  (or pip install -r requirements.txt)",
        "  [bold]uvicorn src.main:app --reload[/bold]",
    ]

    db_line = f"[cyan]{context.vector_db}[/cyan]" if context.vector_db != "none" else "[dim]none[/dim]"
    llm_line = f"[cyan]{context.llm_provider}[/cyan]" if context.llm_provider != "none" else "[dim]none[/dim]"

    console.print(
        Panel(
            f"[bold green]Project '[bold]{context.project_name}[/bold]' created![/bold green]\n\n"
            + f"Profile:    [cyan]{context.profile}[/cyan]\n"
            + f"LLM:        {llm_line}  ({context.llm_model})\n"
            + f"Vector DB:  {db_line}\n\n"
            + "[bold]Next steps:[/bold]\n"
            + "\n".join(lines),
            border_style="green",
            title="[bold]create-ai-project[/bold]",
        )
    )
