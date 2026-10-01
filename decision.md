# Decisions

## 2026-09-20 — Initial frontend approach

**Decision:** Start with FastAPI-served Jinja templates, HTML/CSS, and vanilla JavaScript `fetch()`. React is a later, optional learning milestone.

**Why:** The project owner is new to frontend development and wants to understand the request path. This approach keeps browser → HTTP → FastAPI → RAG → JSON → rendered result visible without adding a JavaScript framework and build toolchain.

**Tradeoff:** The first UI will not teach component-based frontend architecture. A focused React rebuild can provide that learning after the plain implementation is understood.

## 2026-09-20 — Corpus trust model

**Decision:** Use a three-tier corpus: official sources for factual rules, vetted expert blogs for tactics, and community sources only as corroborated leads.

**Why:** Official sources alone omit practical award-booking expertise. Expert sources such as Max Miles Points and Katie's Travel Tricks can provide valuable tactics, but their claims need visible provenance and cannot silently override issuer or airline rules.

**Tradeoff:** Source review and conflict handling add work, but prevent advice from being presented with false certainty.

## 2026-09-20 — Data stores

**Decision:** Use Cloud Spanner with the GoogleSQL dialect as the canonical metadata, session, and vector-search store. Keep raw source artifacts in Cloud Storage. Use an in-memory exact cosine-search adapter only for unit tests.

**Why:** This keeps the production system Google-native and lets the project learn transactional data modeling alongside built-in KNN/ANN vector search. It removes an unnecessary Qdrant deployment while preserving a clear `VectorStore` boundary for later comparison with Vertex AI Vector Search.

**Tradeoff:** Spanner is more infrastructure than the initial corpus requires, and its vector indexes require Enterprise or Enterprise Plus. The project must record cost and query-quality results before enabling ANN indexing.

## 2026-09-20 — Google ADK and Google Cloud as the primary platform

**Decision:** Use Google ADK with Gemini on Vertex AI for the primary agent implementation. Deploy the application first to Cloud Run, then run a deliberate comparison deployment on Vertex AI Agent Engine.

**Why:** Cloud Run keeps the FastAPI/Jinja application, custom retrieval service, and browser endpoint together while teaching containers, service accounts, Cloud Spanner, Cloud Storage, and Vertex AI. Agent Engine is then a focused learning exercise in managed ADK sessions and runtime operations rather than an early constraint on the product.

**Tradeoff:** Two deployment paths add learning work. The second path begins only after the Cloud Run baseline is evaluated and stable.

## 2026-09-20 — Agent boundary

**Decision:** ADK orchestrates conversation, typed tool calls, and response generation; deterministic Python services own retrieval, citation validation, ingestion, and card-scoring rules.

**Why:** An LLM should explain retrieved evidence, not silently decide factual rules or financial recommendation logic. This makes failures measurable and enables the same domain services to be compared with LangChain and LangGraph later.

## 2026-09-20 — Framework learning strategy

**Decision:** Keep ADK as the production baseline. Implement LangChain and LangGraph as isolated comparison labs over the same corpus, contracts, model, and gold evaluation dataset.

**Why:** Adding three orchestration frameworks to the main application would create accidental complexity. Controlled comparisons teach the real tradeoffs without confusing framework behavior for RAG quality.

## 2026-09-20 — Agent development harness

**Decision:** Use Google Agents CLI as the development harness for ADK projects.

**Why:** It supplies a consistent scaffold → playground → run → evaluation → deployment workflow and installs ADK-specific coding skills. It supports fast iteration while preserving the project’s separate pytest and retrieval-evaluation discipline.

**Tradeoff:** The CLI adds Node.js as a setup prerequisite for coding-skill installation and introduces generated project conventions. Learn its generated structure in a disposable sandbox before applying it to the main project.

## 2026-09-22 — Teach Google Cloud and ADK concepts before implementation

**Decision:** Before implementing a non-trivial Google Cloud Platform or Google ADK capability, explain its purpose, architectural role, alternatives, tradeoffs, security implications, smallest implementation step, and verification approach.

**Why:** This project is an AI-engineering learning system, not merely a delivery exercise. Explaining a concept before configuration makes design choices inspectable and reduces cargo-cult use of managed services and agent frameworks.

**Tradeoff:** Implementation takes slightly longer, but each milestone produces reusable engineering understanding rather than an opaque integration.

## 2026-09-22 — Foundation preflight and Python runtime

**Decision:** Begin Milestone 0 with the Google Agents CLI/RAG reading primer and pin the project to the installed Python 3.14 through `uv`.

**Why:** The current Google ADK release explicitly supports Python 3.14 and provides matching dependency constraints; FastAPI supports it as well. Using the already-installed interpreter reduces setup work while retaining a pinned, reproducible project runtime.

**Tradeoff:** A newly released Python version can expose lagging third-party dependencies later. The lock file, unit tests, and integration tests are the compatibility gate; if a required dependency cannot support 3.14, we will make a documented downgrade decision rather than guess.

**Verification:** After setup, `uv run python --version` must report Python 3.14, `agents-cli --version` must succeed, and the minimal project test/lint commands must run.

## 2026-09-27 — Minimal dependency foundation

**Decision:** Create a Python 3.14 `uv` project with Google ADK, FastAPI, Pydantic, and Uvicorn as runtime dependencies; use pytest, pytest-asyncio, and ruff only for development.

**Why:** These packages establish the agent, HTTP, typed-contract, and verification boundaries without prematurely adding ingestion, retrieval, Cloud Spanner, or evaluation-framework dependencies.

**Tradeoff:** The lock file and virtual environment add an up-front setup step, but make every developer and deployment use the same resolved dependency set. New dependencies will be introduced only in the milestone that teaches and uses them.

**Verification:** On 2026-09-27, `uv lock` resolved 56 packages and `uv sync --all-groups` created `.venv` with CPython 3.14.7. `uv run ruff check .` passed. `uv run pytest` executed successfully but collected zero tests (pytest's expected non-zero exit for an empty test suite); the next task is to add the first passing test.

## 2026-09-27 — First HTTP boundary contract

**Decision:** Define the first public input as a Pydantic `QuestionRequest`, with a single trimmed, non-empty question capped at 1,000 characters; reject undeclared fields.

**Why:** The API boundary is where browser-provided JSON becomes application data. A small explicit contract demonstrates validation, serialization, and testability without coupling the first lesson to FastAPI routing, ADK, or a model provider.

**Tradeoff:** Strictly rejecting extra fields means the browser cannot send an experimental field until the contract changes. That intentional friction protects the API from silently accepting misspelled or unsupported inputs.

**Verification:** On 2026-09-27, four contract tests and Ruff passed. `pytest-asyncio` emitted an upstream deprecation warning concerning an API scheduled for removal in Python 3.16; no asynchronous code exists in this slice, so defer action until the first async ADK/FastAPI integration test.

## 2026-09-30 — Thin FastAPI HTTP slice before agent integration

**Decision:** Add an application factory with a health endpoint and a versioned, typed `POST /api/v1/answers` endpoint that returns an explicit placeholder response.

**Why:** This establishes the web boundary and proves Pydantic validation works through real HTTP handling before ADK, Gemini, retrieval, credentials, or cloud infrastructure complicate failure diagnosis. The factory supports dependency injection in later tests instead of binding tests to global external state.

**Tradeoff:** The endpoint has no useful travel-answering capability yet. This is intentional: returning a transparent placeholder is safer than producing an uncited answer before the evidence pipeline exists.

**Verification:** On 2026-09-30, `uv run pytest` passed all 7 tests and `uv run ruff check .` passed. Test startup reports an upstream Starlette `TestClient` deprecation warning alongside the existing `pytest-asyncio` Python 3.14 warning; neither affects this isolated HTTP slice, and both remain visible rather than suppressed.

## 2026-09-30 — Install the project with a `src/` layout

**Decision:** Make the repository an installable package using Hatchling as the build backend, and let `uv sync` install it in editable mode.

**Why:** `src/` keeps application code separate from repository files and prevents accidental imports from the checkout root. However, Uvicorn does not use pytest's test-only import path configuration. An editable installation makes the same `points_guide_rag` import work in pytest, Uvicorn, scripts, and eventually a container.

**Tradeoff:** The project now has a lightweight build-backend dependency during environment setup. This is more explicit and reproducible than requiring every runtime command to remember `--app-dir src`.

**Verification:** On 2026-09-30, `uv sync --all-groups` built and installed `points-guide-rag` in editable mode. `uv run python -c "import points_guide_rag"` resolved to `src/points_guide_rag/__init__.py`; all 7 tests and Ruff then passed.
