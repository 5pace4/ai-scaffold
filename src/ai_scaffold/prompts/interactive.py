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

console = Console(legacy_windows=False)


def run_wizard(
    project_name: str,
    profile: str,
    llm_provider: str | None = None,
    vector_db: str | None = None,
    include_docker: bool = True,
    include_frontend: bool = True,
    include_git: bool = True,
    author_name: str = "",
    author_email: str = "",
    description: str = "",
) -> ProjectContext:
    """Run the interactive setup wizard and return a fully populated ProjectContext."""
    console.print(
        Panel.fit(
            f"[bold cyan]create-ai-project[/bold cyan]  •  profile: [bold]{profile}[/bold]",
            border_style="cyan",
        )
    )

    # ── Project description ───────────────────────────────────────────────────
    if not description:
        description = questionary.text(
            "Project description?",
            default=f"{project_name} — AI application",
        ).ask()
        if description is None:
            raise KeyboardInterrupt
        description = description.strip() or f"{project_name} — AI application"

    # ── Author ────────────────────────────────────────────────────────────────
    if not author_name:
        author_name = questionary.text(
            "Author name? (leave blank to skip)",
            default="",
        ).ask()
        if author_name is None:
            raise KeyboardInterrupt
        author_name = author_name.strip()

    if author_name and not author_email:
        author_email = questionary.text(
            "Author email? (leave blank to skip)",
            default="",
        ).ask()
        if author_email is None:
            raise KeyboardInterrupt
        author_email = author_email.strip()

    # ── LLM provider ──────────────────────────────────────────────────────────
    if llm_provider is None:
        llm_provider = questionary.select(
            "LLM provider?",
            choices=LLM_PROVIDERS,
            default="openai",
        ).ask()
        if llm_provider is None:
            raise KeyboardInterrupt

    # ── LLM model ─────────────────────────────────────────────────────────────
    default_model = DEFAULT_MODEL.get(llm_provider, "none")
    if llm_provider != "none":
        llm_model = questionary.text(
            "LLM model?",
            default=default_model,
        ).ask()
        if llm_model is None:
            raise KeyboardInterrupt
        llm_model = llm_model.strip() or default_model
    else:
        llm_model = "none"

    # ── Vector DB ─────────────────────────────────────────────────────────────
    if vector_db is None:
        vector_db = questionary.select(
            "Vector database?",
            choices=VECTOR_DBS,
            default="none",
        ).ask()
        if vector_db is None:
            raise KeyboardInterrupt

    # ── Embedding model ───────────────────────────────────────────────────────
    default_embedding = DEFAULT_EMBEDDING.get(llm_provider, "none")
    if llm_provider != "none" or vector_db != "none":
        embedding_model = questionary.text(
            "Embedding model?",
            default=default_embedding,
        ).ask()
        if embedding_model is None:
            raise KeyboardInterrupt
        embedding_model = embedding_model.strip() or default_embedding
    else:
        embedding_model = "none"

    return ProjectContext(
        project_name=project_name,
        package_name=project_name,
        profile=profile,
        llm_provider=llm_provider,
        vector_db=vector_db,
        embedding_model=embedding_model,
        llm_model=llm_model,
        description=description,
        include_docker=include_docker,
        include_frontend=include_frontend,
        include_git=include_git,
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
    author_name: str = "",
    author_email: str = "",
    description: str = "",
) -> ProjectContext:
    """Build a ProjectContext using defaults (no interactive prompts)."""
    resolved_llm = llm_provider or "none"
    resolved_db = vector_db or "none"

    return ProjectContext(
        project_name=project_name,
        package_name=project_name,
        profile=profile,
        llm_provider=resolved_llm,
        vector_db=resolved_db,
        embedding_model=DEFAULT_EMBEDDING.get(resolved_llm, "none"),
        llm_model=DEFAULT_MODEL.get(resolved_llm, "none"),
        description=description or f"{project_name} — AI application",
        include_docker=include_docker,
        include_frontend=include_frontend,
        include_git=include_git,
        author_name=author_name,
        author_email=author_email,
    )
