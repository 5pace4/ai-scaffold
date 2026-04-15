from pydantic import BaseModel, Field, field_validator

LLM_PROVIDERS = ["openai", "anthropic", "groq", "ollama", "azure-openai", "none"]
VECTOR_DBS = ["chroma", "qdrant", "pinecone", "weaviate", "pgvector", "none"]

DEFAULT_EMBEDDING: dict[str, str] = {
    "openai": "text-embedding-3-small",
    "anthropic": "text-embedding-3-small",
    "groq": "nomic-embed-text",
    "ollama": "nomic-embed-text",
    "azure-openai": "text-embedding-ada-002",
    "none": "none",
}

DEFAULT_MODEL: dict[str, str] = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-haiku-4-5-20251001",
    "groq": "llama-3.1-8b-instant",
    "ollama": "llama3.2",
    "azure-openai": "gpt-4o-mini",
    "none": "none",
}

# Only direct SDK deps — no langchain
LLM_DEPS: dict[str, list[str]] = {
    "openai": ["openai>=1.50"],
    "anthropic": ["anthropic>=0.37"],
    "groq": ["groq>=0.11"],
    "ollama": ["ollama>=0.3"],
    "azure-openai": ["openai>=1.50"],
    "none": [],
}

VECTOR_DB_DEPS: dict[str, list[str]] = {
    "chroma": ["chromadb>=0.5"],
    "qdrant": ["qdrant-client>=1.9"],
    "pinecone": ["pinecone-client>=3"],
    "weaviate": ["weaviate-client>=4"],
    "pgvector": ["pgvector>=0.3", "psycopg2-binary>=2.9", "sqlalchemy>=2"],
    "none": [],
}


class ProjectContext(BaseModel):
    project_name: str
    package_name: str
    profile: str
    llm_provider: str
    vector_db: str
    embedding_model: str
    llm_model: str
    description: str = "AI application scaffolded with create-ai-project"
    python_version: str = "3.13"
    include_docker: bool = True
    include_frontend: bool = True
    include_git: bool = True
    author_name: str = ""
    author_email: str = ""
    scaffold_version: str = "0.1.2"
    extra_deps: list[str] = Field(default_factory=list)

    @field_validator("package_name", mode="before")
    @classmethod
    def normalize_package_name(cls, v: str) -> str:
        return v.replace("-", "_").replace(" ", "_").lower()

    @field_validator("llm_provider")
    @classmethod
    def validate_llm_provider(cls, v: str) -> str:
        if v not in LLM_PROVIDERS:
            raise ValueError(f"llm_provider must be one of {LLM_PROVIDERS}, got '{v}'")
        return v

    @field_validator("vector_db")
    @classmethod
    def validate_vector_db(cls, v: str) -> str:
        if v not in VECTOR_DBS:
            raise ValueError(f"vector_db must be one of {VECTOR_DBS}, got '{v}'")
        return v

    def resolved_deps(self) -> list[str]:
        """Return minimal deps for the generated project."""
        base = [
            "uvicorn[standard]>=0.30",
        ]
        return base + LLM_DEPS.get(self.llm_provider, []) + VECTOR_DB_DEPS.get(self.vector_db, []) + self.extra_deps
