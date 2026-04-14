from .base import Profile, register_profile
from .rag import RAG_MANIFEST
from .agent import AGENT_MANIFEST

# Deduplicate while preserving order
_seen: set[str] = set()
_combined: list[str] = []
for _key in RAG_MANIFEST + AGENT_MANIFEST:
    if _key not in _seen:
        _seen.add(_key)
        _combined.append(_key)

FULL_MANIFEST = _combined + [
    "common.agents_md",
    "common.docker_compose",
    "common.claude_rules_code_style",
    "common.claude_rules_testing",
    "evaluation.golden_dataset",
    "evaluation.offline_eval",
    "evaluation.online_monitor",
    "observability.tracer",
    "observability.feedback",
    "observability.cost_tracker",
    "scripts.seed",
    "scripts.migrate",
    "scripts.healthcheck",
    "frontend.app",
    "frontend.requirements",
    "frontend.dockerfile",
    "docs.architecture",
    "docs.api_reference",
    "docs.deployment",
]

register_profile(
    Profile(
        name="full",
        description="Complete production AI app: RAG + agents + evaluation + observability + frontend + docs",
        manifest=FULL_MANIFEST,
    )
)
