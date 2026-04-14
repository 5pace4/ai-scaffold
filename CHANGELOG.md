# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]

## [0.1.0] - 2026-04-14

### Added
- `create-ai-project new` command with interactive wizard
- Four profiles: `minimal`, `rag`, `agent`, `full`
- LLM providers: `openai`, `anthropic`, `groq`, `ollama`, `azure-openai`
- Vector DBs: `chroma`, `qdrant`, `pinecone`, `weaviate`, `pgvector`, `none`
- `create-ai-project add <component>` to extend existing projects
- `create-ai-project list-profiles` and `list-components`
- Git init + initial commit on project creation
- `uv sync` auto-install in generated project
- Full template library: RAG pipeline, agents, security guards, evaluation, observability, frontend
- GitHub Actions CI + Trusted Publishing to PyPI
