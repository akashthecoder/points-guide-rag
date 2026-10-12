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

## Local ADK tool-use lab

After enabling Vertex AI, configuring ADC, and reading the local-authentication notes in `reading.md`, run one controlled model/tool-call trace:

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=rag-project-511419
export GOOGLE_CLOUD_LOCATION=us-central1
uv run python -m points_guide_rag.agents.run_tool_lab
```

This makes a billable Vertex AI request using your local ADC identity. It uses an in-memory ADK session, asks the model to count words, and prints the event trace. It does not persist session data or answer points/travel questions.
