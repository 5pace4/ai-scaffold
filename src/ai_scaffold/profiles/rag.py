from .base import Profile, register_profile
from .minimal import MINIMAL_MANIFEST

RAG_MANIFEST = MINIMAL_MANIFEST + [
    "app.dockerfile",
    "app.components.hybrid_retriever",
    "app.components.reranker",
    "app.services.rag_pipeline",
    "app.services.semantic_cache",
    "app.services.conversation",
    "app.services.query_rewriter",
    "app.services.query_router",
    "app.prompts.templates",
    "app.prompts.registry",
    "app.security.input_guard",
    "app.security.content_filter",
    "app.security.output_filter",
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
