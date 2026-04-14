from dataclasses import dataclass, field
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from ai_scaffold.generator.context import ProjectContext

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


@dataclass
class ManifestEntry:
    template_key: str
    template_file: str
    output_path: str
    # If any flag name in this set is False on the context, this file is skipped
    requires: set[str] = field(default_factory=set)


MANIFEST_MAP: dict[str, ManifestEntry] = {
    # ── Common ────────────────────────────────────────────────────────────────
    "common.gitignore": ManifestEntry(
        template_key="common.gitignore",
        template_file="common/gitignore.j2",
        output_path=".gitignore",
    ),
    "common.pyproject_toml": ManifestEntry(
        template_key="common.pyproject_toml",
        template_file="common/pyproject_toml.j2",
        output_path="pyproject.toml",
    ),
    "common.readme": ManifestEntry(
        template_key="common.readme",
        template_file="common/readme.j2",
        output_path="README.md",
    ),
    "common.claude_md": ManifestEntry(
        template_key="common.claude_md",
        template_file="common/claude_md.j2",
        output_path="CLAUDE.md",
    ),
    "common.agents_md": ManifestEntry(
        template_key="common.agents_md",
        template_file="common/agents_md.j2",
        output_path="AGENTS.md",
    ),
    "common.docker_compose": ManifestEntry(
        template_key="common.docker_compose",
        template_file="common/docker_compose.j2",
        output_path="docker-compose.yml",
        requires={"include_docker"},
    ),
    "common.claude_rules_code_style": ManifestEntry(
        template_key="common.claude_rules_code_style",
        template_file="common/claude/rules/code_style.j2",
        output_path=".claude/rules/code-style.md",
    ),
    "common.claude_rules_testing": ManifestEntry(
        template_key="common.claude_rules_testing",
        template_file="common/claude/rules/testing.j2",
        output_path=".claude/rules/testing.md",
    ),
    # ── App core ──────────────────────────────────────────────────────────────
    "app.main": ManifestEntry(
        template_key="app.main",
        template_file="app/main.j2",
        output_path="app/main.py",
    ),
    "app.config": ManifestEntry(
        template_key="app.config",
        template_file="app/config.j2",
        output_path="app/config.py",
    ),
    "app.models": ManifestEntry(
        template_key="app.models",
        template_file="app/models.j2",
        output_path="app/models.py",
    ),
    "app.dockerfile": ManifestEntry(
        template_key="app.dockerfile",
        template_file="app/dockerfile.j2",
        output_path="app/Dockerfile",
        requires={"include_docker"},
    ),
    # ── Components ────────────────────────────────────────────────────────────
    "app.components.hybrid_retriever": ManifestEntry(
        template_key="app.components.hybrid_retriever",
        template_file="app/components/hybrid_retriever.j2",
        output_path="app/components/hybrid_retriever.py",
    ),
    "app.components.reranker": ManifestEntry(
        template_key="app.components.reranker",
        template_file="app/components/reranker.j2",
        output_path="app/components/reranker.py",
    ),
    # ── Services ──────────────────────────────────────────────────────────────
    "app.services.rag_pipeline": ManifestEntry(
        template_key="app.services.rag_pipeline",
        template_file="app/services/rag_pipeline.j2",
        output_path="app/services/rag_pipeline.py",
    ),
    "app.services.semantic_cache": ManifestEntry(
        template_key="app.services.semantic_cache",
        template_file="app/services/semantic_cache.j2",
        output_path="app/services/semantic_cache.py",
    ),
    "app.services.conversation": ManifestEntry(
        template_key="app.services.conversation",
        template_file="app/services/conversation.j2",
        output_path="app/services/conversation.py",
    ),
    "app.services.query_rewriter": ManifestEntry(
        template_key="app.services.query_rewriter",
        template_file="app/services/query_rewriter.j2",
        output_path="app/services/query_rewriter.py",
    ),
    "app.services.query_router": ManifestEntry(
        template_key="app.services.query_router",
        template_file="app/services/query_router.j2",
        output_path="app/services/query_router.py",
    ),
    # ── Prompts ───────────────────────────────────────────────────────────────
    "app.prompts.templates": ManifestEntry(
        template_key="app.prompts.templates",
        template_file="app/prompts/templates.j2",
        output_path="app/prompts/templates.py",
    ),
    "app.prompts.registry": ManifestEntry(
        template_key="app.prompts.registry",
        template_file="app/prompts/registry.j2",
        output_path="app/prompts/registry.py",
    ),
    # ── Agents ────────────────────────────────────────────────────────────────
    "app.agents.document_grader": ManifestEntry(
        template_key="app.agents.document_grader",
        template_file="app/agents/document_grader.j2",
        output_path="app/agents/document_grader.py",
    ),
    "app.agents.query_decomposer": ManifestEntry(
        template_key="app.agents.query_decomposer",
        template_file="app/agents/query_decomposer.j2",
        output_path="app/agents/query_decomposer.py",
    ),
    "app.agents.adaptive_router": ManifestEntry(
        template_key="app.agents.adaptive_router",
        template_file="app/agents/adaptive_router.j2",
        output_path="app/agents/adaptive_router.py",
    ),
    "app.agents.tools.web_search": ManifestEntry(
        template_key="app.agents.tools.web_search",
        template_file="app/agents/tools/web_search.j2",
        output_path="app/agents/tools/web_search.py",
    ),
    "app.agents.tools.code_search": ManifestEntry(
        template_key="app.agents.tools.code_search",
        template_file="app/agents/tools/code_search.j2",
        output_path="app/agents/tools/code_search.py",
    ),
    "app.agents.tools.vector_search": ManifestEntry(
        template_key="app.agents.tools.vector_search",
        template_file="app/agents/tools/vector_search.j2",
        output_path="app/agents/tools/vector_search.py",
    ),
    # ── Security ──────────────────────────────────────────────────────────────
    "app.security.input_guard": ManifestEntry(
        template_key="app.security.input_guard",
        template_file="app/security/input_guard.j2",
        output_path="app/security/input_guard.py",
    ),
    "app.security.content_filter": ManifestEntry(
        template_key="app.security.content_filter",
        template_file="app/security/content_filter.j2",
        output_path="app/security/content_filter.py",
    ),
    "app.security.output_filter": ManifestEntry(
        template_key="app.security.output_filter",
        template_file="app/security/output_filter.j2",
        output_path="app/security/output_filter.py",
    ),
    # ── Evaluation ────────────────────────────────────────────────────────────
    "evaluation.golden_dataset": ManifestEntry(
        template_key="evaluation.golden_dataset",
        template_file="evaluation/golden_dataset.j2",
        output_path="evaluation/golden_dataset.json",
    ),
    "evaluation.offline_eval": ManifestEntry(
        template_key="evaluation.offline_eval",
        template_file="evaluation/offline_eval.j2",
        output_path="evaluation/offline_eval.py",
    ),
    "evaluation.online_monitor": ManifestEntry(
        template_key="evaluation.online_monitor",
        template_file="evaluation/online_monitor.j2",
        output_path="evaluation/online_monitor.py",
    ),
    # ── Observability ─────────────────────────────────────────────────────────
    "observability.tracer": ManifestEntry(
        template_key="observability.tracer",
        template_file="observability/tracer.j2",
        output_path="observability/tracer.py",
    ),
    "observability.feedback": ManifestEntry(
        template_key="observability.feedback",
        template_file="observability/feedback.j2",
        output_path="observability/feedback.py",
    ),
    "observability.cost_tracker": ManifestEntry(
        template_key="observability.cost_tracker",
        template_file="observability/cost_tracker.j2",
        output_path="observability/cost_tracker.py",
    ),
    # ── Scripts ───────────────────────────────────────────────────────────────
    "scripts.seed": ManifestEntry(
        template_key="scripts.seed",
        template_file="scripts/seed.j2",
        output_path="scripts/seed.py",
    ),
    "scripts.migrate": ManifestEntry(
        template_key="scripts.migrate",
        template_file="scripts/migrate.j2",
        output_path="scripts/migrate.py",
    ),
    "scripts.healthcheck": ManifestEntry(
        template_key="scripts.healthcheck",
        template_file="scripts/healthcheck.j2",
        output_path="scripts/healthcheck.py",
    ),
    # ── Frontend ──────────────────────────────────────────────────────────────
    "frontend.app": ManifestEntry(
        template_key="frontend.app",
        template_file="frontend/app.j2",
        output_path="frontend/app.py",
        requires={"include_frontend"},
    ),
    "frontend.requirements": ManifestEntry(
        template_key="frontend.requirements",
        template_file="frontend/requirements.j2",
        output_path="frontend/requirements.txt",
        requires={"include_frontend"},
    ),
    "frontend.dockerfile": ManifestEntry(
        template_key="frontend.dockerfile",
        template_file="frontend/dockerfile.j2",
        output_path="frontend/Dockerfile",
        requires={"include_frontend", "include_docker"},
    ),
    # ── Tests ─────────────────────────────────────────────────────────────────
    "tests.test_retrieval": ManifestEntry(
        template_key="tests.test_retrieval",
        template_file="tests/test_retrieval.j2",
        output_path="tests/test_retrieval.py",
    ),
    "tests.test_cache": ManifestEntry(
        template_key="tests.test_cache",
        template_file="tests/test_cache.j2",
        output_path="tests/test_cache.py",
    ),
    "tests.test_routing": ManifestEntry(
        template_key="tests.test_routing",
        template_file="tests/test_routing.j2",
        output_path="tests/test_routing.py",
    ),
    # ── Docs ──────────────────────────────────────────────────────────────────
    "docs.architecture": ManifestEntry(
        template_key="docs.architecture",
        template_file="docs/architecture.j2",
        output_path="docs/architecture.md",
    ),
    "docs.api_reference": ManifestEntry(
        template_key="docs.api_reference",
        template_file="docs/api_reference.j2",
        output_path="docs/api-reference.md",
    ),
    "docs.deployment": ManifestEntry(
        template_key="docs.deployment",
        template_file="docs/deployment.j2",
        output_path="docs/deployment.md",
    ),
}

_env: Environment | None = None


def get_env() -> Environment:
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
            autoescape=False,
        )
    return _env


def render(template_key: str, context: ProjectContext) -> str:
    entry = MANIFEST_MAP[template_key]
    tpl = get_env().get_template(entry.template_file)
    return tpl.render(**context.model_dump())
