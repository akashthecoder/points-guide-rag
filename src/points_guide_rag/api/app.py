"""FastAPI application factory for the points-guide HTTP API."""

from fastapi import FastAPI

from points_guide_rag.api.contracts import AnswerResponse, QuestionRequest


def create_app() -> FastAPI:
    """Create the HTTP application without connecting to external services."""
    app = FastAPI(
        title="Points Guide RAG API",
        version="0.1.0",
        description="Evidence-backed points and award-travel research assistant.",
    )

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Report whether the web process can receive requests."""
        return {"status": "ok"}

    @app.post("/api/v1/answers", response_model=AnswerResponse)
    async def answer_question(request: QuestionRequest) -> AnswerResponse:
        """Accept a validated question until retrieval and generation are connected."""
        return AnswerResponse(
            answer=(
                "The points guide received your question, but retrieval and generation are "
                "not connected yet."
            ),
            status="placeholder",
        )

    return app


app = create_app()
