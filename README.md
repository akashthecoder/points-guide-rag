# Points Guide RAG

An evidence-backed assistant for U.S. points, credit-card rewards, and award travel. This is an end-to-end AI-engineering learning project built with Google ADK, Google Cloud, FastAPI, and a test-first RAG workflow.

## Local development

Install the locked project dependencies once:

```bash
uv sync --all-groups
```

Run the automated checks:

```bash
uv run pytest
uv run ruff check .
```

Start the local API:

```bash
uv run uvicorn points_guide_rag.api.app:app --reload
```

Then open `http://127.0.0.1:8000/docs` for FastAPI's generated interactive API documentation. The current `POST /api/v1/answers` endpoint is deliberately a placeholder; it validates a question but does not yet retrieve sources or call a model.

`uv sync` installs this `src/`-layout project in editable mode. That makes `points_guide_rag` importable by Uvicorn while letting local source edits take effect immediately.
