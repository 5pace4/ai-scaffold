import typer
from rich.console import Console
from rich.table import Table

from ai_scaffold import __version__

app = typer.Typer(
    name="create-ai-project",
    help="Scaffold production-ready AI projects with clean architecture.",
    rich_markup_mode="rich",
    no_args_is_help=True,
)

console = Console(legacy_windows=False)


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", is_eager=True, help="Show version and exit."
    ),
) -> None:
    if version:
        console.print(f"create-ai-project [bold cyan]v{__version__}[/bold cyan]")
        raise typer.Exit()


@app.command()
def new(
    project_name: str = typer.Argument(..., help="Name of the project to create."),
    profile: str = typer.Option(
        "rag", "--profile", "-p", help="Project profile: minimal, rag, agent, full."
    ),
    llm: str | None = typer.Option(
        None,
        "--llm",
        help="LLM provider: openai, anthropic, groq, ollama, azure-openai.",
    ),
    vector_db: str | None = typer.Option(
        None,
        "--vector-db",
        help="Vector database: chroma, qdrant, pinecone, weaviate, pgvector, none.",
    ),
    no_docker: bool = typer.Option(False, "--no-docker", help="Skip Docker files."),
    no_frontend: bool = typer.Option(
        False, "--no-frontend", help="Skip frontend/ directory."
    ),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git init."),
    no_uv: bool = typer.Option(False, "--no-uv", help="Skip uv sync in new project."),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Skip interactive prompts, use defaults."
    ),
    author_name: str = typer.Option("", "--author-name", help="Author name."),
    author_email: str = typer.Option("", "--author-email", help="Author email."),
) -> None:
    """Create a new AI project with clean architecture."""
    from ai_scaffold.commands.new import run_new

    run_new(
        project_name=project_name,
        profile=profile,
        llm=llm,
        vector_db=vector_db,
        include_docker=not no_docker,
        include_frontend=not no_frontend,
        include_git=not no_git,
        include_uv=not no_uv,
        yes=yes,
        author_name=author_name,
        author_email=author_email,
    )


@app.command()
def add(
    component: str = typer.Argument(
        ...,
        help="Component to add: semantic-cache, reranker, cost-tracker, agent-tools, observability, frontend, evaluation.",
    ),
    project_dir: str = typer.Option(
        ".", "--project-dir", help="Path to existing project."
    ),
) -> None:
    """Add a component to an existing AI project."""
    from ai_scaffold.commands.add import run_add

    run_add(component=component, project_dir=project_dir)


@app.command("list-profiles")
def list_profiles() -> None:
    """List all available project profiles."""
    # Import to trigger registration
    import ai_scaffold.profiles.minimal  # noqa: F401
    import ai_scaffold.profiles.rag  # noqa: F401
    import ai_scaffold.profiles.agent  # noqa: F401
    import ai_scaffold.profiles.full  # noqa: F401
    from ai_scaffold.profiles.base import PROFILE_REGISTRY

    table = Table(title="Available Profiles", show_lines=True)
    table.add_column("Profile", style="bold cyan")
    table.add_column("Description")
    table.add_column("Files", justify="right")

    for name, profile in PROFILE_REGISTRY.items():
        table.add_row(name, profile.description, str(len(profile.manifest)))

    console.print(table)


@app.command("list-components")
def list_components() -> None:
    """List all components that can be added to an existing project."""
    from ai_scaffold.commands.add import ADDABLE_COMPONENTS

    table = Table(title="Addable Components", show_lines=True)
    table.add_column("Component", style="bold cyan")
    table.add_column("Description")

    for name, desc in ADDABLE_COMPONENTS.items():
        table.add_row(name, desc)

    console.print(table)


if __name__ == "__main__":
    app()
