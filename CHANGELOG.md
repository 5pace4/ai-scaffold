# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), [Semantic Versioning](https://semver.org/)

## [Unreleased]

## [0.1.4] - 2026-04-15

### Added
- `create-ai-project new <name>` command with interactive wizard
- Four project profiles: `minimal`, `rag`, `agent`, `full`
- LLM providers: `openai`, `anthropic`, `groq`, `ollama`, `azure-openai`, `none`
- Vector databases: `chroma`, `qdrant`, `pinecone`, `weaviate`, `pgvector`, `none`
- Interactive wizard collects project description, author name, author email, LLM provider, model, vector DB, and embedding model
- `--yes` flag to skip wizard and scaffold with defaults
- Profile-based folder structure: creates directories and empty `.py` files — no implementation code written
- Minimal direct SDK dependencies only (no LangChain); deps auto-selected based on chosen provider and DB
- Git repository initialization on project creation
- Generated `pyproject.toml` with Hatchling build backend and correct `src/` layout
- `.env.example` with provider/DB-specific environment variable placeholders
- `requirements.txt` with resolved minimal dependencies
- `README.md`, `CLAUDE.md`, `AGENTS.md` generated per project
- `Dockerfile` and `docker-compose.yml` (when Docker is enabled)
- GitHub Actions CI workflow in generated projects
- `--version` flag (`create-ai-project --version`)
