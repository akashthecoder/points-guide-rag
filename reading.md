# Reading Notes

Use [plan.md](plan.md) for the ordered reading sequence and add personal notes below each item as the corresponding milestone begins.

## How to use papers and articles

Do **not** begin by reading papers cover to cover. For each concept, read the companion article or tutorial first, implement a small experiment, then read the paper selectively. Articles teach the vocabulary and practical workflow; papers explain the original problem, assumptions, evaluation method, and limitations.

Use this three-pass paper method:

1. Read the abstract, introduction, diagrams, tables, and conclusion. Write one paragraph in your own words.
2. Identify one design choice that affects this project and one metric the authors use.
3. Read the method/math only when you are changing that part of the implementation. Do not block progress on understanding every equation.

For this project, articles are the required first pass. Papers are the deeper, optional second pass—except when an experiment result surprises you or you are choosing between competing retrieval approaches.

## Papers with companion articles and experiments

| Concept | Read first: article/tutorial | Then, when ready: paper | Project experiment |
|---|---|---|---|
| RAG fundamentals | [Google Cloud: What is RAG?](https://cloud.google.com/use-cases/retrieval-augmented-generation) | [RAG: Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | Trace one answer from retrieval through cited generation. |
| Dense retrieval | [Sentence Transformers: Semantic Search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/) | [Dense Passage Retrieval](https://arxiv.org/abs/2004.04906) | Compare semantic retrieval with BM25 on 10 labeled questions. |
| Sentence embeddings | [Sentence Transformers usage](https://www.sbert.net/docs/sentence_transformer/usage/usage.html) | [Sentence-BERT](https://arxiv.org/abs/1908.10084) | Embed a query and three chunks; inspect cosine-similarity ranking. |
| Lexical retrieval / BM25 | [Elastic: Practical BM25](https://www.elastic.co/blog/practical-bm25-part-1-how-shards-affect-relevance-scoring-in-elasticsearch) | [BM25/BM25F in Lucene](https://arxiv.org/abs/0911.5046) | Calculate one BM25 score by hand, then compare it with semantic search. |
| Retrieval evaluation | [Elasticsearch Labs: BEIR and search relevance](https://www.elastic.co/search-labs/blog/evaluating-search-relevance-part-1) | [BEIR](https://arxiv.org/abs/2104.08663) | Calculate Recall@5 and MRR from the gold dataset. |
| RAG evaluation | [Ragas available metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) | [RAGAS](https://arxiv.org/abs/2309.15217) | Compare a manual citation review with a faithfulness score. |
| Spanner vector search | [Spanner vector-search tutorial](https://docs.cloud.google.com/spanner/docs/vector-search-tutorial) | No paper required initially; read [ScaNN](https://arxiv.org/abs/1908.10396) only when tuning ANN behavior | Run exact KNN first, then measure ANN recall and latency with a vector index. |

## Rules for notes

- Summarize the central idea in your own words.
- State where it appears in this project.
- Record one question or experiment it motivates.

## Immediate reading — Pydantic contracts and pytest

Read these before we add the FastAPI route. No paper is needed for this stage.

1. **Start here:** [Real Python: Pydantic—Simplifying Data Validation](https://realpython.com/python-pydantic/) — a practical explanation of the problem before the API details (about 20–30 minutes). It contrasts fragile, manually checked Python data with a model that validates and serializes itself. Focus on the motivation, `BaseModel`, and validation errors; skip advanced sections for now.
2. [Pydantic: Why use Pydantic Validation?](https://pydantic.dev/docs/validation/latest/get-started/why/) — a short official companion explaining the design rationale and tradeoffs (about 10 minutes).
3. [Pydantic: Models](https://pydantic.dev/docs/validation/latest/concepts/models/) — use this as the reference after the articles (about 15–20 minutes). Focus on `BaseModel`, type annotations, `ValidationError`, and `model_dump()`.
4. [pytest: Get Started](https://pytest.org/en/latest/getting-started.html) — read the first examples (about 10 minutes). Focus on plain `assert` and how pytest finds functions beginning with `test_`.
5. [pytest: `raises`](https://docs.pytest.org/en/stable/reference/reference.html#pytest.raises) — skim this after the first item (about 5 minutes). It explains the pattern used to prove invalid input is rejected.

Small exercise after reading: add a temporary assertion that `QuestionRequest(question="Hello").model_dump()` is `{"question": "Hello"}`, run `uv run pytest`, then remove the temporary assertion. This connects the model, serialization, and test runner without adding another project feature.

## Immediate reading — FastAPI HTTP endpoints

Read these after the Pydantic section and before adding ADK. No paper is needed for this stage.

1. **Start here:** [FastAPI: First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) — read through the path-operation examples (about 15 minutes). Map `FastAPI()` to our `app`, `@app.get` / `@app.post` to our routes, and the function beneath each decorator to an endpoint handler.
2. [FastAPI: Request Body](https://fastapi.tiangolo.com/tutorial/body/) — read the whole short page (about 10 minutes). It explains why FastAPI turns the `request: QuestionRequest` parameter into validated JSON input and returns a `422` response for invalid input.
3. [FastAPI: Testing](https://fastapi.tiangolo.com/tutorial/testing/) — read the `TestClient` section (about 10 minutes). It directly matches `tests/api/test_app.py`: test functions stay synchronous even though the endpoint is declared `async`.

While reading, run the application with `uv run uvicorn points_guide_rag.api.app:app --reload`, open `http://127.0.0.1:8000/docs`, and submit one valid and one blank question to `POST /api/v1/answers`. Observe the `200` placeholder response and the automatic `422` validation response. Stop the server with `Ctrl+C` when finished.

## Agent development harness — complete before Milestone 0

Google Agents CLI is the development harness for this project’s Google ADK work. ADK is the framework used to write agents; Agents CLI provides the practical surrounding loop: scaffolding, a local playground, structured agent evaluations, deployment helpers, and observability.

### Prerequisites

- Python 3.14 and `uv` are already project requirements.
- Install Node.js before harness setup; Google Agents CLI uses it when installing coding-agent skills.
- Install the Google Cloud CLI for Vertex AI and deployment work.
- For local Gemini/Vertex AI development, authenticate with Application Default Credentials and configure a billed Google Cloud project.

### One-time workstation setup

Run these commands from a terminal, not from application code:

```bash
uvx google-agents-cli setup
gcloud auth application-default login
gcloud config set project YOUR_GOOGLE_CLOUD_PROJECT_ID
export GOOGLE_CLOUD_LOCATION="us-east1"
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
agents-cli login --status
```

`uvx google-agents-cli setup` installs the CLI and its ADK lifecycle skills for supported coding environments. It changes local development-tool configuration, so read and approve its prompts rather than treating it as an application dependency. Vertex AI deployment also requires billing and the appropriate IAM permissions.

### Learn the harness safely in a disposable sandbox

Do this before scaffolding the main points-guide agent. Create the sandbox beside the project or in another scratch directory so generated files do not obscure this repository:

```bash
agents-cli create adk-sandbox --prototype --yes
cd adk-sandbox
agents-cli install
agents-cli playground
```

The playground should open at `http://localhost:8080` with hot reload. Add one tiny typed tool, run it interactively, then test it from the terminal:

```bash
agents-cli run "Use the sample tool once"
agents-cli eval run
```

Read the generated `GEMINI.md`, `agents-cli-manifest.yaml`, `tests/`, and evaluation dataset before deleting or keeping the sandbox. The goal is to understand what the harness generated, not merely to make its sample pass.

### Daily development loop for this project

1. Start the local stack and the agent playground.
2. Make one change: agent instruction, typed tool, retrieval adapter, or structured-output contract.
3. Exercise the narrow behavior in the playground and with `agents-cli run`.
4. Run `uv run pytest` for deterministic services and `agents-cli eval run` for agent behavior.
5. Inspect failed tool and agent traces; turn every meaningful failure into a versioned gold evaluation case.
6. Record the result in `decision.md` and milestone evidence in `plan.md`.
7. Deploy only after local quality gates pass.

### Main-project deployment harness sequence

When the Cloud Run milestone begins, add deployment scaffolding rather than hand-assembling it first:

```bash
agents-cli scaffold enhance --deployment-target cloud_run
agents-cli deploy
agents-cli deploy --status
```

Use `agents-cli infra single-project` only after the manual deployment works and you need provisioned service accounts, IAM, telemetry resources, or Terraform-managed infrastructure. Do not run it casually: it plans or provisions cloud resources.

### Required reading

- [Agents CLI getting started](https://google.github.io/agents-cli/guide/getting-started/) — setup, prerequisites, and coding-agent skills.
- [Manual workflow tutorial](https://google.github.io/agents-cli/guide/hands-on-tutorial/) — scaffold, playground, terminal run, evaluation, deployment, and trace inspection.
- [Agents CLI project structure](https://google.github.io/agents-cli/guide/project-structure/) — understand generated manifests, agent files, tests, and guidance.
- [Agents CLI evaluation guide](https://google.github.io/agents-cli/guide/evaluation/) — agent-specific evaluation datasets and grading.
- [Agents CLI deployment guide](https://google.github.io/agents-cli/guide/deployment/) — Cloud Run, Agent Runtime, infrastructure, and CI/CD.
- [Agents CLI authentication guide](https://google.github.io/agents-cli/guide/authentication/) — Gemini API keys versus Vertex AI/Application Default Credentials.

## Pending

- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- Dense Passage Retrieval
- Sentence-BERT
- BEIR
- RAGAS
- FastAPI templates
- MDN Fetch API
- Cloud Spanner overview and GoogleSQL dialect
- Spanner vector search overview and tutorial
- Google ADK documentation and function tools
- Vertex AI Agent Engine deployment
- Cloud Run FastAPI and Spanner data path
- Vertex AI Vector Search comparison
- LangChain RAG tutorial
- LangGraph reference
- Google Agents CLI harness and manual workflow
