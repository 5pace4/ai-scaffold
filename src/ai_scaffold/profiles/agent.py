from .base import Profile, register_profile
from .minimal import MINIMAL_MANIFEST

AGENT_MANIFEST = MINIMAL_MANIFEST + [
    "src.dockerfile",
    "docs.architecture",
    "docs.deployment",
]

register_profile(
    Profile(
        name="agent",
        description="Agent skeleton: agents, tools, llm, memory, workflows, retrieval, guardrails, api, cache, monitoring",
        manifest=AGENT_MANIFEST,
    )
)
