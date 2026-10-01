# Project Flow

## Intended request flow

1. The browser loads a Jinja-rendered page from FastAPI.
2. Vanilla JavaScript sends a typed JSON question to `POST /api/v1/answers` using `fetch()`; `QuestionRequest` trims and validates the question before downstream work starts.
3. FastAPI validates the request with Pydantic and creates or resumes an ADK session. Until the ADK integration milestone, this boundary returns an explicit placeholder response instead.
4. The Google ADK root agent calls the typed `retrieve_evidence` tool.
5. The deterministic retrieval workflow filters, searches, fuses, and selects date-stamped source chunks.
6. The ADK agent creates a grounded response; server-side validation verifies that citations reference retrieved chunks or returns an explicit coverage gap.
7. FastAPI returns structured JSON containing the answer, citations, warnings, ADK/tool trace metadata, and trace ID.
8. The browser renders the response and a citation drawer.
9. Logs, feedback, ADK events, and evaluation results use the trace ID for later analysis.

## Intended ingestion flow

1. A reviewer adds an approved source to `sources/registry.yaml` with a trust tier and reason.
2. The ingestion job fetches the source within site constraints and preserves raw HTML/PDF.
3. Extraction produces normalized Markdown and structured tables.
4. Validation records source metadata, date, hash, and reviewer state.
5. Chunking creates heading-aware, traceable chunks.
6. Embedding and indexing write source/chunk metadata and embeddings to Cloud Spanner; unit tests use the in-memory exact-search adapter.
7. Evaluation runs against the new corpus version before it becomes the default.

## Google Cloud deployment flow

1. Cloud Build creates a container image and stores it in Artifact Registry.
2. Cloud Run deploys FastAPI, Jinja UI, and the ADK application using a dedicated service account.
3. The service account accesses Gemini through Vertex AI, metadata/sessions/vectors through Cloud Spanner, and raw artifacts through Cloud Storage.
4. Cloud Run Jobs perform ingestion and re-indexing outside the request-serving service.
5. Cloud Logging, Trace, Monitoring, and budget alerts collect operational evidence.
6. After Cloud Run evaluation gates pass, the same ADK root agent is deployed to Agent Engine for a controlled runtime comparison.

## Agent development harness flow

1. Google Agents CLI scaffolds or enhances an ADK project and supplies a manifest, local playground, tests, and evaluation configuration.
2. The developer changes one agent/tool/prompt behavior at a time.
3. The local playground and terminal run provide interactive feedback; pytest validates deterministic domain code.
4. Agents CLI evaluations validate agent and tool behavior against versioned cases.
5. Failed traces become new regression cases before a deployment is attempted.
6. Deployment and cloud traces are inspected only after local quality gates pass.
