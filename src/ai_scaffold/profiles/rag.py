from .base import Profile, register_profile
from .minimal import MINIMAL_MANIFEST

RAG_MANIFEST = MINIMAL_MANIFEST + [
    "src.dockerfile",
    "src.components.hybrid_retriever",
    "src.components.reranker",
    "src.services.rag_pipeline",
    "src.services.semantic_cache",
    "src.services.conversation",
    "src.services.query_rewriter",
    "src.services.query_router",
    "src.prompts.templates",
    "src.prompts.registry",
    "src.security.input_guard",
    "src.security.content_filter",
    "src.security.output_filter",
    "tests.test_retrieval",
    "tests.test_cache",
    "tests.test_routing",
]

register_profile(
    Profile(
        name="rag",
        description="RAG pipeline with hybrid search, semantic cache, security guards, and tests",
        manifest=RAG_MANIFEST,
    )
)
