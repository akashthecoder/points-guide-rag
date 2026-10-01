"""Tests for the FastAPI application boundary."""

from fastapi.testclient import TestClient

from points_guide_rag.api.app import create_app


def test_health_check_reports_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_answers_endpoint_returns_the_placeholder_response() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/answers",
        json={"question": "  How can I book Qatar business class?  "},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": (
            "The points guide received your question, but retrieval and generation are not "
            "connected yet."
        ),
        "status": "placeholder",
    }


def test_answers_endpoint_rejects_an_empty_question() -> None:
    client = TestClient(create_app())

    response = client.post("/api/v1/answers", json={"question": "   "})

    assert response.status_code == 422
