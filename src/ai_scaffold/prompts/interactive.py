import questionary
from rich.console import Console
from rich.panel import Panel

from ai_scaffold.generator.context import (
    DEFAULT_EMBEDDING,
    DEFAULT_MODEL,
    LLM_PROVIDERS,
    VECTOR_DBS,
    ProjectContext,
)

console = Console()


def run_wizard(
    project_name: str,
    profile: str,
    llm_provider: str | None = None,
    vector_db: str | None = None,
    include_docker: bool = True,
    include_frontend: bool = True,
    include_git: bool = True,
    include_uv: bool = True,
    author_name: str = "",
    author_email: str = "",
) -> ProjectContext:
    """Run the interactive setup wizard and return a fully populated ProjectContext."""
    console.print(
        Panel.fit(
            f"[bold cyan]create-ai-project[/bold cyan]  •  profile: [bold]{profile}[/bold]",
            border_style="cyan",
        )
    )

    if llm_provider is None:
        llm_provider = questionary.select(
            "LLM provider?",
            choices=LLM_PROVIDERS,
            default="openai",
        ).ask()
        if llm_provider is None:
            raise KeyboardInterrupt

    if vector_db is None:
        vector_db = questionary.select(
            "Vector database?",
            choices=VECTOR_DBS,
            default="chroma",
        ).ask()
        if vector_db is None:
            raise KeyboardInterrupt

    default_embedding = DEFAULT_EMBEDDING.get(llm_provider, "text-embedding-3-small")
    embedding_model = questionary.text(
        "Embedding model?",
        default=default_embedding,
    ).ask()
    if embedding_model is None:
        raise KeyboardInterrupt

    llm_model = DEFAULT_MODEL.get(llm_provider, "gpt-4o")

    return ProjectContext(
        project_name=project_name,
        package_name=project_name,
        profile=profile,
        llm_provider=llm_provider,
        vector_db=vector_db,
        embedding_model=embedding_model,
        llm_model=llm_model,
        include_docker=include_docker,
        include_frontend=include_frontend,
        include_git=include_git,
        include_uv=include_uv,
        author_name=author_name,
        author_email=author_email,
    )


def build_context_with_defaults(
    project_name: str,
    profile: str,
    llm_provider: str | None = None,
    vector_db: str | None = None,
    include_docker: bool = True,
    include_frontend: bool = True,
    include_git: bool = True,
    include_uv: bool = True,
    author_name: str = "",
    author_email: str = "",
) -> ProjectContext:
    """Build a ProjectContext using defaults (no interactive prompts)."""
    resolved_llm = llm_provider or "openai"
    resolved_db = vector_db or "chroma"

    return ProjectContext(
        project_name=project_name,
        package_name=project_name,
        profile=profile,
        llm_provider=resolved_llm,
        vector_db=resolved_db,
        embedding_model=DEFAULT_EMBEDDING.get(resolved_llm, "text-embedding-3-small"),
        llm_model=DEFAULT_MODEL.get(resolved_llm, "gpt-4o"),
        include_docker=include_docker,
        include_frontend=include_frontend,
        include_git=include_git,
        include_uv=include_uv,
        author_name=author_name,
        author_email=author_email,
    )
