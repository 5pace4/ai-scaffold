# create-ai-project

Scaffold production-ready AI project structures in seconds.

```bash
pip install create-ai-project
create-ai-project new my-rag-app --profile rag
```

---

## What it does

Creates a clean folder structure with empty files for your AI project — no boilerplate code, no opinions on implementation. You get the architecture, you write the logic.

---

## Install

```bash
pip install create-ai-project
# or
uv add create-ai-project
```

---

## Usage

### Create a new project

```bash
create-ai-project new <project-name> [OPTIONS]
```

**Options**

| Flag | Default | Description |
|---|---|---|
| `--profile` | `rag` | Project profile: `minimal`, `rag`, `agent`, `full` |
| `--llm` | interactive | LLM provider: `openai`, `anthropic`, `groq`, `ollama`, `azure-openai` |
| `--vector-db` | interactive | Vector DB: `chroma`, `qdrant`, `pinecone`, `weaviate`, `pgvector` |
| `--no-docker` | — | Skip Dockerfile |
| `--no-git` | — | Skip `git init` |
| `--yes` / `-y` | — | Use defaults, skip wizard |

**Examples**

```bash
# Interactive wizard
create-ai-project new my-rag-app

# Non-interactive
create-ai-project new my-agent --profile agent --llm anthropic --vector-db qdrant -y
```

---

## Profiles

| Profile | What you get |
|---|---|
| `minimal` | `src/` skeleton, configs, utils, tests |
| `rag` | + ingestion, embedding, vectorstore, rag, evaluation, api, cache, monitoring |
| `agent` | + agents, tools, llm, memory, workflows, retrieval, guardrails, api, cache, monitoring |
| `full` | RAG + Agent combined, frontend/ directory |

### RAG structure

```
my-rag-app/
├── src/
│   ├── main.py
│   ├── configs/config.py
│   ├── ingestion/          # loader, chunker, cleaner
│   ├── embedding/          # embedder, utils
│   ├── vectorstore/        # client, indexer, retriever
│   ├── rag/                # pipeline, prompt, generator
│   ├── evaluation/         # metrics, evaluator
│   ├── api/                # routes, schemas, controllers
│   ├── cache/              # redis_client
│   ├── monitoring/         # tracing, metrics
│   └── utils/              # logger, helpers
├── data/raw/  data/processed/  data/embeddings/
├── notebooks/  scripts/  tests/
├── .env.example  requirements.txt  pyproject.toml
└── Dockerfile
```

### Agent structure

```
my-agent/
├── src/
│   ├── main.py
│   ├── configs/config.py
│   ├── agents/             # base, chat, planner, executor
│   ├── tools/              # web_search, calculator, db_tool, rag_tool
│   ├── llm/                # client, prompts, output_parser
│   ├── memory/             # short_term, long_term, episodic
│   ├── workflows/          # agent_loop, planner_executor, multi_agent
│   ├── retrieval/          # pipeline, retriever, indexer
│   ├── guardrails/         # validators, filters
│   ├── api/  cache/  monitoring/  utils/
├── data/  notebooks/  scripts/  tests/  docker/
└── .env.example  requirements.txt  pyproject.toml
```

---

## Other commands

```bash
# List profiles
create-ai-project list-profiles

# Show version
create-ai-project --version
```

---

## License

MIT
