"""Tests for API contracts independent of FastAPI and ADK."""

import pytest
from pydantic import ValidationError

from points_guide_rag.api.contracts import QuestionRequest


def test_question_request_accepts_and_trims_a_question() -> None:
    request = QuestionRequest(question="  How can I book Qatar business class?  ")

    assert request.question == "How can I book Qatar business class?"


@pytest.mark.parametrize("question", ["", "   "])
def test_question_request_rejects_an_empty_question(question: str) -> None:
    with pytest.raises(ValidationError):
        QuestionRequest(question=question)


def test_question_request_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        QuestionRequest(question="Which card should I start with?", card_name="Venture X")
