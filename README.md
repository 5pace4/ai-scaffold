# create-ai-project

[![PyPI](https://img.shields.io/pypi/v/create-ai-project)](https://pypi.org/project/create-ai-project/)
[![Python](https://img.shields.io/pypi/pyversions/create-ai-project)](https://pypi.org/project/create-ai-project/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**Scaffold production-ready AI project structures in seconds.**

`create-ai-project` generates a clean folder structure with empty files for your AI project — no boilerplate code, no locked-in frameworks. You get the architecture, you write the logic.

```bash
pip install create-ai-project
create-ai-project new my-rag-app --profile rag --llm openai --vector-db chroma
```

---

## Why

Starting an AI project means the same directory decisions every time — where does the RAG pipeline go? Where do agents live? How do you separate ingestion from retrieval? This tool answers those questions by giving you a battle-tested folder structure upfront, so you can start writing code immediately.

---

## Install

```bash
pip install create-ai-project
```

Requires Python 3.13+. Works with `uv`, `pip`, and `pipx`.

---

## Quick Start

```bash
# Interactive wizard — asks LLM provider, vector DB, author, etc.
create-ai-project new my-project

# Non-interactive with flags
create-ai-project new my-project --profile agent --llm anthropic --vector-db qdrant -y
```

After scaffolding, every `.py` file exists but is empty. Open the files and start building.

---

## Profiles

| Profile | What gets scaffolded |
|---|---|
| `minimal` | `src/` skeleton, configs, utils, tests |
| `rag` | Ingestion → Embedding → Vector store → RAG pipeline + API, cache, monitoring |
| `agent` | Agents, tools, LLM layer, memory, workflows, guardrails + API, cache, monitoring |
| `full` | RAG + Agent combined, plus a `frontend/` directory |

### RAG layout

```
my-rag-app/
├── src/
│   ├── main.py
│   ├── configs/config.py
│   ├── ingestion/          loader · chunker · cleaner
│   ├── embedding/          embedder · utils
│   ├── vectorstore/        client · indexer · retriever
│   ├── rag/                pipeline · prompt · generator
│   ├── evaluation/         metrics · evaluator
│   ├── api/                routes · schemas · controllers
│   ├── cache/              redis_client
│   ├── monitoring/         tracing · metrics
│   └── utils/              logger · helpers
├── data/raw/  data/processed/  data/embeddings/
├── notebooks/  scripts/  tests/
├── .env.example  requirements.txt  pyproject.toml
└── Dockerfile
```

### Agent layout

```
my-agent/
├── src/
│   ├── main.py
│   ├── configs/config.py
│   ├── agents/             base · chat · planner · executor
│   ├── tools/              web_search · calculator · db_tool · rag_tool
│   ├── llm/                client · prompts · output_parser
│   ├── memory/             short_term · long_term · episodic
│   ├── workflows/          agent_loop · planner_executor · multi_agent
│   ├── retrieval/          pipeline · retriever · indexer
│   ├── guardrails/         validators · filters
│   ├── api/  cache/  monitoring/  utils/
├── data/  notebooks/  scripts/  tests/  docker/
└── .env.example  requirements.txt  pyproject.toml
```

---

## What gets generated

Every scaffold includes:

- **`pyproject.toml`** — pre-configured with your LLM and vector DB dependencies
- **`requirements.txt`** — ready to install
- **`.env.example`** — lists every required environment variable for your chosen stack
- **`README.md`** — project-specific quick start
- **`CLAUDE.md`** — context file for AI coding assistants
- **`Dockerfile`** — multi-stage build (rag/agent/full profiles)
- **`docs/`** — architecture, API reference, deployment guides
- **`.claude/rules/`** — code style and testing conventions

---

## CLI reference

```
create-ai-project new <name>   Create a new project
create-ai-project add <component>   Add a component to an existing project
create-ai-project list-profiles     List available profiles
create-ai-project --version         Show version
```

**`new` options**

```
--profile      minimal (default) | rag | agent | full
--llm          openai | anthropic | groq | ollama | azure-openai | none
--vector-db    chroma | qdrant | pinecone | weaviate | pgvector | none
--no-docker    Skip Dockerfile
--no-git       Skip git init
--description  Project description
-y / --yes     Skip interactive wizard, use defaults
```

---

## License

MIT — [5pace4/ai-scaffold](https://github.com/5pace4/ai-scaffold)

## Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.