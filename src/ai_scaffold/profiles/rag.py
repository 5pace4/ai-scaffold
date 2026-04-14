from .base import Profile, register_profile
from .minimal import MINIMAL_MANIFEST

RAG_MANIFEST = MINIMAL_MANIFEST + [
    "src.dockerfile",
    "docs.architecture",
    "docs.api_reference",
    "docs.deployment",
]

register_profile(
    Profile(
        name="rag",
        description="RAG skeleton: ingestion, embedding, vectorstore, rag, evaluation, api, cache, monitoring",
        manifest=RAG_MANIFEST,
    )
)
