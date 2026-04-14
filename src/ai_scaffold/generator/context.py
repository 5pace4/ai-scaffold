from pydantic import BaseModel, Field, field_validator

LLM_PROVIDERS = ["openai", "anthropic", "groq", "ollama", "azure-openai"]
VECTOR_DBS = ["chroma", "qdrant", "pinecone", "weaviate", "pgvector", "none"]

DEFAULT_EMBEDDING: dict[str, str] = {
    "openai": "text-embedding-3-small",
    "anthropic": "text-embedding-3-small",
    "groq": "text-embedding-3-small",
    "ollama": "nomic-embed-text",
    "azure-openai": "text-embedding-3-small",
}

DEFAULT_MODEL: dict[str, str] = {
    "openai": "gpt-4o",
    "anthropic": "claude-sonnet-4-5",
    "groq": "llama-3.3-70b-versatile",
    "ollama": "llama3.2",
    "azure-openai": "gpt-4o",
}

# Deps added to generated project's pyproject.toml per provider/db
LLM_DEPS: dict[str, list[str]] = {
    "openai": ["openai>=1.50", "langchain-openai>=0.2"],
    "anthropic": ["anthropic>=0.37", "langchain-anthropic>=0.2"],
    "groq": ["groq>=0.11", "langchain-groq>=0.2"],
    "ollama": ["ollama>=0.3", "langchain-ollama>=0.2"],
    "azure-openai": ["openai>=1.50", "langchain-openai>=0.2"],
}

VECTOR_DB_DEPS: dict[str, list[str]] = {
    "chroma": ["chromadb>=0.5"],
    "qdrant": ["qdrant-client>=1.11", "langchain-qdrant>=0.2"],
    "pinecone": ["pinecone-client>=5", "langchain-pinecone>=0.2"],
    "weaviate": ["weaviate-client>=4", "langchain-weaviate>=0.0.3"],
    "pgvector": ["pgvector>=0.3", "psycopg2-binary>=2.9", "langchain-postgres>=0.0.12"],
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
    python_version: str = "3.13"
    include_docker: bool = True
    include_frontend: bool = True
    include_git: bool = True
    include_uv: bool = True
    author_name: str = ""
    author_email: str = ""
    scaffold_version: str = "0.1.0"
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
        """Return all deps to install in the generated project."""
        base = [
            "fastapi>=0.115",
            "uvicorn[standard]>=0.32",
            "pydantic>=2",
            "pydantic-settings>=2",
            "python-dotenv>=1",
            "langchain>=0.3",
            "langchain-community>=0.3",
            "tiktoken>=0.7",
            "httpx>=0.27",
        ]
        return base + LLM_DEPS.get(self.llm_provider, []) + VECTOR_DB_DEPS.get(self.vector_db, []) + self.extra_deps
