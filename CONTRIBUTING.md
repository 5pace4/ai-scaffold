# Contributing to ai-scaffold

## Dev setup

```bash
git clone https://github.com/tofayel/ai-scaffold
cd ai-scaffold
uv sync
```

Verify it works:
```bash
uv run create-ai-project --help
```

## Running tests

```bash
uv run pytest tests/ -v
uv run pytest --cov=ai_scaffold --cov-report=term-missing
```

## Linting

```bash
uv run ruff check src/ tests/
uv run mypy src/
```

## Adding a new profile

1. Create `src/ai_scaffold/profiles/myprofile.py`
2. Define a `MY_MANIFEST` list of template keys from `MANIFEST_MAP`
3. Call `register_profile(Profile(name="myprofile", ...))`
4. Import it in `cli.py` alongside the other profile imports

## Adding a new template

1. Add a `.j2` file under `src/ai_scaffold/templates/`
2. Add a `ManifestEntry` to `MANIFEST_MAP` in `generator/engine.py`
3. Add the key to the relevant profile manifests

## Adding a new LLM provider or vector DB

1. Update `LLM_PROVIDERS` / `VECTOR_DBS` in `generator/context.py`
2. Add deps to `LLM_DEPS` / `VECTOR_DB_DEPS`
3. Add a `{% if llm_provider == "..." %}` branch to the affected templates
4. Add a wizard choice in `prompts/interactive.py`

## Releasing

1. Bump `version` in `pyproject.toml` and `src/ai_scaffold/__init__.py`
2. Update `CHANGELOG.md`
3. Create a GitHub release — the publish workflow handles PyPI automatically
