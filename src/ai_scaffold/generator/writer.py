from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_scaffold.generator import engine
from ai_scaffold.generator.context import ProjectContext
from ai_scaffold.generator.engine import MANIFEST_MAP, ManifestEntry
from ai_scaffold.profiles.base import PROFILE_REGISTRY

console = Console(legacy_windows=False)

# ── Empty Python files created per profile ────────────────────────────────────
# Each string is a path relative to the project root.
# Files are written empty — no implementation code.

_MINIMAL_FILES: list[str] = [
    "src/__init__.py",
    "src/configs/__init__.py",
    "src/configs/config.py",
    "src/utils/__init__.py",
    "src/utils/logger.py",
    "src/utils/helpers.py",
    "tests/__init__.py",
    "tests/conftest.py",
]

_RAG_FILES: list[str] = [
    "src/__init__.py",
    "src/configs/__init__.py",
    "src/configs/config.py",
    "src/dependencies.py",
    # ingestion pipeline
    "src/ingestion/__init__.py",
    "src/ingestion/loader.py",
    "src/ingestion/chunker.py",
    "src/ingestion/cleaner.py",
    # embedding
    "src/embedding/__init__.py",
    "src/embedding/embedder.py",
    "src/embedding/utils.py",
    # vector store
    "src/vectorstore/__init__.py",
    "src/vectorstore/client.py",
    "src/vectorstore/indexer.py",
    "src/vectorstore/retriever.py",
    # core RAG
    "src/rag/__init__.py",
    "src/rag/pipeline.py",
    "src/rag/prompt.py",
    "src/rag/generator.py",
    # evaluation
    "src/evaluation/__init__.py",
    "src/evaluation/metrics.py",
    "src/evaluation/evaluator.py",
    # api layer
    "src/api/__init__.py",
    "src/api/routes.py",
    "src/api/schemas.py",
    "src/api/controllers.py",
    # caching
    "src/cache/__init__.py",
    "src/cache/redis_client.py",
    # observability
    "src/monitoring/__init__.py",
    "src/monitoring/tracing.py",
    "src/monitoring/metrics.py",
    # shared utils
    "src/utils/__init__.py",
    "src/utils/logger.py",
    "src/utils/helpers.py",
    # scripts
    "scripts/ingest_data.py",
    "scripts/build_index.py",
    "scripts/run_query.py",
    # tests
    "tests/__init__.py",
    "tests/conftest.py",
]

_AGENT_FILES: list[str] = [
    "src/__init__.py",
    "src/configs/__init__.py",
    "src/configs/config.py",
    "src/dependencies.py",
    # agents
    "src/agents/__init__.py",
    "src/agents/base_agent.py",
    "src/agents/chat_agent.py",
    "src/agents/planner_agent.py",
    "src/agents/executor_agent.py",
    # tools
    "src/tools/__init__.py",
    "src/tools/base_tool.py",
    "src/tools/web_search.py",
    "src/tools/calculator.py",
    "src/tools/db_tool.py",
    "src/tools/rag_tool.py",
    # llm layer
    "src/llm/__init__.py",
    "src/llm/client.py",
    "src/llm/prompts.py",
    "src/llm/output_parser.py",
    # memory
    "src/memory/__init__.py",
    "src/memory/short_term.py",
    "src/memory/long_term.py",
    "src/memory/episodic.py",
    # workflows / orchestration
    "src/workflows/__init__.py",
    "src/workflows/agent_loop.py",
    "src/workflows/planner_executor.py",
    "src/workflows/multi_agent.py",
    # retrieval subsystem
    "src/retrieval/__init__.py",
    "src/retrieval/pipeline.py",
    "src/retrieval/retriever.py",
    "src/retrieval/indexer.py",
    # evaluation
    "src/evaluation/__init__.py",
    "src/evaluation/agent_eval.py",
    "src/evaluation/datasets.py",
    # guardrails / safety
    "src/guardrails/__init__.py",
    "src/guardrails/validators.py",
    "src/guardrails/filters.py",
    # api layer
    "src/api/__init__.py",
    "src/api/routes.py",
    "src/api/schemas.py",
    "src/api/controllers.py",
    # caching
    "src/cache/__init__.py",
    "src/cache/redis_client.py",
    # observability
    "src/monitoring/__init__.py",
    "src/monitoring/tracing.py",
    "src/monitoring/metrics.py",
    # shared utils
    "src/utils/__init__.py",
    "src/utils/logger.py",
    "src/utils/helpers.py",
    # scripts
    "scripts/run_agent.py",
    "scripts/test_tools.py",
    # tests
    "tests/__init__.py",
    "tests/conftest.py",
]

# Full = RAG + Agent union (deduplicated, order preserved)
_seen: set[str] = set()
_FULL_FILES: list[str] = []
for _f in _RAG_FILES + _AGENT_FILES:
    if _f not in _seen:
        _seen.add(_f)
        _FULL_FILES.append(_f)

_PROFILE_FILES: dict[str, list[str]] = {
    "minimal": _MINIMAL_FILES,
    "rag": _RAG_FILES,
    "agent": _AGENT_FILES,
    "full": _FULL_FILES,
}

# ── Directories created with .gitkeep (non-Python, must not be empty in git) ──
_PROFILE_GITKEEP_DIRS: dict[str, list[str]] = {
    "minimal": ["data"],
    "rag":     ["data/raw", "data/processed", "data/embeddings", "notebooks"],
    "agent":   ["data/raw", "data/processed", "notebooks", "docker"],
    "full":    ["data/raw", "data/processed", "data/embeddings",
                "notebooks", "docker", "frontend"],
}


def should_include(entry: ManifestEntry, context: ProjectContext) -> bool:
    """Return False if any required flag is disabled on the context."""
    for flag in entry.requires:
        if not getattr(context, flag, True):
            return False
    return True


def write_project(context: ProjectContext) -> Path:
    # Trigger profile registration
    import ai_scaffold.profiles.minimal  # noqa: F401
    import ai_scaffold.profiles.rag      # noqa: F401
    import ai_scaffold.profiles.agent    # noqa: F401
    import ai_scaffold.profiles.full     # noqa: F401

    context = context.model_copy(update={"extra_deps": context.resolved_deps()})

    profile = PROFILE_REGISTRY[context.profile]
    root = Path.cwd() / context.project_name

    if root.exists():
        overwrite = typer.confirm(
            f"Directory '{root.name}' already exists. Overwrite?", default=False
        )
        if not overwrite:
            raise typer.Abort()

    # Config/doc files rendered from templates
    included_keys = [
        key for key in profile.manifest if should_include(MANIFEST_MAP[key], context)
    ]
    # Empty .py files for this profile
    py_files = _PROFILE_FILES.get(context.profile, [])
    # Data / non-package directories
    gitkeep_dirs = _PROFILE_GITKEEP_DIRS.get(context.profile, [])

    total = len(included_keys) + len(py_files) + len(gitkeep_dirs)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(
            f"[cyan]Scaffolding [bold]{context.project_name}[/bold]...",
            total=total,
        )

        # 1. Render config / documentation templates
        for key in included_keys:
            entry = MANIFEST_MAP[key]
            content = engine.render(key, context)
            dest = root / entry.output_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
            progress.advance(task)

        # 2. Create empty Python source files (structure only, no code)
        for rel_path in py_files:
            dest = root / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                dest.write_text("", encoding="utf-8")
            progress.advance(task)

        # 3. Create placeholder directories
        for rel_dir in gitkeep_dirs:
            d = root / rel_dir
            d.mkdir(parents=True, exist_ok=True)
            (d / ".gitkeep").write_text("", encoding="utf-8")
            progress.advance(task)

    return root
