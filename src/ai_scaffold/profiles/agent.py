from .base import Profile, register_profile
from .minimal import MINIMAL_MANIFEST

AGENT_MANIFEST = MINIMAL_MANIFEST + [
    "src.dockerfile",
    "src.agents.document_grader",
    "src.agents.query_decomposer",
    "src.agents.adaptive_router",
    "src.agents.tools.web_search",
    "src.agents.tools.code_search",
    "src.agents.tools.vector_search",
    "src.services.query_rewriter",
    "src.services.query_router",
    "src.prompts.templates",
    "src.prompts.registry",
    "tests.test_routing",
]

register_profile(
    Profile(
        name="agent",
        description="Agentic app with self-correcting retrieval, tool use, and LLM-driven routing",
        manifest=AGENT_MANIFEST,
    )
)
