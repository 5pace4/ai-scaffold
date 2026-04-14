from .base import Profile, register_profile
from .rag import RAG_MANIFEST

FULL_MANIFEST = RAG_MANIFEST + [
    "common.agents_md",
    "common.docker_compose",
    "docs.api_reference",  # agent profile omits this; add it here
]

# Deduplicate while preserving order
_seen: set[str] = set()
_deduped: list[str] = []
for _key in FULL_MANIFEST:
    if _key not in _seen:
        _seen.add(_key)
        _deduped.append(_key)
FULL_MANIFEST = _deduped

register_profile(
    Profile(
        name="full",
        description="Complete AI project: RAG + agents + evaluation + monitoring + frontend + docs",
        manifest=FULL_MANIFEST,
    )
)
