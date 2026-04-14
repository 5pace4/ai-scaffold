from .base import Profile, register_profile
from .minimal import MINIMAL_MANIFEST

AGENT_MANIFEST = MINIMAL_MANIFEST + [
    "app.dockerfile",
    "app.agents.document_grader",
    "app.agents.query_decomposer",
    "app.agents.adaptive_router",
    "app.agents.tools.web_search",
    "app.agents.tools.code_search",
    "app.agents.tools.vector_search",
    "app.services.query_rewriter",
    "app.services.query_router",
    "app.prompts.templates",
    "app.prompts.registry",
    "tests.test_routing",
]

register_profile(
    Profile(
        name="agent",
        description="Agentic app with self-correcting retrieval, tool use, and LLM-driven routing",
        manifest=AGENT_MANIFEST,
    )
)
